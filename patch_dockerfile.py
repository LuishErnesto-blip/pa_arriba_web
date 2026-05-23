with open("Dockerfile", "r", encoding="utf-8") as f:
    content = f.read()

old = "# Copiar el proyecto\nCOPY . /app/\n\n# Puerto que usa Cloud Run"
new = "# Copiar el proyecto\nCOPY . /app/\n\n# Recopilar archivos estaticos\nRUN python manage.py collectstatic --noinput\n\n# Puerto que usa Cloud Run"

if old in content:
    content = content.replace(old, new)
    with open("Dockerfile", "w", encoding="utf-8") as f:
        f.write(content)
    print("OK - collectstatic agregado")
else:
    print("ERROR - texto no encontrado")
