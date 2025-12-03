# 🔄 Endpoint de Reordenamiento de Items - Drag & Drop

## 📋 Descripción

Endpoint para actualizar el orden de los platillos en una categoría mediante drag & drop desde el panel de administración.

## 🎯 Endpoint

```
PUT /api/admin/categorias/{categoria_id}/reordenar-items
```

## 🔐 Autenticación

Requiere token de administrador en el header:
```
Authorization: Bearer {token}
```

## 📥 Request

### URL Parameters
- `categoria_id` (string, required): ID de la categoría cuyos items se van a reordenar

### Body (JSON)
```json
{
  "items": ["nombre_item_1", "nombre_item_2", "nombre_item_3", ...]
}
```

**Campos:**
- `items` (array de strings, required): Array con los nombres de los items en el nuevo orden

### Ejemplo de Request
```bash
curl -X PUT http://localhost:8000/api/admin/categorias/68e1a2eebeba702d9b740f4b/reordenar-items \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbG..." \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      "Barbacoa de Res",
      "Barbacoa a la Mexicana",
      "Birria de Res",
      "Arrachera",
      "Costillas BBQ"
    ]
  }'
```

## 📤 Response

### Success (200 OK)
```json
{
  "status": "success",
  "message": "Orden de items actualizado exitosamente",
  "items_actualizados": 5,
  "categoria": "CARNES"
}
```

### Error - Categoría no encontrada (404)
```json
{
  "detail": "Categoría no encontrada"
}
```

### Error - Body inválido (400)
```json
{
  "detail": "Se requiere un array de nombres de items"
}
```

### Error - No autenticado (401)
```json
{
  "detail": "No autenticado"
}
```

### Error - No es admin (403)
```json
{
  "detail": "No tiene permisos de administrador"
}
```

## 🔧 Funcionamiento Interno

### 1. Validación
- Verifica que la categoría existe
- Valida que el body contiene un array de items
- Verifica autenticación y permisos de admin

### 2. Actualización en `items_menu` (Colección)
- Itera sobre el array de nombres
- Para cada item, actualiza el campo `orden` con su índice
- Solo actualiza items que pertenecen a la categoría

### 3. Actualización en `categorias_menu.items` (Array Embebido)
- Si la categoría tiene items en el array embebido
- Reordena el array según el nuevo orden
- Actualiza el campo `orden` en cada item del array

### 4. Cache
- Limpia el caché del menú para reflejar cambios inmediatamente

## 💾 Estructura de Datos

### Antes del Reordenamiento
```javascript
// En items_menu
[
  { nombre: "Barbacoa de Res", orden: 0, categoria_id: "..." },
  { nombre: "Birria de Res", orden: 1, categoria_id: "..." },
  { nombre: "Arrachera", orden: 2, categoria_id: "..." }
]
```

### Después del Reordenamiento
```javascript
// Nuevo orden: ["Arrachera", "Barbacoa de Res", "Birria de Res"]

// En items_menu
[
  { nombre: "Arrachera", orden: 0, categoria_id: "..." },
  { nombre: "Barbacoa de Res", orden: 1, categoria_id: "..." },
  { nombre: "Birria de Res", orden: 2, categoria_id: "..." }
]
```

## 🎨 Integración Frontend

### Ejemplo con Fetch API
```javascript
async function reordenarItems(categoriaId, nuevosNombres) {
  const response = await fetch(
    `http://localhost:8000/api/admin/categorias/${categoriaId}/reordenar-items`,
    {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ items: nuevosNombres })
    }
  );
  
  if (!response.ok) {
    throw new Error('Error al reordenar items');
  }
  
  return await response.json();
}

// Uso
const nuevosNombres = ["Item 3", "Item 1", "Item 2"];
const resultado = await reordenarItems("68e1a2ee...", nuevosNombres);
console.log(resultado.message); // "Orden de items actualizado exitosamente"
```

### Ejemplo con @dnd-kit (React)
```jsx
import { DndContext } from '@dnd-kit/core';
import { SortableContext, arrayMove } from '@dnd-kit/sortable';

function handleDragEnd(event) {
  const { active, over } = event;
  
  if (active.id !== over.id) {
    const oldIndex = items.findIndex(i => i.nombre === active.id);
    const newIndex = items.findIndex(i => i.nombre === over.id);
    
    // Reordenar localmente
    const reordenados = arrayMove(items, oldIndex, newIndex);
    setItems(reordenados);
    
    // Enviar al backend
    const nuevosNombres = reordenados.map(item => item.nombre);
    await reordenarItems(categoriaId, nuevosNombres);
  }
}
```

## 🧪 Testing

### Prueba Manual con cURL
```bash
# 1. Login
TOKEN=$(curl -X POST http://localhost:8000/api/auth-mongo/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"tu_password"}' \
  | jq -r '.access_token')

# 2. Reordenar items
curl -X PUT http://localhost:8000/api/admin/categorias/CATEGORIA_ID/reordenar-items \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"items":["Item C","Item A","Item B"]}'
```

### Prueba con Python
```python
import requests

# Login
response = requests.post('http://localhost:8000/api/auth-mongo/login', 
                        json={'username': 'admin', 'password': 'password'})
token = response.json()['access_token']

# Reordenar
headers = {'Authorization': f'Bearer {token}'}
data = {'items': ['Camarones al Coco', 'Camarones a la Diabla', 'Camarones Empanizados']}
response = requests.put(
    'http://localhost:8000/api/admin/categorias/CATEGORIA_ID/reordenar-items',
    json=data,
    headers=headers
)
print(response.json())
```

## 📊 Logs de Debug

El endpoint genera logs detallados para debugging:

```
🔄 DEBUG: Reordenando 5 items en categoría 'CARNES'
📝 DEBUG: Nuevo orden: ['Barbacoa de Res', 'Barbacoa a la Mexicana', ...]
✅ DEBUG: 5 items actualizados en colección items_menu
✅ DEBUG: Array embebido actualizado con 5 items
🗑️ Caché del menú limpiado completamente
🎉 DEBUG: Reordenamiento completado exitosamente
```

## ⚠️ Consideraciones

### Importante
- El array `items` debe contener **nombres exactos** de los items
- Los nombres deben coincidir con los que existen en la base de datos
- Si un nombre no existe, simplemente se omite (no genera error)
- El orden se guarda mediante el campo `orden` (índice numérico)

### Performance
- Operación optimizada para arrays de hasta 100 items
- Usa update individual para cada item (no batch)
- Cache se limpia automáticamente después del reordenamiento

### Seguridad
- Requiere autenticación de administrador
- Valida que la categoría existe
- Valida formato del body

## 🔗 Endpoints Relacionados

- `GET /api/admin/categorias` - Listar categorías con items
- `PUT /api/admin/categorias/{id}/items/{nombre}` - Actualizar item individual
- `DELETE /api/admin/categorias/{id}/items/{nombre}` - Eliminar item
- `POST /api/admin/categorias/{id}/items` - Crear nuevo item

## 📝 Changelog

### v1.0.0 (2025-12-02)
- ✅ Implementación inicial del endpoint
- ✅ Soporte para actualización en colección y array embebido
- ✅ Limpieza automática de caché
- ✅ Logs detallados para debugging
