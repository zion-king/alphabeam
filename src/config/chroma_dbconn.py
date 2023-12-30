import chromadb
from src.config import appconfig


async def chroma_dbconn():
   try:
        # initialize client, setting path to save data
        # db = chromadb.PersistentClient(path="./chroma_db")
        print("Connecting to Chroma database...")
        db = chromadb.HttpClient(host=appconfig.chroma_db_host, port=appconfig.chroma_db_port)
        return db
   except Exception as e:
        return {'statusCode': 400, 'status': 'Could not connect to chroma database'}