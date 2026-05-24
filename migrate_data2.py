import os
import requests
import tempfile
from django.core.management import call_command

# Descargar con requests (disponible en la imagen)
for url, name in [
    ('https://storage.googleapis.com/paarriba-media-ec/backups/termometro_backup.json', 'termometro_backup.json'),
    ('https://storage.googleapis.com/paarriba-media-ec/backups/prospectos_backup.json', 'prospectos_backup.json'),
]:
    r = requests.get(url)
    path = f'/tmp/{name}'
    with open(path, 'wb') as f:
        f.write(r.content)
    call_command('loaddata', path)
    print(f'Importado: {name}')

print('OK')
