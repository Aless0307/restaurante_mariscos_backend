# 🔧 IMPORTANTE: Reiniciar el Servidor

## ⚠️ El servidor necesita reiniciarse

He hecho cambios en el código de autenticación para que funcione con bcrypt (que es como se guardó la contraseña).

## 📝 Pasos para Aplicar los Cambios:

### 1. Detener el servidor actual
```bash
# En la terminal donde está corriendo uvicorn, presiona:
Ctrl + C
```

### 2. Iniciar el servidor nuevamente
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Probar el login
```bash
curl -X POST http://localhost:8000/api/auth-mongo/login \
  -H "Content-Type: application/json" \
  -d '{"username":"restaurantedario","password":"Dario6219$"}'
```

Deberías recibir:
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

## 🔧 Cambios Realizados

1. ✅ Cambiado de `auth_mongo_simple` (SHA256) a `auth_mongo_service` (bcrypt)
2. ✅ Agregado soporte para verificación directa con bcrypt
3. ✅ Mantenida compatibilidad con hashes antiguos
4. ✅ Login ahora acepta username o email

## 🧪 Después de Reiniciar

El login funcionará con:
- **Username:** `restaurantedario`
- **Email:** `restaurantedario@restaurante.com`
- **Contraseña:** `Dario6219$`

---

**REINICIA EL SERVIDOR AHORA** ⚡
