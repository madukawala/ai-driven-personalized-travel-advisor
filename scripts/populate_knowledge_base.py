"""
Script to populate the vector store with sample travel knowledge
This creates sample travel content for the RAG system
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../backend"))

from app.rag.vector_store import VectorStore
import asyncio


# Sample travel knowledge data
SAMPLE_TRAVEL_DATA = [
    {
        "text": "Tokyo's Tsukiji Outer Market is best visited early in the morning, around 5-6 AM, "
        "when the freshest seafood arrives. The inner market has moved to Toyosu, but the outer market "
        "remains a fantastic place for street food. Try the fresh sushi, tamagoyaki (Japanese omelet), "
        "and grilled seafood. Budget around $30-50 per person for a good breakfast experience.",
        "source_name": "Nomadic Matt",
        "source_type": "blog",
        "destination": "Tokyo",
        "locations": ["Tsukiji", "Tokyo"],
        "categories": ["food", "culture", "morning activities"],
        "source_url": "https://nomadicmatt.com/travel-guides/japan-travel-tips/tokyo/",
    },
    {
        "text": "Paris museums are free on the first Sunday of each month. The Louvre can be overwhelming, "
        "so focus on specific sections like the Italian Renaissance or Egyptian antiquities. "
        "Book tickets online to skip the lines. The museum is least crowded on Wednesday and Friday evenings. "
        "Consider getting a Museum Pass if you plan to visit multiple museums.",
        "source_name": "Lonely Planet",
        "source_type": "guidebook",
        "destination": "Paris",
        "locations": ["Paris", "Louvre", "France"],
        "categories": ["culture", "art", "museums", "budget tips"],
        "source_url": "https://lonelyplanet.com/france/paris",
    },
    {
        "text": "Bangkok's Grand Palace is a must-see but requires modest dress - shoulders and knees covered. "
        "Visit early morning (before 10 AM) to avoid crowds and heat. Entry is 500 baht ($15). "
        "Beware of scams from touts outside saying the palace is closed - it's open daily 8:30 AM to 3:30 PM. "
        "Combine with nearby Wat Pho to see the Reclining Buddha.",
        "source_name": "TripAdvisor",
        "source_type": "article",
        "destination": "Bangkok",
        "locations": ["Bangkok", "Grand Palace", "Wat Pho", "Thailand"],
        "categories": ["culture", "temples", "sightseeing"],
        "source_url": "https://tripadvisor.com/bangkok",
    },
    {
        "text": "Rome's Vatican Museums are incredibly crowded. Book skip-the-line tickets well in advance. "
        "The Sistine Chapel is the highlight but photos are not allowed. Plan for 3-4 hours minimum. "
        "Tuesday and Thursday mornings are least crowded. Consider a small group tour for insights. "
        "Dress code: covered shoulders and knees. Budget €17 for entry plus €5 for online booking.",
        "source_name": "Lonely Planet",
        "source_type": "guidebook",
        "destination": "Rome",
        "locations": ["Rome", "Vatican", "Sistine Chapel", "Italy"],
        "categories": ["culture", "art", "museums", "religious sites"],
        "source_url": "https://lonelyplanet.com/italy/rome",
    },
    {
        "text": "London's Borough Market is excellent for food lovers. Open Monday-Saturday with full operation on Fridays and Saturdays. "
        "Try the grilled cheese sandwiches, fresh oysters, and international street food. Budget £15-25 per person. "
        "Get there before noon to avoid peak crowds. The market is near London Bridge station. "
        "Combine with a walk along the Thames and visit to Shakespeare's Globe Theatre.",
        "source_name": "Reddit Travel",
        "source_type": "reddit",
        "destination": "London",
        "locations": ["London", "Borough Market", "London Bridge", "UK"],
        "categories": ["food", "markets", "walking"],
        "source_url": "https://reddit.com/r/travel",
    },
    {
        "text": "Barcelona's Sagrada Familia requires advance booking, often weeks ahead in summer. "
        "Book the earliest slot (9 AM) for best light and fewer crowds. Audio guide is essential. "
        "Budget €26 for basic entry, €36 with tower access. Plan 2-3 hours. "
        "Combine with Casa Batlló and Park Güell for a Gaudí-themed day. "
        "The towers offer amazing views but involve stairs - not suitable for those with mobility issues.",
        "source_name": "Nomadic Matt",
        "source_type": "blog",
        "destination": "Barcelona",
        "locations": ["Barcelona", "Sagrada Familia", "Spain"],
        "categories": ["architecture", "culture", "sightseeing"],
        "source_url": "https://nomadicmatt.com/travel-guides/spain-travel-tips/barcelona/",
    },
    {
        "text": "Kyoto's Fushimi Inari Shrine with its thousands of red torii gates is free to visit 24/7. "
        "Early morning (before 8 AM) or late afternoon (after 4 PM) offers fewer crowds and better photos. "
        "The full hike to the summit takes 2-3 hours. There are exit points if you don't want to complete the full trail. "
        "Wear comfortable shoes. Street food vendors near the entrance sell traditional snacks.",
        "source_name": "Lonely Planet",
        "source_type": "guidebook",
        "destination": "Kyoto",
        "locations": ["Kyoto", "Fushimi Inari", "Japan"],
        "categories": ["temples", "hiking", "photography", "free activities"],
        "source_url": "https://lonelyplanet.com/japan/kyoto",
    },
    {
        "text": "New York City's Central Park is perfect for a budget-friendly day. Free activities include walking, "
        "visiting Bethesda Fountain, Bow Bridge, and Strawberry Fields. Summer features free concerts and Shakespeare in the Park. "
        "Bike rentals available for around $15/hour. Best visited on weekday mornings for peaceful atmosphere. "
        "Combine with nearby free museums like the Met (suggested donation) on Sundays.",
        "source_name": "Budget Travel Blog",
        "source_type": "blog",
        "destination": "New York",
        "locations": ["New York", "Central Park", "USA"],
        "categories": ["parks", "walking", "budget tips", "free activities"],
        "source_url": "https://budgettravel.com/nyc",
    },
    {
        "text": "Amsterdam's Anne Frank House requires online booking weeks in advance. Tours run every 15 minutes. "
        "The experience is moving but crowded. Budget €14 for adults. Plan 75-90 minutes. "
        "Evening slots (after 6 PM) are slightly less crowded. Photography not allowed inside. "
        "Combine with a canal walk and visit to the nearby Westerkerk church which offers tower climbs with city views.",
        "source_name": "TripAdvisor",
        "source_type": "article",
        "destination": "Amsterdam",
        "locations": ["Amsterdam", "Anne Frank House", "Netherlands"],
        "categories": ["museums", "history", "culture"],
        "source_url": "https://tripadvisor.com/amsterdam",
    },
    {
        "text": "Istanbul's Grand Bazaar is one of the world's oldest covered markets. Open Monday-Saturday 9 AM-7 PM. "
        "Bargaining is expected - start at 40-50% of the asking price. Best for carpets, ceramics, jewelry, and textiles. "
        "Avoid tourist trap restaurants inside - eat at local spots outside the bazaar. "
        "Visit early morning for a more authentic experience with fewer tourists. "
        "Combine with nearby Spice Bazaar and Blue Mosque.",
        "source_name": "Reddit Travel",
        "source_type": "reddit",
        "destination": "Istanbul",
        "locations": ["Istanbul", "Grand Bazaar", "Turkey"],
        "categories": ["shopping", "markets", "culture"],
        "source_url": "https://reddit.com/r/travel",
    },
    {
        "text": "Venice during Acqua Alta (high water) requires rubber boots. Water levels peak November-March. "
        "St. Mark's Square floods first. Elevated walkways are set up during flooding. "
        "Consider visiting in shoulder season (April-May, September-October) for better weather and fewer crowds. "
        "Venice is very expensive - budget €15-25 for casual meals, €40+ for sit-down restaurants. "
        "Avoid restaurants with touts outside - find places where locals eat.",
        "source_name": "Lonely Planet",
        "source_type": "guidebook",
        "destination": "Venice",
        "locations": ["Venice", "St. Mark's Square", "Italy"],
        "categories": ["weather tips", "budget tips", "seasonal advice"],
        "source_url": "https://lonelyplanet.com/italy/venice",
    },
    {
        "text": "Dubai's desert safari tours are popular but choose carefully. Morning safaris are cooler but less dramatic for photos. "
        "Evening safaris include dinner and entertainment, budget around $60-80 per person. "
        "Sunset timing is best for photos. Activities include dune bashing, camel rides, and sandboarding. "
        "Summer months (June-August) are extremely hot - winter (November-March) is ideal. "
        "Book through reputable companies, not street vendors.",
        "source_name": "Travel Blog",
        "source_type": "blog",
        "destination": "Dubai",
        "locations": ["Dubai", "UAE"],
        "categories": ["adventure", "desert", "tours"],
        "source_url": "https://travelblog.com/dubai",
    },
]


def populate_vector_store():
    """Populate vector store with sample data"""
    print("Initializing vector store...")
    vector_store = VectorStore()

    # Prepare texts and metadata
    texts = [doc["text"] for doc in SAMPLE_TRAVEL_DATA]
    metadatas = [
        {
            "source_name": doc["source_name"],
            "source_type": doc["source_type"],
            "destination": doc["destination"],
            "locations": doc["locations"],
            "categories": doc["categories"],
            "source_url": doc["source_url"],
        }
        for doc in SAMPLE_TRAVEL_DATA
    ]

    # Add documents
    print(f"Adding {len(texts)} documents to vector store...")
    count = vector_store.add_documents(texts, metadatas)

    print(f"Successfully added {count} documents")

    # Save index
    print("Saving vector store...")
    vector_store.save_index()

    print("✅ Vector store populated successfully!")

    # Test search
    print("\nTesting search functionality...")
    results = vector_store.search("food in Tokyo", k=3)

    print(f"\nFound {len(results)} results for 'food in Tokyo':")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result.get('destination')} - {result.get('source_name')}")
        print(f"   Score: {result.get('similarity_score')}")
        print(f"   Text: {result.get('text')[:100]}...")


if __name__ == "__main__":
    populate_vector_store()
