import subprocess


DB_USER_NAME = 'postgres'
DB_USER_PASSWORD = 'postgres'
DB_ADDRESS = '34.88.140.102'
DB_PORT = '5432'
DB_NAME = 'postgres'

ORIGINS = [
    'http://localhost',
    'http://localhost:8000',
    'http://localhost:3000',
    'http://10.166.0.3:3000',
    'http://35.228.28.221:3000',
]

WKHTMLTOPDF_PATH = subprocess.run(["which", "wkhtmltopdf"], capture_output=True, text=True).stdout.strip()
