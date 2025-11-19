"""
Vector Store module: Manages FAISS vector database for RAG
"""

import faiss
import numpy as np
import pickle
import os
from typing import List, Dict, Any, Tuple, Optional
import logging
from pathlib import Path
from .embeddings import EmbeddingManager
from ..utils.config import settings

logger = logging.getLogger(__name__)


class VectorStore:
    """Manages FAISS vector store for knowledge retrieval"""

    def __init__(self, index_path: str = None):
        """
        Initialize vector store

        Args:
            index_path: Path to store/load FAISS index
        """
        self.index_path = index_path or settings.FAISS_INDEX_PATH
        self.embedding_manager = EmbeddingManager()
        self.dimension = self.embedding_manager.get_embedding_dimension()

        # Initialize FAISS index
        self.index = None
        self.metadata = []  # Store metadata for each document

        # Create directory if it doesn't exist
        Path(self.index_path).parent.mkdir(parents=True, exist_ok=True)

        # Try to load existing index
        self.load_index()

    def create_index(self, use_gpu: bool = False):
        """
        Create a new FAISS index

        Args:
            use_gpu: Whether to use GPU for FAISS (if available)
        """
        logger.info(f"Creating new FAISS index with dimension {self.dimension}")

        # Use IndexFlatL2 for exact search (can be replaced with IndexIVFFlat for larger datasets)
        self.index = faiss.IndexFlatL2(self.dimension)

        # Optionally use GPU
        if use_gpu and faiss.get_num_gpus() > 0:
            logger.info("Using GPU for FAISS")
            self.index = faiss.index_cpu_to_gpu(
                faiss.StandardGpuResources(), 0, self.index
            )

        self.metadata = []
        logger.info("FAISS index created successfully")

    def add_documents(
        self,
        texts: List[str],
        metadatas: List[Dict[str, Any]],
        ids: Optional[List[str]] = None,
    ) -> int:
        """
        Add documents to the vector store

        Args:
            texts: List of text documents
            metadatas: List of metadata dictionaries
            ids: Optional list of IDs for documents

        Returns:
            Number of documents added
        """
        if self.index is None:
            self.create_index()

        if len(texts) != len(metadatas):
            raise ValueError("Number of texts and metadatas must match")

        logger.info(f"Adding {len(texts)} documents to vector store")

        # Generate embeddings
        embeddings = self.embedding_manager.embed_texts(texts)

        # Add to FAISS index
        self.index.add(embeddings.astype('float32'))

        # Store metadata
        for i, (text, metadata) in enumerate(zip(texts, metadatas)):
            doc_id = ids[i] if ids and i < len(ids) else f"doc_{len(self.metadata)}"
            self.metadata.append({
                "id": doc_id,
                "text": text,
                **metadata,
            })

        logger.info(f"Successfully added {len(texts)} documents")
        return len(texts)

    def search(
        self,
        query: str,
        k: int = 5,
        score_threshold: float = None,
    ) -> List[Dict[str, Any]]:
        """
        Search for similar documents

        Args:
            query: Query text
            k: Number of results to return
            score_threshold: Minimum similarity score threshold

        Returns:
            List of matching documents with scores
        """
        if self.index is None or self.index.ntotal == 0:
            logger.warning("Vector store is empty")
            return []

        # Generate query embedding
        query_embedding = self.embedding_manager.embed_text(query)
        query_embedding = query_embedding.reshape(1, -1).astype('float32')

        # Search in FAISS
        distances, indices = self.index.search(query_embedding, min(k, self.index.ntotal))

        # Process results
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < 0 or idx >= len(self.metadata):
                continue

            # Convert L2 distance to similarity score (0-1)
            # Using exponential decay: similarity = exp(-distance)
            similarity_score = float(np.exp(-dist))

            # Apply threshold if specified
            if score_threshold and similarity_score < score_threshold:
                continue

            result = {
                **self.metadata[idx],
                "similarity_score": round(similarity_score, 4),
                "distance": float(dist),
            }
            results.append(result)

        logger.info(f"Found {len(results)} results for query")
        return results

    def save_index(self, path: str = None):
        """
        Save FAISS index and metadata to disk

        Args:
            path: Optional custom path to save index
        """
        save_path = path or self.index_path

        if self.index is None:
            logger.warning("No index to save")
            return

        try:
            # Ensure directory exists
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)

            # Save FAISS index
            index_file = f"{save_path}.faiss"
            faiss.write_index(self.index, index_file)

            # Save metadata
            metadata_file = f"{save_path}.pkl"
            with open(metadata_file, 'wb') as f:
                pickle.dump(self.metadata, f)

            logger.info(f"Index saved successfully to {save_path}")
        except Exception as e:
            logger.error(f"Error saving index: {e}")
            raise

    def load_index(self, path: str = None):
        """
        Load FAISS index and metadata from disk

        Args:
            path: Optional custom path to load index from
        """
        load_path = path or self.index_path
        index_file = f"{load_path}.faiss"
        metadata_file = f"{load_path}.pkl"

        if not os.path.exists(index_file) or not os.path.exists(metadata_file):
            logger.info("No existing index found, will create new one when needed")
            return False

        try:
            # Load FAISS index
            self.index = faiss.read_index(index_file)

            # Load metadata
            with open(metadata_file, 'rb') as f:
                self.metadata = pickle.load(f)

            logger.info(
                f"Index loaded successfully with {self.index.ntotal} documents"
            )
            return True
        except Exception as e:
            logger.error(f"Error loading index: {e}")
            self.index = None
            self.metadata = []
            return False

    def delete_index(self):
        """Delete the current index"""
        self.index = None
        self.metadata = []
        logger.info("Index deleted from memory")

    def get_document_count(self) -> int:
        """Get the number of documents in the index"""
        return self.index.ntotal if self.index else 0

    def get_document_by_id(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a document by its ID

        Args:
            doc_id: Document ID

        Returns:
            Document metadata or None
        """
        for doc in self.metadata:
            if doc.get("id") == doc_id:
                return doc
        return None
