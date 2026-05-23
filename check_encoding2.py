with open("pa_arriba_project/settings.py", "rb") as f:
    content = f.read()

# Detectar encoding
try:
    content.decode("utf-8")
    print("UTF-8 OK")
except:
    print("NO es UTF-8 - intentando latin-1")
    text = content.decode("latin-1")
    with open("pa_arriba_project/settings.py", "w", encoding="utf-8") as f:
        f.write(text)
    print("Convertido a UTF-8 OK")
