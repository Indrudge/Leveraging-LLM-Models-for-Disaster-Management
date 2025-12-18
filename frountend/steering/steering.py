from frountend.steering import news, llm, map
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "news_db"
RESULT_COLLECTION = "results_final"

def process_disaster_request(disaster_type, location):
    """
    Process the user input, search the database, and return disaster details.
    If not found, run `news.py` and `llm.py` to fetch and process data.
    """
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[RESULT_COLLECTION]

    # Search for disaster details in the database
    result = collection.find_one({"type": disaster_type, "location": location})

    if result:
        # Data exists in the database
        context = {
            "disaster": {
                "location": result.get("location", "Unknown Disaster"),
                "title": result.get("type", "Unknown Disaster"),
                "details": result.get("details", "No details available."),
            },
        }
    else:
        # Data doesn't exist; run `news.py` and `llm.py`
        print(f"Data not found for {disaster_type} in {location}. Running news and llm processing...")
        news.fetch_and_store_news()
        llm.process_news()

        # Recheck the database after processing
        result = collection.find_one({"type": disaster_type, "location": location})
        if result:
            context = {
                "disaster": {
                    "location": result.get("location", "Unknown Disaster"),
                    "title": result.get("type", "Unknown Disaster"),
                    "details": result.get("details", "No details available."),
                },
            }
        else:
            # Return default response if no data is still found
            context = {
                "disaster": {
                    "location": "",
                    "title": "No Results Found",
                    "details": "We could not find any matching disaster data.",
                },
            }

    # Integrate map generation
    map_html_path = map.generate_map(location)
    if map_html_path:
        context["map_path"] = map_html_path
    else:
        context["map_path"] = None

    return context
