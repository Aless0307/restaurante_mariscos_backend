# API del Restaurante Dario - Backend Completo

Backend desarrollado con **FastAPI** que integra **MongoDB Atlas** para el sistema completo de gestión del restaurante.

## 🎯 Características Implementadas

### � **Doble Sistema de Base de Datos**
- **SQLite**: Para usuarios, reservas y autenticación (desarrollo local)
- **MongoDB Atlas**: Para todo el contenido dinámico del restaurante (producción)

### 🍽️ **Contenido Dinámico en MongoDB**
- ✅ **19 Categorías** completas del menú
- ✅ **113 Items** con precios y descripciones
- ✅ **Información del restaurante** (contacto, horarios, etc.)
- ✅ **Características y servicios**
- ✅ **Imágenes** almacenadas con GridFS
- ✅ **Sistema de búsqueda** en tiempo real

### 🚀 **APIs Disponibles**

#### **Rutas MongoDB (Contenido Dinámico)**
```
GET /api/mongo/menu/menu-completo     # Menú completo con categorías e items
GET /api/mongo/menu/categorias        # Todas las categorías
GET /api/mongo/menu/items             # Items con filtros (categoría, búsqueda)
GET /api/restaurante/info             # Información general
GET /api/restaurante/contacto         # Datos de contacto
GET /api/restaurante/caracteristicas  # Características del restaurante
GET /api/restaurante/servicios        # Servicios ofrecidos
```

#### **Rutas SQLite (Sistema de Gestión)**
```
POST /api/auth/register               # Registro de usuarios
POST /api/auth/login                  # Autenticación
GET /api/auth/profile                 # Perfil de usuario
POST /api/reservas/                   # Crear reserva
GET /api/reservas/                    # Listar reservas (admin)
```

## 📊 **Datos Almacenados en MongoDB**

### **Categorías del Menú (19)**
- CARNES, MARISCOS, CAMARONES, FILETES, PESCADOS
- ENTRADAS, CÓCTELES, CALDOS Y CONSOMÉS, PULPOS
- BEBIDAS, CERVEZA, REFRESCOS, LICORES, BEBIDAS MEXICANAS
- ENSALADAS, POSTRES, ANTOJITOS, EXTRAS, HUEVA DE LISA

### **Funcionalidades de Búsqueda**
- Filtrar por categoría
- Búsqueda por nombre de platillo
- Filtrar por disponibilidad
- Ordenamiento personalizado

### **Información del Restaurante**
- Datos de contacto (teléfono, WhatsApp, email)
- Dirección y ubicación
- Horarios de atención
- Características y servicios

## 🛠️ **Instalación y Configuración**

### **1. Instalar Dependencias**
```bash
pip install -r requirements.txt
```

### **2. Configurar Variables de Entorno (.env)**
```env
# SQLite (desarrollo)
DATABASE_URL=sqlite:///./restaurante.db
SECRET_KEY=tu-clave-secreta

# MongoDB Atlas (producción)
MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/
MONGO_DATABASE=restaurante_dario
```

### **3. Cargar Datos Iniciales**
```bash
# Cargar datos del restaurante en MongoDB
python cargar_datos_mongo.py

# O usar el script de prueba simplificado
python test_mongo_conexion.py
```

### **4. Ejecutar Servidor**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 🌐 **URLs de Acceso**

- **Documentación API**: http://localhost:8000/docs
- **API Alternativa**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **Menú Completo**: http://localhost:8000/api/mongo/menu/menu-completo

## 🔧 **Pruebas de la API**

Ejecutar script de pruebas:
```bash
python probar_api.py
```

## 📁 **Estructura del Proyecto**

```
restaurante-backend/
├── app/
│   ├── models/              # Modelos SQLAlchemy (usuarios, reservas)
│   ├── routers/
│   │   ├── auth.py         # Autenticación (SQLite)
│   │   ├── reservas.py     # Reservas (SQLite)
│   │   ├── menu_mongo.py   # Menú (MongoDB) ⭐
│   │   └── restaurante.py  # Info restaurante (MongoDB) ⭐
│   ├── schemas/
│   │   ├── schemas.py      # Esquemas SQLite
│   │   └── mongo_schemas.py # Esquemas MongoDB ⭐
│   ├── services/
│   │   └── auth_service.py # Servicios de autenticación
│   ├── database.py         # Configuración SQLite
│   └── mongo_database.py   # Configuración MongoDB ⭐
├── main.py                 # Aplicación principal
├── cargar_datos_mongo.py   # Script carga completa ⭐
├── test_mongo_conexion.py  # Script prueba conexión ⭐
├── probar_api.py          # Script pruebas API ⭐
└── requirements.txt        # Dependencias
```

## 🎯 **Ventajas del Sistema Actual**

### **Para el Cliente/Frontend**
- ✅ **Contenido dinámico**: Menú actualizable sin redeployar
- ✅ **Búsquedas rápidas**: Filtros en tiempo real
- ✅ **Imágenes optimizadas**: GridFS para manejo eficiente
- ✅ **Datos siempre actualizados**: Conexión directa a MongoDB

### **Para el Administrador**
- ✅ **Gestión centralizada**: Todo en MongoDB Atlas
- ✅ **Escalabilidad**: MongoDB maneja grandes volúmenes
- ✅ **Backup automático**: Atlas incluye respaldos
- ✅ **Panel de administración**: Futuro desarrollo con roles admin

### **Para el Desarrollador**
- ✅ **APIs RESTful**: Documentación automática
- ✅ **Separación de responsabilidades**: SQLite para gestión, MongoDB para contenido
- ✅ **Validación automática**: Pydantic schemas
- ✅ **Código escalable**: Estructura modular

## 🚀 **Próximos Pasos**

1. **Panel de Administración**
   - Crear rutas protegidas para admin
   - CRUD completo de categorías e items
   - Subida de imágenes vía API

2. **Optimizaciones**
   - Cache con Redis
   - Paginación en listados grandes
   - Compresión de imágenes

3. **Funcionalidades Avanzadas**
   - Sistema de inventario
   - Analíticas de ventas
   - Notificaciones en tiempo real

## 📞 **Soporte**

- **Documentación**: http://localhost:8000/docs
- **Estado del servicio**: http://localhost:8000/health
- **Logs**: Revisa la consola del servidor

---

✨ **El backend está completamente funcional y listo para conectar con el frontend React.**