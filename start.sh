#!/bin/bash
# Script para despliegue en Railway/Render/etc.

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python -m uvicorn main:app --host 0.0.0.0 --port $PORT