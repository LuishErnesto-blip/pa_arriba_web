with open("blog_data.sql", "r", encoding="utf-8") as f:
    content = f.read()
print("Caracteres especiales OK:" , "¡" in content or "ó" in content or "é" in content)
print("Primeros 200 chars:")
print(content[:200])
