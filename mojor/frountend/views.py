from django.shortcuts import render
from pymongo import MongoClient
from frountend.steering import steering
from django.shortcuts import render, get_object_or_404

# MongoDB configuraton
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "news_db"
RESULT_COLLECTION = "results_final"
CONTACT = "contacts"

def disaster_news(request):
    # Handle POST request data
    if request.method == "POST":
        disaster_type = request.POST.get('disaster_type', None)
        location = request.POST.get('location', None)

        if disaster_type and location:
            # Process request using steering.py
            result = steering.process_disaster_request(disaster_type, location)
            # Pass the result to the template
            context = {
                    "disaster": result.get("disaster", {}),
                }
        else:
            context = {
                "disaster": {
                    "location":"No disaster selected",
                    "title": "No disaster selected",
                    "details": "Please provide a disaster type and location to view the results.",
                    },
                }

        return render(request, "disaster.html", context)

    return render(request, "index.html")  # Redirect to index if accessed via GET

def index(request):
    """
    Render the homepage with the main disaster news and recent disasters.
    """
    # Connect to the MongoDB
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[RESULT_COLLECTION]

    # Fetch the main news (top-most entry in the database)
    main_disaster = collection.find_one({}, {"_id": 0, "type": 1,"location":1, "details": 1})

    # Fetch the next three entries as recent disasters
    recent_disasters = list(
        collection.find({}, {"_id": 0, "type": 1, "location": 1}).skip(1).limit(3)
    )

    # Pass the data to the template context
    context = {
        "main_disaster": main_disaster if main_disaster else {
            "type": "No News Available",
            "location":"",
            "details": "No main disaster news is currently available.",
        },
        "recent_disasters": recent_disasters if recent_disasters else [],
    }

    return render(request, 'index.html', context)

def map(request):
    return render(request, 'maps/map.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def disasterlist(request):
    # Connect to the MongoDB
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[RESULT_COLLECTION]
    
    # Fetch all disasters
    disasters = list(collection.find({}, {"_id": 0, "type": 1, "location": 1}))
    
    # Pass the data to the template context
    context = { "disasters": disasters if disasters else [],}

    return render(request, 'disasterlist.html', context)


def disaster_detail(request):
    disaster_type = request.GET.get('disaster_type')
    disaster_location = request.GET.get('disaster_location')

    # Connect to the MongoDB
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[RESULT_COLLECTION]

    # Fetch the disaster details from the database
    disaster = collection.find_one({
        'type': disaster_type,
        'location': disaster_location
    })
    steering.process_disaster_request(disaster_type, disaster_location)


    # Pass disaster data to the template
    context = {
        'disaster': disaster
    }

    return render(request, 'disasterdetail.html', context)

def contact_us(request):
    if request.method == "POST":
        # Fetch form data
        name = request.POST.get("name")
        email = request.POST.get("email")
        query = request.POST.get("query")

        # Connect to MongoDB
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[CONTACT]

        # Insert data into MongoDB
        collection.insert_one({
            "name": name,
            "email": email,
            "query": query,
        })

        # Redirect or show success message
        return render(request, "contact_success.html", {"name": name})
    
    return render(request, "contact.html")