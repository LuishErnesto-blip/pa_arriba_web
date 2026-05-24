import subprocess
import os

# Descargar backups
subprocess.run(['gsutil', 'cp', 'gs://paarriba-media-ec/backups/termometro_backup.json', '/tmp/termometro_backup.json'])
subprocess.run(['gsutil', 'cp', 'gs://paarriba-media-ec/backups/prospectos_backup.json', '/tmp/prospectos_backup.json'])

# Importar a PostgreSQL
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pa_arriba_project.settings')
django.setup()

from django.core.management import call_command
call_command('loaddata', '/tmp/termometro_backup.json')
call_command('loaddata', '/tmp/prospectos_backup.json')
print('Migracion completada OK')
