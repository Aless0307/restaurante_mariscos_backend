# 🔐 Credenciales de Administración - Restaurante Dario

## ✅ Usuario Creado Exitosamente

### 📋 Información de Acceso

| Campo | Valor |
|-------|-------|
| **Email** | `restaurantedario@restaurante.com` |
| **Usuario** | `restaurantedario` |
| **Contraseña** | `Dario6219$` |
| **Nombre** | Restaurante Dario |
| **Permisos** | ✅ Administrador |
| **Estado** | ✅ Activo |
| **ID MongoDB** | `692f9b4a9786046096423556` |

---

## 🌐 Cómo Iniciar Sesión

### Opción 1: Usar el Email
```
Email: restaurantedario@restaurante.com
Contraseña: Dario6219$
```

### Opción 2: Usar el Usuario
```
Usuario: restaurantedario
Contraseña: Dario6219$
```

---

## 🔗 URLs de Acceso

### Panel de Administración (Frontend)
```
http://localhost:5173
```

### API Backend
```
http://localhost:8000
```

### Endpoint de Login
```
POST http://localhost:8000/api/auth-mongo/login
Body: {
  "username": "restaurantedario",
  "password": "Dario6219$"
}
```

---

## 🧪 Probar Login con cURL

```bash
# Login con username
curl -X POST http://localhost:8000/api/auth-mongo/login \
  -H "Content-Type: application/json" \
  -d '{"username":"restaurantedario","password":"Dario6219$"}'

# Login con email  
curl -X POST http://localhost:8000/api/auth-mongo/login \
  -H "Content-Type: application/json" \
  -d '{"username":"restaurantedario@restaurante.com","password":"Dario6219$"}'
```

---

## 📝 Notas Importantes

⚠️ **Seguridad:**
- Esta contraseña está hasheada con bcrypt en la base de datos
- El hash almacenado: `$2b$12$LCbpX6XqJpUYq8uzfXS5OOz...`
- **NUNCA** compartas este archivo en repositorios públicos

⚠️ **Backup:**
- Guarda estas credenciales en un lugar seguro
- Considera cambiar la contraseña después del primer login

⚠️ **Usuarios Existentes:**
- Este usuario fue creado el: **2 de diciembre de 2025**
- Otros usuarios admin pueden existir en la base de datos

---

## 🔄 Actualizar Credenciales

Si necesitas cambiar la contraseña, ejecuta:

```bash
/home/alessandro-hp/mi_entorno/bin/python crear_usuario_restaurantedario_bcrypt.py
```

El script detectará que el usuario existe y te preguntará si deseas actualizar la contraseña.

---

## 🗄️ Información en Base de Datos

### Colección: `usuarios`
```javascript
{
  "_id": ObjectId("692f9b4a9786046096423556"),
  "nombre": "Restaurante Dario",
  "email": "restaurantedario@restaurante.com",
  "telefono": "2291096048",
  "password_hash": "$2b$12$LCbpX6XqJpUYq8uzfXS5OO...",
  "es_admin": true,
  "fecha_registro": ISODate("2025-12-02T..."),
  "activo": true
}
```

---

## ✅ Verificación

Para verificar que el usuario fue creado correctamente:

### 1. Verificar en MongoDB
```bash
mongosh "mongodb+srv://alessandroah77:alessandro2003@clustermarisco.uuco735.mongodb.net/restaurante_dario"

# En el shell de MongoDB:
db.usuarios.find({email: "restaurantedario@restaurante.com"})
```

### 2. Verificar con la API
```bash
# Login
curl -X POST http://localhost:8000/api/auth-mongo/login \
  -H "Content-Type: application/json" \
  -d '{"username":"restaurantedario","password":"Dario6219$"}'

# Deberías recibir un access_token si es exitoso
```

### 3. Verificar en el Frontend
1. Ve a `http://localhost:5173`
2. Haz clic en "Iniciar Sesión"
3. Usa las credenciales de arriba
4. Deberías acceder al panel de administración

---

**Creado el:** 2 de diciembre de 2025  
**Script utilizado:** `crear_usuario_restaurantedario_bcrypt.py`  
**Estado:** ✅ Activo y funcional
