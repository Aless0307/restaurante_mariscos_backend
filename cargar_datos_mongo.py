from pymongo import MongoClient
import gridfs
import os
import requests
from urllib.parse import urlparse
import json
from datetime import datetime

# ----------------------------------------------------------------------
# ⚠️ VARIABLES A EDITAR
# ----------------------------------------------------------------------

# Ruta donde se descargarán las imágenes temporalmente
TEMP_IMAGES_DIR = "/home/alessandro-hp/Documentos/IngSoftAvanzada/temp_images"

# Cadena de conexión de MongoDB
MONGO_URI = "mongodb+srv://alessandroah77:alessandro2003@clustermarisco.uuco735.mongodb.net/?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"

# Nombre de la base de datos donde se guardará todo
DATABASE_NAME = "restaurante_dario"

# ----------------------------------------------------------------------
# DATOS DEL RESTAURANTE EXTRAÍDOS DEL FRONTEND
# ----------------------------------------------------------------------

# Información general del restaurante
restaurante_info = {
    "nombre": "Dario Restaurante",
    "descripcion_corta": "Los mariscos más frescos del mar, preparados con pasión y tradición desde 1969",
    "descripcion_larga": "En Dario Restaurante, llevamos más de dos décadas dedicados a ofrecer la mejor experiencia gastronómica de mariscos. Nuestra pasión por los productos del mar nos ha convertido en el destino favorito para los amantes de los mariscos frescos.",
    "año_fundacion": 1969,
    "años_experiencia": 20,
    "clientes_satisfechos": 10000,
    "platos_unicos": 50,
    "capacidad_personas": 150,
    "slogan": "Mariscos frescos seleccionados diariamente",
    "logo_url": "figma:asset/9e3fb91044d97a7f4be76c9eab3f4e7c4e7a4aa8.png"
}

# Información de contacto
contacto_info = {
    "telefono": "+52 229 109 6048",
    "whatsapp": "522291096048",
    "email": "restaurantedario1@outlook.com",
    "direccion": {
        "calle": "Carr. Veracruz - Medellin km 2.5",
        "codigo_postal": "91966",
        "ciudad": "Veracruz",
        "estado": "Ver.",
        "pais": "México"
    },
    "horarios": {
        "todos_los_dias": "9:00 AM - 6:00 PM"
    },
    "maps_embed": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3763.8886!2d-96.1644!3d19.2065!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x85c35afbf3b63a5d%3A0x5a4f7e0e1b8c9d3a!2sCarr.+Veracruz+-+Medell%C3%ADn%2C+Veracruz%2C+Ver.%2C+M%C3%A9xico!5e0!3m2!1ses!2smx!4v1234567890123"
}

# Categorías del menú con sus datos completos
menu_categorias = [
    {
        "nombre": "CARNES",
        "color": "bg-red-600",
        "imagen_url": "https://images.unsplash.com/photo-1693422662674-591afed861d7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxncmlsbGVkJTIwbWVhdCUyMHN0ZWFrfGVufDF8fHx8MTc1ODIwMjU3M3ww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral",
        "icono": "🥩",
        "orden": 1,
        "activo": True,
        "items": [
            {"nombre": "Barbacoa de Res", "precio": 110, "descripcion": "", "disponible": True},
            {"nombre": "Barbacoa a la Mexicana", "precio": 130, "descripcion": "", "disponible": True},
            {"nombre": "Asamblea", "precio": 180, "descripcion": "", "disponible": True},
            {"nombre": "Carne Asada o Enchipotlada", "precio": 180, "descripcion": "", "disponible": True},
            {"nombre": "Milanesa de Res", "precio": 200, "descripcion": "", "disponible": True}
        ]
    },
    {
        "nombre": "ENTRADAS",
        "color": "bg-orange-600",
        "imagen_url": "https://images.unsplash.com/photo-1581073750855-bac45fde1568?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxzaHJpbXAlMjBhcHBldGl6ZXJzfGVufDF8fHx8MTc1ODIwMjU3N3ww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral",
        "icono": "🍤",
        "orden": 2,
        "activo": True,
        "items": [
            {"nombre": "Camarón para Pelar 1/4", "precio": 150, "descripcion": "", "disponible": True},
            {"nombre": "Ceviche", "precio": 170, "descripcion": "", "disponible": True},
            {"nombre": "Pico al Gusto", "precio": 170, "descripcion": "", "disponible": True},
            {"nombre": "Plátanos Rellenos de Mariscos", "precio": 170, "descripcion": "", "disponible": True},
            {"nombre": "Orden de Empanadas", "precio": 180, "descripcion": "", "disponible": True},
            {"nombre": "Orden de Tostadas", "precio": 180, "descripcion": "", "disponible": True},
            {"nombre": "Salpicón de Jaiba", "precio": 190, "descripcion": "", "disponible": True},
            {"nombre": "Jaiva Enchipotlayada en Pulpa", "precio": 190, "descripcion": "", "disponible": True}
        ]
    },
    {
        "nombre": "MARISCOS",
        "color": "bg-blue-600",
        "imagen_url": "https://images.unsplash.com/photo-1750271328082-22490577fbb5?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxmcmVzaCUyMHNlYWZvb2QlMjBwbGF0dGVyfGVufDF8fHx8MTc1ODIwMjU4M3ww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral",
        "icono": "🦐",
        "orden": 3,
        "activo": True,
        "items": [
            {"nombre": "Torta de Mariscos", "precio": 200, "descripcion": "", "disponible": True},
            {"nombre": "Torta de Camarón", "precio": 180, "descripcion": "", "disponible": True},
            {"nombre": "Hueva de Lisa:", "precio": 0, "descripcion": "Título de sección", "disponible": True},
            {"nombre": "• A la Mexicana", "precio": 180, "descripcion": "Hueva de Lisa", "disponible": True},
            {"nombre": "• Enchipotlada", "precio": 190, "descripcion": "Hueva de Lisa", "disponible": True},
            {"nombre": "• Al mojo de Ajo", "precio": 190, "descripcion": "Hueva de Lisa", "disponible": True},
            {"nombre": "• A La Veracruzana", "precio": 190, "descripcion": "Hueva de Lisa", "disponible": True},
            {"nombre": "• En Salsa Verde", "precio": 190, "descripcion": "Hueva de Lisa", "disponible": True},
            {"nombre": "Arroz c/Camarones", "precio": 190, "descripcion": "", "disponible": True},
            {"nombre": "Arroz a la Tumbada", "precio": 200, "descripcion": "", "disponible": True}
        ]
    },
    {
        "nombre": "HUEVA DE LISA",
        "color": "bg-yellow-600",
        "imagen_url": "https://images.unsplash.com/photo-1750271328082-22490577fbb5?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxmcmVzaCUyMHNlYWZvb2QlMjBwbGF0dGVyfGVufDF8fHx8MTc1ODIwMjU4M3ww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral",
        "icono": "🥚",
        "orden": 4,
        "activo": True,
        "items": [
            {"nombre": "Frita", "precio": 250, "descripcion": "", "disponible": True},
            {"nombre": "Al mojo de ajo", "precio": 260, "descripcion": "", "disponible": True},
            {"nombre": "Enchipotlada", "precio": 260, "descripcion": "", "disponible": True},
            {"nombre": "En salsa verde", "precio": 260, "descripcion": "", "disponible": True}
        ]
    },
    {
        "nombre": "FILETES",
        "color": "bg-teal-600",
        "imagen_url": "https://images.unsplash.com/photo-1700760933394-976f1d27dff2?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxmaXNoJTIwZmlsbGV0JTIwZ3JpbGxlZHxlbnwxfHx8fDE3NTgyMDI1ODd8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral",
        "icono": "🐟",
        "orden": 5,
        "activo": True,
        "items": [
            {"nombre": "Casamiento de Camarón", "precio": 190, "descripcion": "", "disponible": True},
            {"nombre": "Filete Empanizado de Robalo", "precio": 190, "descripcion": "", "disponible": True},
            {"nombre": "Filete de Robalo a la Plancha", "precio": 200, "descripcion": "", "disponible": True},
            {"nombre": "Filete de Robalo Sol", "precio": 200, "descripcion": "", "disponible": True},
            {"nombre": "Filete de Robalo en Salsa Verde", "precio": 220, "descripcion": "", "disponible": True},
            {"nombre": "Filete de Robalo Gratinado", "precio": 220, "descripcion": "", "disponible": True},
            {"nombre": "Filete Relleno de Mariscos", "precio": 240, "descripcion": "", "disponible": True},
            {"nombre": "Mixto de Marisco Enchipotlayado", "precio": 250, "descripcion": "", "disponible": True}
        ]
    },
    {
        "nombre": "PESCADOS",
        "color": "bg-indigo-600",
        "imagen_url": "https://images.unsplash.com/photo-1708388464516-b52bfefde2b0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx3aG9sZSUyMGdyaWxsZWQlMjBmaXNofGVufDF8fHx8MTc1ODIwMjU5MHww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral",
        "icono": "🐠",
        "orden": 6,
        "activo": True,
        "items": [
            {"nombre": "Mojarra Frita 1 Kg", "precio": 250, "descripcion": "", "disponible": True},
            {"nombre": "Robalito Frito 1 Kg", "precio": 390, "descripcion": "", "disponible": True},
            {"nombre": "Al Gusto 1 Kg", "precio": 20, "descripcion": "extra", "disponible": True},
            {"nombre": "Rebosada Frita", "precio": 300, "descripcion": "", "disponible": True}
        ]
    },
    {
        "nombre": "CAMARONES",
        "color": "bg-pink-600",
        "imagen_url": "https://images.unsplash.com/photo-1565680018434-b513d5e5fd47?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxjb29rZWQlMjBzaHJpbXB8ZW58MXx8fHwxNzU4MjAyNTk1fDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral",
        "icono": "🍤",
        "orden": 7,
        "activo": True,
        "items": [
            {"nombre": "Empanizados", "precio": 200, "descripcion": "", "disponible": True},
            {"nombre": "Camarones a la Dario", "precio": 220, "descripcion": "", "disponible": True},
            {"nombre": "Al Mojo de Ajo", "precio": 220, "descripcion": "", "disponible": True},
            {"nombre": "Enchipotlados", "precio": 220, "descripcion": "", "disponible": True},
            {"nombre": "A la Plancha", "precio": 220, "descripcion": "", "disponible": True},
            {"nombre": "Enchipotlayados", "precio": 220, "descripcion": "", "disponible": True},
            {"nombre": "Al Ajillo", "precio": 220, "descripcion": "", "disponible": True},
            {"nombre": "Al Coco", "precio": 230, "descripcion": "", "disponible": True}
        ]
    },
    {
        "nombre": "CALDOS Y CONSOMÉS",
        "color": "bg-amber-600",
        "imagen_url": "https://images.unsplash.com/photo-1621174438159-6a9a82405498?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxzZWFmb29kJTIwc291cHxlbnwxfHx8fDE3NTgyMDI1OTl8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral",
        "icono": "🍲",
        "orden": 8,
        "activo": True,
        "items": [
            {"nombre": "Caldo de: Langostino 350g", "precio": 460, "descripcion": "", "disponible": True},
            {"nombre": "Camarón", "precio": 180, "descripcion": "Caldo de", "disponible": True},
            {"nombre": "Pescado 300gr", "precio": 180, "descripcion": "Caldo de", "disponible": True},
            {"nombre": "Robalo de 300gr", "precio": 300, "descripcion": "Caldo de", "disponible": True},
            {"nombre": "Chilpachole de Camarón", "precio": 190, "descripcion": "", "disponible": True},
            {"nombre": "c/Bollitas de Masa", "precio": 0, "descripcion": "Acompañamiento", "disponible": True},
            {"nombre": "Sopa de Mariscos", "precio": 200, "descripcion": "", "disponible": True},
            {"nombre": "Cazuela de Mariscos", "precio": 220, "descripcion": "", "disponible": True},
            {"nombre": "Consomé de:", "precio": 0, "descripcion": "Título de sección", "disponible": True},
            {"nombre": "Camarón", "precio": 30, "descripcion": "Consomé de", "disponible": True},
            {"nombre": "Jaiba", "precio": 30, "descripcion": "Consomé de", "disponible": True},
            {"nombre": "Pescado", "precio": 30, "descripcion": "Consomé de", "disponible": True}
        ]
    },
    {
        "nombre": "CÓCTELES",
        "color": "bg-cyan-600",
        "imagen_url": "https://images.unsplash.com/photo-1719750488901-076ffef0403c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxzZWFmb29kJTIwY29ja3RhaWx8ZW58MXx8fHwxNzU4MjAyNjAzfDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral",
        "icono": "🍹",
        "orden": 9,
        "activo": True,
        "items": [
            {"nombre": "Camarón", "precio": 80, "descripcion": "", "disponible": True},
            {"nombre": "Pulpo", "precio": 80, "descripcion": "", "disponible": True},
            {"nombre": "Jaiba", "precio": 80, "descripcion": "", "disponible": True},
            {"nombre": "Caracol", "precio": 80, "descripcion": "", "disponible": True},
            {"nombre": "Campechana de 2 Mariscos", "precio": 160, "descripcion": "", "disponible": True},
            {"nombre": "Vuelve a la Vida", "precio": 230, "descripcion": "", "disponible": True},
            {"nombre": "Consomé de Caracol", "precio": 160, "descripcion": "", "disponible": True}
        ]
    },
    {
        "nombre": "PULPOS",
        "color": "bg-purple-600",
        "imagen_url": "https://images.unsplash.com/photo-1731601816614-2423297fe97b?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxvY3RvcHVzJTIwZGlzaHxlbnwxfHx8fDE3NTgyMDI2MDd8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral",
        "icono": "🐙",
        "orden": 10,
        "activo": True,
        "items": [
            {"nombre": "Encebollados", "precio": 270, "descripcion": "", "disponible": True},
            {"nombre": "Enchipotlados", "precio": 0, "descripcion": "Sin precio especificado", "disponible": True},
            {"nombre": "Veracruzana", "precio": 230, "descripcion": "", "disponible": True},
            {"nombre": "Enchipotlayados", "precio": 0, "descripcion": "Sin precio especificado", "disponible": True},
            {"nombre": "Pulpos a la Dario", "precio": 350, "descripcion": "", "disponible": True}
        ]
    },
    {
        "nombre": "EXTRAS",
        "color": "bg-gray-600",
        "imagen_url": "https://images.unsplash.com/photo-1750271328082-22490577fbb5?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxmcmVzaCUyMHNlYWZvb2QlMjBwbGF0dGVyfGVufDF8fHx8MTc1ODIwMjU4M3ww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral",
        "icono": "🥗",
        "orden": 11,
        "activo": True,
        "items": [
            {"nombre": "Papas a la Francesas", "precio": 60, "descripcion": "", "disponible": True},
            {"nombre": "Pico de Gallo", "precio": 35, "descripcion": "", "disponible": True},
            {"nombre": "Guacamole", "precio": 40, "descripcion": "", "disponible": True}
        ]
    },
    {
        "nombre": "ENSALADAS",
        "color": "bg-lime-600",
        "imagen_url": "https://images.unsplash.com/photo-1750271328082-22490577fbb5?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxmcmVzaCUyMHNlYWZvb2QlMjBwbGF0dGVyfGVufDF8fHx8MTc1ODIwMjU4M3ww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral",
        "icono": "🥬",
        "orden": 12,
        "activo": True,
        "items": [
            {"nombre": "Camarón", "precio": 190, "descripcion": "", "disponible": True},
            {"nombre": "Pulpo", "precio": 220, "descripcion": "", "disponible": True},
            {"nombre": "Caracol", "precio": 220, "descripcion": "", "disponible": True},
            {"nombre": "Mixta de Marisco Gde", "precio": 450, "descripcion": "", "disponible": True},
            {"nombre": "Caracol al Ajillo", "precio": 220, "descripcion": "", "disponible": True}
        ]
    },
    {
        "nombre": "POSTRES",
        "color": "bg-rose-600",
        "imagen_url": "https://images.unsplash.com/photo-1750271328082-22490577fbb5?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxmcmVzaCUyMHNlYWZvb2QlMjBwbGF0dGVyfGVufDF8fHx8MTc1ODIwMjU4M3ww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral",
        "icono": "🍮",
        "orden": 13,
        "activo": True,
        "items": [
            {"nombre": "Flan Napolitano", "precio": 40, "descripcion": "", "disponible": True},
            {"nombre": "Helado Chalco", "precio": 80, "descripcion": "", "disponible": True}
        ]
    },
    {
        "nombre": "ANTOJITOS",
        "color": "bg-emerald-600",
        "imagen_url": "https://images.unsplash.com/photo-1750271328082-22490577fbb5?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxmcmVzaCUyMHNlYWZvb2QlMjBwbGF0dGVyfGVufDF8fHx8MTc1ODIwMjU4M3ww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral",
        "icono": "🫔",
        "orden": 14,
        "activo": True,
        "items": [
            {"nombre": "Platanos c/Arroz", "precio": 80, "descripcion": "", "disponible": True},
            {"nombre": "Platanos c/Frijoles Refritos", "precio": 80, "descripcion": "", "disponible": True},
            {"nombre": "Platanos c/Crema y Queso", "precio": 80, "descripcion": "", "disponible": True},
            {"nombre": "Gordas Blancas y Negras Picadas", "precio": 0, "descripcion": "Sin precio especificado", "disponible": True}
        ]
    },
    {
        "nombre": "BEBIDAS",
        "color": "bg-green-600",
        "imagen_url": "https://images.unsplash.com/photo-1650926978013-85c236b90e22?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtZXhpY2FuJTIwYmV2ZXJhZ2VzfGVufDF8fHx8MTc1ODIwMjYxMHww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral",
        "icono": "🥤",
        "orden": 15,
        "activo": True,
        "items": [
            {"nombre": "Agua Natural de Limón o Jamaica", "precio": 45, "descripcion": "", "disponible": True},
            {"nombre": "Limonada Mineral 500 ml", "precio": 50, "descripcion": "", "disponible": True},
            {"nombre": "Jarra de Agua 1.5 L", "precio": 140, "descripcion": "", "disponible": True},
            {"nombre": "Café América", "precio": 35, "descripcion": "", "disponible": True}
        ]
    },
    {
        "nombre": "CERVEZA",
        "color": "bg-yellow-600",
        "imagen_url": "https://images.unsplash.com/photo-1678120074037-51063532a3b6?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtZXhpY2FuJTIwYmVlciUyMGJvdHRsZXN8ZW58MXx8fHwxNzU4MjAyODMxfDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral",
        "icono": "🍺",
        "orden": 16,
        "activo": True,
        "items": [
            {"nombre": "Corona", "precio": 50, "descripcion": "", "disponible": True},
            {"nombre": "Victoria", "precio": 50, "descripcion": "", "disponible": True},
            {"nombre": "Negra Modelo", "precio": 50, "descripcion": "", "disponible": True},
            {"nombre": "Modelo Especial", "precio": 50, "descripcion": "", "disponible": True},
            {"nombre": "Ultra", "precio": 55, "descripcion": "", "disponible": True},
            {"nombre": "Michelada", "precio": 55, "descripcion": "", "disponible": True},
            {"nombre": "Chelada", "precio": 60, "descripcion": "", "disponible": True},
            {"nombre": "Chelada con Clamato", "precio": 65, "descripcion": "", "disponible": True},
            {"nombre": "Cerveza Premium", "precio": 75, "descripcion": "", "disponible": True}
        ]
    },
    {
        "nombre": "REFRESCOS",
        "color": "bg-red-600",
        "imagen_url": "https://images.unsplash.com/photo-1670213543633-7cb7ff372b83?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtZXhpY2FuJTIwc29mdCUyMGRyaW5rcyUyMGNvY2ElMjBjb2xhfGVufDF8fHx8MTc1ODIwMjgzNHww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral",
        "icono": "🥤",
        "orden": 17,
        "activo": True,
        "items": [
            {"nombre": "Coca Cola 355 ml", "precio": 40, "descripcion": "", "disponible": True},
            {"nombre": "Peñafiel Manzana 355 ml", "precio": 40, "descripcion": "", "disponible": True},
            {"nombre": "Peñafiel Toronja 355 ml", "precio": 40, "descripcion": "", "disponible": True},
            {"nombre": "Sangría Señorial 355 ml", "precio": 40, "descripcion": "", "disponible": True},
            {"nombre": "Sprite 355 ml", "precio": 40, "descripcion": "", "disponible": True},
            {"nombre": "Fanta 355 ml", "precio": 40, "descripcion": "", "disponible": True}
        ]
    },
    {
        "nombre": "LICORES",
        "color": "bg-purple-600",
        "imagen_url": "https://images.unsplash.com/photo-1717116068433-c0896dbd563c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtZXhpY2FuJTIwbGlxdW9yJTIwYm90dGxlc3xlbnwxfHx8fDE3NTgyMDI4NDN8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral",
        "icono": "🍷",
        "orden": 18,
        "activo": True,
        "items": [
            {"nombre": "Licor de Cacahuate", "precio": 70, "descripcion": "", "disponible": True},
            {"nombre": "Licor de Jobo", "precio": 70, "descripcion": "", "disponible": True},
            {"nombre": "Licor de Café", "precio": 75, "descripcion": "", "disponible": True},
            {"nombre": "Licor de Coco", "precio": 75, "descripcion": "", "disponible": True}
        ]
    },
    {
        "nombre": "BEBIDAS MEXICANAS",
        "color": "bg-orange-600",
        "imagen_url": "https://images.unsplash.com/photo-1650926978013-85c236b90e22?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtZXhpY2FuJTIwYmV2ZXJhZ2VzfGVufDF8fHx8MTc1ODIwMjYxMHww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral",
        "icono": "🌮",
        "orden": 19,
        "activo": True,
        "items": [
            {"nombre": "Horchata", "precio": 45, "descripcion": "", "disponible": True},
            {"nombre": "Agua de Tamarindo", "precio": 45, "descripcion": "", "disponible": True},
            {"nombre": "Agua de Hibisco", "precio": 45, "descripcion": "", "disponible": True},
            {"nombre": "Tepache", "precio": 50, "descripcion": "", "disponible": True},
            {"nombre": "Agua Fresca de Chía", "precio": 50, "descripcion": "", "disponible": True}
        ]
    }
]

# Características del restaurante
caracteristicas = [
    {
        "titulo": "Horarios Flexibles",
        "descripcion": "Abierto todos los días de 9:00 AM a 6:00 PM",
        "icono": "⏰"
    },
    {
        "titulo": "Capacidad Amplia", 
        "descripcion": "Espacio para 150 comensales en un ambiente acogedor",
        "icono": "👥"
    },
    {
        "titulo": "Calidad Garantizada",
        "descripcion": "Mariscos frescos seleccionados diariamente", 
        "icono": "🏆"
    },
    {
        "titulo": "Tradición Familiar",
        "descripcion": "Más de 20 años sirviendo los mejores mariscos",
        "icono": "❤️"
    }
]

# Servicios adicionales
servicios = [
    {
        "nombre": "Pedidos por WhatsApp",
        "descripcion": "Listo en 30 minutos",
        "icono": "⏰"
    },
    {
        "nombre": "Entrega disponible",
        "descripcion": "Servicio a domicilio",
        "icono": "🚗"
    },
    {
        "nombre": "Pago flexible",
        "descripcion": "Efectivo/transferencia",
        "icono": "💳"
    }
]

# ----------------------------------------------------------------------
# FUNCIONES PRINCIPALES
# ----------------------------------------------------------------------

def crear_directorio_temporal():
    """Crear directorio temporal para imágenes si no existe"""
    if not os.path.exists(TEMP_IMAGES_DIR):
        os.makedirs(TEMP_IMAGES_DIR)
        print(f"📁 Directorio temporal creado: {TEMP_IMAGES_DIR}")

def descargar_imagen(url, filename):
    """Descargar una imagen desde URL y guardarla localmente"""
    try:
        print(f"⏳ Descargando imagen: {filename}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        filepath = os.path.join(TEMP_IMAGES_DIR, filename)
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ Imagen descargada: {filename}")
        return filepath
    except Exception as e:
        print(f"❌ Error descargando {filename}: {e}")
        return None

def subir_imagen_a_mongodb(filepath, filename, fs):
    """Subir una imagen a MongoDB usando GridFS"""
    try:
        if not os.path.exists(filepath):
            print(f"❌ Archivo no encontrado: {filepath}")
            return None
        
        with open(filepath, 'rb') as archivo_img:
            file_id = fs.put(
                archivo_img,
                filename=filename,
                contentType='image/jpeg'
            )
        
        print(f"✅ Imagen subida a MongoDB: {filename} (ID: {file_id})")
        return str(file_id)
    except Exception as e:
        print(f"❌ Error subiendo {filename}: {e}")
        return None

def limpiar_archivos_temporales():
    """Eliminar archivos temporales descargados"""
    try:
        if os.path.exists(TEMP_IMAGES_DIR):
            for filename in os.listdir(TEMP_IMAGES_DIR):
                filepath = os.path.join(TEMP_IMAGES_DIR, filename)
                os.remove(filepath)
            os.rmdir(TEMP_IMAGES_DIR)
            print("🧹 Archivos temporales eliminados")
    except Exception as e:
        print(f"⚠️ Error limpiando archivos temporales: {e}")

def almacenar_datos_restaurante():
    """Función principal que almacena todos los datos del restaurante en MongoDB"""
    
    client = None
    try:
        print("🚀 Iniciando proceso de almacenamiento de datos del restaurante...")
        
        # Crear directorio temporal
        crear_directorio_temporal()
        
        # Conectar a MongoDB
        print("📡 Conectando a MongoDB...")
        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        fs = gridfs.GridFS(db)
        
        # Limpiar colecciones existentes
        print("🧹 Limpiando colecciones existentes...")
        db.restaurante_info.delete_many({})
        db.contacto_info.delete_many({})
        db.categorias_menu.delete_many({})
        db.items_menu.delete_many({})
        db.caracteristicas.delete_many({})
        db.servicios.delete_many({})
        
        # También limpiar archivos de GridFS
        for file in fs.find():
            fs.delete(file._id)
        print("✅ Colecciones limpiadas")
        
        # 1. Guardar información general del restaurante
        print("\n📝 Guardando información general del restaurante...")
        restaurante_doc = {
            **restaurante_info,
            "fecha_actualizacion": datetime.now(),
            "version": "1.0"
        }
        db.restaurante_info.insert_one(restaurante_doc)
        print("✅ Información general guardada")
        
        # 2. Guardar información de contacto
        print("\n📞 Guardando información de contacto...")
        contacto_doc = {
            **contacto_info,
            "fecha_actualizacion": datetime.now()
        }
        db.contacto_info.insert_one(contacto_doc)
        print("✅ Información de contacto guardada")
        
        # 3. Procesar categorías del menú con imágenes
        print("\n🍽️ Procesando categorías del menú...")
        
        for categoria in menu_categorias:
            print(f"\n--- Procesando categoría: {categoria['nombre']} ---")
            
            # Descargar imagen de la categoría
            imagen_filename = f"categoria_{categoria['nombre'].lower().replace(' ', '_')}.jpg"
            imagen_path = descargar_imagen(categoria['imagen_url'], imagen_filename)
            
            # Subir imagen a MongoDB
            imagen_id = None
            if imagen_path:
                imagen_id = subir_imagen_a_mongodb(imagen_path, imagen_filename, fs)
            
            # Preparar documento de categoría
            categoria_doc = {
                "nombre": categoria['nombre'],
                "color": categoria['color'],
                "icono": categoria['icono'],
                "orden": categoria['orden'],
                "activo": categoria['activo'],
                "imagen_url_original": categoria['imagen_url'],
                "imagen_id": imagen_id,
                "fecha_creacion": datetime.now(),
                "fecha_actualizacion": datetime.now()
            }
            
            # Insertar categoría
            categoria_result = db.categorias_menu.insert_one(categoria_doc)
            categoria_id = categoria_result.inserted_id
            
            print(f"✅ Categoría '{categoria['nombre']}' guardada")
            
            # Procesar items de la categoría
            print(f"📋 Procesando {len(categoria['items'])} items...")
            
            for idx, item in enumerate(categoria['items']):
                item_doc = {
                    "categoria_id": categoria_id,
                    "categoria_nombre": categoria['nombre'],
                    "nombre": item['nombre'],
                    "precio": item['precio'],
                    "descripcion": item['descripcion'],
                    "disponible": item['disponible'],
                    "orden": idx + 1,
                    "fecha_creacion": datetime.now(),
                    "fecha_actualizacion": datetime.now()
                }
                
                db.items_menu.insert_one(item_doc)
            
            print(f"✅ {len(categoria['items'])} items guardados para '{categoria['nombre']}'")
        
        # 4. Guardar características del restaurante
        print("\n⭐ Guardando características del restaurante...")
        for caracteristica in caracteristicas:
            caract_doc = {
                **caracteristica,
                "fecha_creacion": datetime.now()
            }
            db.caracteristicas.insert_one(caract_doc)
        print(f"✅ {len(caracteristicas)} características guardadas")
        
        # 5. Guardar servicios
        print("\n🛎️ Guardando servicios...")
        for servicio in servicios:
            servicio_doc = {
                **servicio,
                "fecha_creacion": datetime.now()
            }
            db.servicios.insert_one(servicio_doc)
        print(f"✅ {len(servicios)} servicios guardados")
        
        # 6. Crear índices para mejor rendimiento
        print("\n🔍 Creando índices...")
        db.categorias_menu.create_index("nombre")
        db.categorias_menu.create_index("orden")
        db.items_menu.create_index("categoria_id")
        db.items_menu.create_index("nombre")
        db.items_menu.create_index("disponible")
        print("✅ Índices creados")
        
        # Limpiar archivos temporales
        limpiar_archivos_temporales()
        
        # Mostrar resumen
        print("\n" + "="*60)
        print("🎉 ¡PROCESO COMPLETADO EXITOSAMENTE!")
        print("="*60)
        print(f"📊 Resumen de datos almacenados:")
        print(f"   • Categorías de menú: {len(menu_categorias)}")
        print(f"   • Items de menú: {sum(len(cat['items']) for cat in menu_categorias)}")
        print(f"   • Imágenes subidas: {len(menu_categorias)}")
        print(f"   • Características: {len(caracteristicas)}")
        print(f"   • Servicios: {len(servicios)}")
        print(f"📍 Base de datos: {DATABASE_NAME}")
        print(f"🔗 MongoDB URI: {MONGO_URI}")
        print("="*60)
        
    except Exception as e:
        print(f"🚨 Error general: {e}")
        
    finally:
        if client:
            client.close()
            print("🔌 Conexión a MongoDB cerrada")

if __name__ == "__main__":
    almacenar_datos_restaurante()