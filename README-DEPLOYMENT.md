# 🍽️ Restaurante Darío - Backend API

API del sistema de gestión del restaurante construida con FastAPI y MongoDB.

## 🚀 Despliegue en Producción

### **Backend (Railway/Render/Heroku):**

1. **Crear cuenta en tu plataforma preferida:**
   - [Railway](https://railway.app/) (Recomendado)
   - [Render](https://render.com/)
   - [Heroku](https://heroku.com/)

2. **Conectar tu repositorio GitHub**

3. **Configurar variables de entorno:**
   ```
   SECRET_KEY=tu-clave-secreta-super-fuerte-para-produccion
   DEBUG=False
   MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/dbname
   MONGO_DATABASE=restaurante_dario
   FRONTEND_URL=https://tu-frontend.vercel.app
   ```

4. **Comando de inicio:** `python -m uvicorn main:app --host 0.0.0.0 --port $PORT`

### **Frontend (Vercel/Netlify):**

1. **Configurar variable de entorno:**
   ```
   VITE_API_URL=https://tu-backend.railway.app
   ```

## 🛠️ Desarrollo Local

1. **Clonar repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/restaurante-backend.git
   cd restaurante-backend
   ```

2. **Crear entorno virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # o
   venv\Scripts\activate  # Windows
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno:**
   ```bash
   cp .env.example .env
   # Editar .env con tus valores
   ```

5. **Ejecutar servidor:**
   ```bash
   uvicorn main:app --reload
   ```

## 🎯 Características Implementadas

### 🔐 **Sistema de Autenticación**
- JWT con tokens de 1 hora
- Manejo automático de expiración
- Panel de administración protegido
- Verificación en tiempo real

### 🍽️ **Gestión de Contenido**
- ✅ Sistema completo de menú con MongoDB
- ✅ 19 categorías predefinidas
- ✅ 113+ items con precios y descripciones
- ✅ Gestión de imágenes con GridFS
- ✅ Sistema de búsqueda y filtros

### 📸 **Gestión de Imágenes**
- Subida de imágenes a GridFS
- URLs dinámicas de imágenes
- Gestión simplificada desde admin
- Soporte para categorías e items

## 📚 API Endpoints

### 🔑 Autenticación
- `POST /api/auth-mongo/login` - Iniciar sesión admin
- `GET /api/auth-mongo/profile` - Perfil de usuario

### 📋 Administración
- `GET /api/admin/categorias` - Listar categorías con conteo
- `POST /api/admin/categorias` - Crear categoría
- `PUT /api/admin/categorias/{id}` - Actualizar categoría
- `POST /api/admin/upload-image` - Subir imagen
- `GET /api/admin/restaurante` - Info del restaurante

### 🖼️ Imágenes
- `GET /api/imagenes/{id}` - Obtener imagen por ID

### 🍽️ Menú Público
- `GET /api/mongo/menu/menu-completo` - Menú completo
- `GET /api/mongo/menu/categorias` - Lista de categorías
- `GET /api/mongo/menu/items` - Items con filtros

## 📁 Estructura del Proyecto

```
restaurante-backend/
├── app/
│   ├── routers/           # Endpoints de la API
│   │   ├── admin.py      # Panel de administración
│   │   ├── auth_mongo.py # Autenticación MongoDB
│   │   ├── menu_mongo.py # Menú público
│   │   └── images.py     # Gestión de imágenes
│   ├── models/           # Modelos de datos
│   ├── schemas/          # Esquemas Pydantic
│   ├── services/         # Lógica de negocio
│   └── mongo_database.py # Configuración MongoDB
├── requirements.txt      # Dependencias Python
├── main.py              # Aplicación principal
├── .env.example         # Template de variables
├── Procfile             # Para Railway/Heroku
├── Dockerfile           # Para Docker (opcional)
└── README.md
```

## 🔧 Tecnologías

- **FastAPI** - Framework web moderno y rápido
- **MongoDB Atlas** - Base de datos NoSQL en la nube
- **GridFS** - Almacenamiento de imágenes
- **JWT** - Autenticación segura con tokens
- **Python 3.11+** - Lenguaje de programación
- **Pydantic** - Validación de datos
- **Motor** - Driver asíncrono para MongoDB

## 🔒 Seguridad

- ✅ Autenticación JWT con tokens de 1 hora
- ✅ CORS configurado para dominios específicos
- ✅ Variables de entorno para configuración sensible
- ✅ Hash de contraseñas con bcrypt
- ✅ Validación automática de requests
- ✅ Manejo de errores y timeouts

## 🚀 Instrucciones de Despliegue

### **Railway (Recomendado):**
1. Fork este repositorio
2. Conecta Railway a tu GitHub
3. Importa el proyecto
4. Configura las variables de entorno
5. ¡Listo! Railway detecta automáticamente FastAPI

### **Render:**
1. Conecta tu repositorio
2. Configura: `pip install -r requirements.txt && python -m uvicorn main:app --host 0.0.0.0 --port $PORT`
3. Configura variables de entorno
4. Deploy

### **Vercel (Solo si usas serverless):**
1. Instala: `npm i -g vercel`
2. `vercel --prod`
3. Configura variables en dashboard

## 🧪 Testing

```bash
# Verificar salud de la API
curl http://localhost:8000/health

# Probar autenticación
curl -X POST http://localhost:8000/api/auth-mongo/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}'

# Obtener menú completo
curl http://localhost:8000/api/mongo/menu/menu-completo
```

## 📞 Soporte

- **Documentación**: http://localhost:8000/docs
- **Estado del servicio**: http://localhost:8000/health
- **API Interactiva**: http://localhost:8000/redoc

---

✨ **Backend completamente funcional y listo para producción**