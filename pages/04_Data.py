
# Path: pages/data.py
import streamlit as st
from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer


encoder = SentenceTransformer('all-MiniLM-L6-v2')

documents = [
  { "name": "The Time Machine", "description": "A man travels through time and witnesses the evolution of humanity.", "author": "H.G. Wells", "year": 1895 },
  { "name": "Ender's Game", "description": "A young boy is trained to become a military leader in a war against an alien race.", "author": "Orson Scott Card", "year": 1985 },
  { "name": "Brave New World", "description": "A dystopian society where people are genetically engineered and conditioned to conform to a strict social hierarchy.", "author": "Aldous Huxley", "year": 1932 },
  { "name": "The Hitchhiker's Guide to the Galaxy", "description": "A comedic science fiction series following the misadventures of an unwitting human and his alien friend.", "author": "Douglas Adams", "year": 1979 },
  { "name": "Dune", "description": "A desert planet is the site of political intrigue and power struggles.", "author": "Frank Herbert", "year": 1965 },
  { "name": "Foundation", "description": "A mathematician develops a science to predict the future of humanity and works to save civilization from collapse.", "author": "Isaac Asimov", "year": 1951 },
  { "name": "Snow Crash", "description": "A futuristic world where the internet has evolved into a virtual reality metaverse.", "author": "Neal Stephenson", "year": 1992 },
  { "name": "Neuromancer", "description": "A hacker is hired to pull off a near-impossible hack and gets pulled into a web of intrigue.", "author": "William Gibson", "year": 1984 },
  { "name": "The War of the Worlds", "description": "A Martian invasion of Earth throws humanity into chaos.", "author": "H.G. Wells", "year": 1898 },
  { "name": "The Hunger Games", "description": "A dystopian society where teenagers are forced to fight to the death in a televised spectacle.", "author": "Suzanne Collins", "year": 2008 },
  { "name": "The Andromeda Strain", "description": "A deadly virus from outer space threatens to wipe out humanity.", "author": "Michael Crichton", "year": 1969 },
  { "name": "The Left Hand of Darkness", "description": "A human ambassador is sent to a planet where the inhabitants are genderless and can change gender at will.", "author": "Ursula K. Le Guin", "year": 1969 },
  { "name": "The Time Traveler's Wife", "description": "A love story between a man who involuntarily time travels and the woman he loves.", "author": "Audrey Niffenegger", "year": 2003 }
]


#client = QdrantClient(":memory:")
# or
#client = QdrantClient(path="path/to/db")  # Persists changes to disk
#st.write(os.path.dirname())

#client = QdrantClient(host="localhost", port=6333)

client = QdrantClient(
    url=st.secrets["QDRANT_SERVER"], 
    api_key=st.secrets["QDRANT_KEY"],
)


response = client.get_collections()

if response is not None:
    print(response.collections)
    collections = response.collections
    st.write("Collections: ", collections)
    # if collections contains my_books collection
    
    col = [collection for collection in collections if collection.name == "my_books"]
    
    print(col)
    if col is not None:
        st.write("my_books collection exists")
        # collection = client.get_collection("my_books")
        
    else:
        st.write("my_books collection does not exist")
        
        # Create collection to store books
        # if collection is None:
        client.recreate_collection(
                collection_name="my_books",
                vectors_config=models.VectorParams(
                    size=encoder.get_sentence_embedding_dimension(), # Vector size is defined by used model
                    distance=models.Distance.COSINE
                )
            )

            # Let's vectorize descriptions and upload to qdrant

        client.upload_records(
                collection_name="my_books",
                records=[
                    models.Record(
                        id=idx,
                        vector=encoder.encode(doc["description"]).tolist(),
                        payload=doc
                    ) for idx, doc in enumerate(documents)
                ]
            )


    




def app():
    st.title("Data")
    st.write("This is the data page of the multi-page app.")

st.title("Data with Qdrant")


searchTerm = st.text_input("Search")


isSearch = False

if st.button("Search"):
   if (searchTerm != ""):
        # st.write("Searching for: ", searchTerm)
        hits = client.search(
            collection_name="my_books",
            query_vector=encoder.encode(searchTerm).tolist(),
            limit=3
            )
        print(hits)
        isSearch = True
   else:
       st.write("input a search term first")


if (isSearch == True):
    st.write("Search Results")
    for hit in hits:
        st.write(hit.payload, "score:", hit.score)