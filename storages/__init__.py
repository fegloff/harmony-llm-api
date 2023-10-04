from .chromadb_storage import ChromaStorage
import chromadb.config

_client_settings = chromadb.config.Settings(
    persist_directory= "./chroma",
    is_persistent= True
)

chromadb = ChromaStorage(_client_settings)
