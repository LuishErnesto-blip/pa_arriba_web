with open('pa_arriba_project/settings.py', 'rb') as f:
    content = f.read()

old_storages = b'STORAGES = {\r\n\r\n    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},\r\n\r\n    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"},\r\n\r\n}'

new_storages = b'# CAMBIO FECHA:2026-05-23|MOTIVO: Redirigir uploads a GCS para persistencia en Cloud Run\r\nGCS_BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME", "paarriba-media-ec")\r\nGCS_DEFAULT_ACL = "publicRead"\r\nGCS_QUERYSTRING_AUTH = False\r\nGCS_FILE_OVERWRITE = False\r\n\r\nSTORAGES = {\r\n    "default": {"BACKEND": "storages.backends.gcloud.GoogleCloudStorage"},\r\n    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"},\r\n}'

old_media = b"MEDIA_ROOT = os.path.join(BASE_DIR, 'media')\r\n\r\nMEDIA_URL = '/media/'"

new_media = b"# CAMBIO FECHA:2026-05-23|MOTIVO: Media servida desde GCS\r\nMEDIA_URL = 'https://storage.googleapis.com/paarriba-media-ec/'"

c1 = content.replace(old_storages, new_storages)
c2 = c1.replace(old_media, new_media)

print('STORAGES reemplazado:', old_storages in content and old_storages not in c1)
print('MEDIA reemplazado:', old_media in content and old_media not in c2)

with open('pa_arriba_project/settings.py', 'wb') as f:
    f.write(c2)

print('OK')
