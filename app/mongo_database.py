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
    
    def _ensure_connected(self):
        """Asegurar que la conexión esté establecida (lazy connection)"""
        if self._client is None:
            # Configuración optimizada de MongoDB con connection pooling y timeouts
            self._client = MongoClient(
                MONGO_URI,
                maxPoolSize=50,  # Máximo de conexiones en el pool
                minPoolSize=10,  # Mínimo de conexiones siempre abiertas
                maxIdleTimeMS=45000,  # Tiempo máximo de inactividad
                serverSelectionTimeoutMS=10000,  # Timeout para seleccionar servidor (10s)
                connectTimeoutMS=10000,  # Timeout para conectar (10s)
                socketTimeoutMS=20000,  # Timeout para operaciones (20s)
                retryWrites=True,  # Reintentar escrituras automáticamente
                retryReads=True,  # Reintentar lecturas automáticamente
                # Permitir lecturas desde secundarios para mejor disponibilidad
                readPreference='secondaryPreferred',
                # Concern de escritura para mejor rendimiento
                w='majority',
                wtimeoutMS=10000,
            )
            self._db = self._client[DATABASE_NAME]
            self._fs = gridfs.GridFS(self._db)
    
    @property
    def client(self):
        self._ensure_connected()
        return self._client
    
    @property
    def db(self):
        self._ensure_connected()
        return self._db
    
    @property
    def fs(self):
        self._ensure_connected()
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