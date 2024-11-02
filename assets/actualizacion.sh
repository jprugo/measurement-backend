#!/bin/bash

# Eliminar directorios si existen
rm -rf ~/Documentos/measurement-backend
rm -rf ~/Documentos/measurement-frontend

# Clonar los repositorios
git clone https://github.com/jprugo/measurement-backend.git
git clone https://github.com/jprugo/measurement-frontend.git

cd ~/Documentos/measurement-backend || { echo "Directorio 'app' no encontrado"; exit 1; }

# Instalar dependencias (python)
pip install -r requirements.txt

# Configurar BD
DB_NAME="measurements.db"
sqlite3 $DB_NAME < ddl.sql
echo "Base de datos '$DB_NAME' creada y tabla 'measurements' creada."

# Refrescar apache
cp -r ~/Documentos/measurement-frontend/* /var/www/html
sudo systemctl restart apache2

echo "Proceso completado exitosamente"
