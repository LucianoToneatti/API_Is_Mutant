# Etapa de construcción
FROM python:3.11.6-slim-bullseye AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Etapa final
FROM python:3.11.6-slim-bullseye

WORKDIR /app

# Copiar los paquetes instalados desde la etapa de construcción
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copiar el resto de los archivos necesarios
COPY . .

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]



