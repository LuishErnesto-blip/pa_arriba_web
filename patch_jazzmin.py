with open("pa_arriba_project/settings.py", "r", encoding="utf-8") as f:
    content = f.read()

old = "INSTALLED_APPS = [\n    'django.contrib.admin',"
new = "INSTALLED_APPS = [\n    'jazzmin',\n    'django.contrib.admin',"

if old in content:
    content = content.replace(old, new)
    with open("pa_arriba_project/settings.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("OK - jazzmin agregado")
else:
    print("ERROR - texto no encontrado")
