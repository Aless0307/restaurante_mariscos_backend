from pymongo import MongoClient
import gridfs
import os
from dotenv import load_dotenv
from typing import Optional
from bson import ObjectId

load_dotenv()

# Configuración de MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://alessandroah77:alessandro2003@clustermarisco.uuco735.mongodb.net/")
DATABASE_NAME = os.getenv("MONGO_DATABASE", "restaurante_dario")

class MongoDB:
    _instance = None
    _client = None
    _db = None
    _fs = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDB, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._client is None:
            self._client = MongoClient(MONGO_URI)
            self._db = self._client[DATABASE_NAME]
            self._fs = gridfs.GridFS(self._db)
    
    @property
    def client(self):
        return self._client
    
    @property
    def db(self):
        return self._db
    
    @property
    def fs(self):
        return self._fs
    
    def close(self):
        if self._client:
            self._client.close()

# Instancia global de MongoDB
mongodb = MongoDB()

# Función para convertir ObjectId a string en documentos
def serialize_doc(doc):
    """Convierte ObjectId a string en documentos de MongoDB"""
    if doc is None:
        return None
    
    if isinstance(doc, list):
        return [serialize_doc(item) for item in doc]
    
    if isinstance(doc, dict):
        serialized = {}
        for key, value in doc.items():
            if isinstance(value, ObjectId):
                serialized[key] = str(value)
            elif isinstance(value, dict):
                serialized[key] = serialize_doc(value)
            elif isinstance(value, list):
                serialized[key] = serialize_doc(value)
            else:
                serialized[key] = value
        return serialized
    
    return doc

# Dependencia para obtener la base de datos
def get_mongodb():
    return mongodb.db

# Alias para compatibilidad
def get_mongo_db():
    return mongodb.db