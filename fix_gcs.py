with open('pa_arriba_project/settings.py', 'rb') as f:
    content = f.read()

old = b'GCS_BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME", "paarriba-media-ec")\r\nGCS_DEFAULT_ACL = "publicRead"\r\nGCS_QUERYSTRING_AUTH = False\r\nGCS_FILE_OVERWRITE = False'

new = b'GS_BUCKET_NAME = os.environ.get("GS_BUCKET_NAME", "paarriba-media-ec")\r\nGS_DEFAULT_ACL = "publicRead"\r\nGS_QUERYSTRING_AUTH = False\r\nGS_FILE_OVERWRITE = False'

result = content.replace(old, new)
print('Cambio aplicado:', old in content and old not in result)

with open('pa_arriba_project/settings.py', 'wb') as f:
    f.write(result)
