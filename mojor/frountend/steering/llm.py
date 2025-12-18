from pymongo import MongoClient
from langchain.prompts import PromptTemplate
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain.text_splitter import RecursiveCharacterTextSplitter

# MongoDB configuration
MONGO_URI = "mongodb://localhost:27017/"  # Update this to your MongoDB URI
DB_NAME = "news_db"
NEWS_COLLECTION = "disaster_news"
RESULT_COLLECTION = "results_final"

# Setup MongoDB collections
def setup_mongodb():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]

    # Check if the news collection exists
    if NEWS_COLLECTION not in db.list_collection_names():
        db.create_collection(NEWS_COLLECTION, capped=False)
        print(f"Collection {NEWS_COLLECTION} created.")
    else:
        print(f"Collection {NEWS_COLLECTION} already exists.")

    # Check if the results collection exists
    if RESULT_COLLECTION not in db.list_collection_names():
        db.create_collection(RESULT_COLLECTION, capped=False)
        print(f"Collection {RESULT_COLLECTION} created.")
    else:
        print(f"Collection {RESULT_COLLECTION} already exists.")
    
    print("MongoDB setup complete.")

# Initialize LLaMA model and prompts
llm = OllamaLLM(model="llama3.1")

# Initialize embedding model
embedding_model = OllamaEmbeddings(model="llama3.1")

# Define prompts
type_prompt = PromptTemplate(
    template="Identify the disaster type in the following text: anserwer in one precise word only and do not use '.' \nTitle: {title}\nDescription: {description}\nContent: {content} ",
    input_variables=["title", "description", "content"]
)
location_prompt = PromptTemplate(
    template="Identify the location of the disaster in the following text: anserwer in one precise word only and do not use '.' \nTitle: {title}\nDescription: {description}\nContent: {content}",
    input_variables=["title", "description", "content"]
)
details_prompt = PromptTemplate(
    template="In parahraphs without any headings give the details and casualties and precautions that could be taken in an event of \nTitle: {title} without saying any extra word from the following text : \nDescription: {description} \nContent: {content}",
    input_variables=["title", "description", "content"]
)

# New precise location prompt
precise_location_prompt = PromptTemplate(
    template="Identify the precise locations of the disaster from the following description: in case of multiple possible locations answer in the following format  'Jaipur', 'Dausa', 'Jhunjhunu', 'Sawai Madhopur', 'Sriganganagar' just give the main location in one word if precise location is not available without saying any extra word in the following text \nDescription: {description}", 
    input_variables=["description"]
)

# Initialize runnable chains
type_chain = type_prompt | llm
location_chain = location_prompt | llm
details_chain = details_prompt | llm
precise_location_chain = precise_location_prompt | llm  # New precise location chain

# Chunking and embedding function
def process_text_for_embedding(Title, Description, Content):
    # Combine title, description, and content for chunking
    full_text = f"Title: {Title}\nDescription: {Description}\nContent: {Content}"
    
    # Initialize text splitter with 1000-token chunks and 200-token overlap
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    text_chunks = text_splitter.split_text(full_text)
    
    embeddings = []
    for chunk in text_chunks:
        embedding = embedding_model.embed_query(chunk)  # Generate embedding using embed_query
        embeddings.append((chunk, embedding))
        
    return embeddings

# Process a single row from MongoDB and store results
def process_and_store_single_row(news_row):
    title = news_row.get("Title")
    description = news_row.get("Description")
    content = news_row.get("Content")
    news_id = str(news_row.get("_id"))

    # Generate embeddings for each chunk
    embeddings = process_text_for_embedding(title, description, content)
    
    # Use the first chunk for generating output; adapt as needed
    first_chunk = embeddings[0][0] if embeddings else ""
    
    # Prepare input dictionary
    input_data = {"title": title, "description": description, "content": first_chunk}
    
    # Generate outputs for each attribute using the first chunk text
    disaster_type = type_chain.invoke(input=input_data)
    location = location_chain.invoke(input=input_data)
    details = details_chain.invoke(input=input_data)

    # Generate precise location using the description
    precise_location_input = {"description": description}
    precise_location = precise_location_chain.invoke(input=precise_location_input)
    
    # Insert results into the results collection
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    result_collection = db[RESULT_COLLECTION]
    
    # Insert the result into the results collection
    result_collection.insert_one({
        "news_id": news_id,
        "type": disaster_type,
        "location": location,
        "precise_location": precise_location,
        "details": details
    })
    print(f"Processed and stored result for news ID: {news_id}")

# Fetch a single row from the MongoDB news collection
def fetch_single_news_row():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    news_collection = db[NEWS_COLLECTION]

    # Fetch one unprocessed row
    news_row = news_collection.find_one({"processed": {"$ne": True}})
    if news_row:
        # Mark it as processed to avoid reprocessing
        news_collection.update_one({"_id": news_row["_id"]}, {"$set": {"processed": True}})
    return news_row

# Main processing loop
def process_news():
    while True:
        news_row = fetch_single_news_row()
        if not news_row:
            print("No more unprocessed news rows.")
            break
        process_and_store_single_row(news_row)

# Execute setup and processing
if __name__ == "__main__":
    setup_mongodb()  # Setup MongoDB collections
    process_news()  # Process news articles
