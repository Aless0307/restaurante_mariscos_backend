# ✅ Cambios Realizados: Login con Username

## 🎯 Problema Resuelto

El formulario de login pedía "email" pero el usuario quería ingresar con "restaurantedario" (username). Esto causaba que la validación fallara.

## 🔧 Cambios Implementados

### 1. Schema de Login (`auth_schemas.py`)

**Antes:**
```python
class UsuarioMongoLogin(BaseModel):
    email: EmailStr  # Solo aceptaba email válido
    password: str
```

**Después:**
```python
class UsuarioMongoLogin(BaseModel):
    username: str  # Acepta email o username
    password: str
```

### 2. Endpoint de Login (`auth_mongo.py`)

**Antes:**
- Solo buscaba por email exacto
- `user = db.usuarios.find_one({"email": user_credentials.email})`

**Después:**
- Busca primero por email completo
- Si no encuentra, busca extrayendo el username del email (parte antes del @)
- Ejemplo: "restaurantedario@restaurante.com" → username "restaurantedario"

```python
# Buscar por email completo
user = db.usuarios.find_one({"email": user_credentials.username})

# Si no encuentra, buscar por username (parte antes del @)
if not user:
    user = db.usuarios.find_one({
        "$expr": {
            "$eq": [
                {"$toLower": {"$arrayElemAt": [{"$split": ["$email", "@"]}, 0]}},
                {"$toLower": user_credentials.username}
            ]
        }
    })
```

## ✅ Comportamiento Actual

### Ahora puedes hacer login con:

#### Opción 1: Username
```json
{
  "username": "restaurantedario",
  "password": "Dario6219$"
}
```
✅ **Funciona** - Extrae "restaurantedario" del email y compara

#### Opción 2: Email completo
```json
{
  "username": "restaurantedario@restaurante.com",
  "password": "Dario6219$"
}
```
✅ **Funciona** - Busca directamente por email

## 🎨 Cambios Necesarios en el Frontend

### Actualizar el label del input

**Antes:**
```jsx
<input 
  type="email" 
  placeholder="Email"
  ...
/>
```

**Después:**
```jsx
<input 
  type="text"  // Cambiar de "email" a "text"
  placeholder="Usuario o Email"  // Cambiar el placeholder
  ...
/>
```

### Actualizar el body del request

**Antes:**
```javascript
{
  email: formData.email,  // Campo "email"
  password: formData.password
}
```

**Después:**
```javascript
{
  username: formData.username,  // Campo "username"
  password: formData.password
}
```

## 🧪 Testing

### Probar con cURL

```bash
# Con username
curl -X POST http://localhost:8000/api/auth-mongo/login \
  -H "Content-Type: application/json" \
  -d '{"username":"restaurantedario","password":"Dario6219$"}'

# Con email completo
curl -X POST http://localhost:8000/api/auth-mongo/login \
  -H "Content-Type: application/json" \
  -d '{"username":"restaurantedario@restaurante.com","password":"Dario6219$"}'
```

### Probar con el script Python

```bash
/home/alessandro-hp/mi_entorno/bin/python test_login_username.py
```

## 📋 Checklist Frontend

Para que funcione completamente en el frontend:

- [ ] Cambiar `type="email"` a `type="text"` en el input
- [ ] Cambiar placeholder de "Email" a "Usuario o Email"
- [ ] Cambiar el nombre del campo de `email` a `username` en el request
- [ ] Remover validación de formato email (si existe)
- [ ] Actualizar mensajes de error para reflejar "usuario o email"

## 🔍 Ejemplo de Código Frontend

### React/TypeScript
```typescript
// Formulario de login
interface LoginForm {
  username: string;  // Cambiar de "email" a "username"
  password: string;
}

// Input
<input
  type="text"  // Cambiar de "email" a "text"
  name="username"  // Cambiar de "email" a "username"
  placeholder="Usuario o Email"
  value={formData.username}
  onChange={(e) => setFormData({...formData, username: e.target.value})}
/>

// Request
const response = await fetch('/api/auth-mongo/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: formData.username,  // Campo "username"
    password: formData.password
  })
});
```

## ✅ Estado Actual

- ✅ Backend actualizado y funcionando
- ✅ Acepta username ("restaurantedario")
- ✅ Acepta email completo ("restaurantedario@restaurante.com")
- ✅ Validación case-insensitive
- ⏳ Pendiente: Actualizar frontend

---

**Fecha:** 2 de diciembre de 2025  
**Archivos modificados:**
- `app/schemas/auth_schemas.py`
- `app/routers/auth_mongo.py`
