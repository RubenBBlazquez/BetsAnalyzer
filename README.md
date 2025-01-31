Pasos para arrancar el proyecto:
1. Dar permisos de ejecución al script de airflow_dags_entry_point.sh
2. Dar todos los permisos chmod 777 a la carpeta airflow_config y sus subcarpetas (es una carpeta interna que necesitará airflow)
3. Dar todos los permisos sólo a la carpeta de data_pipelines (no dar todos los permisos a los archivos.py de dentro), esto es debido a que esa carpeta es una librería, y al instalarse genera un archivo .egg-info que necesita permisos de escritura.
4. Ir a la carpeta config y copiar el archivo .env_sample y crear .env, que contiene credenciales, urls...
5. Ejecutar docker-compose up -d

Urls
- Airflow: http://localhost:8080
  - User: airflow
  - Password: airflow


- SeleniumHub: http://localhost:4444/grid/console


- redis: http://localhost:6379

**A tener en cuenta**:
Para la generación de dags, lo que hace el scheduler de airflow es leer continuamente la carpeta dags de data_pipelines,
y crear un enlace simbólico dentro de la máquina de airflow, puedes verlo en el script de airflow_dags_entrypoint.sh