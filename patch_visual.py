path = "core/templates/core/rentabilidad_landing.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Corrección de Contraste: Agregar color de texto oscuro a la sección del encebollado
old_section = '<section class="py-16 px-4 bg-gray-50 border-t border-b border-gray-200">'
new_section = '<section class="py-16 px-4 bg-gray-50 border-t border-b border-gray-200 text-gray-900">'
content = content.replace(old_section, new_section)

# 2. Corrección de Ancho: Unificar el contenedor estrecho a max-w-4xl para mantener la simetría
content = content.replace('<div class="max-w-3xl mx-auto">', '<div class="max-w-4xl mx-auto">')

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("Correccion de contraste y ancho aplicada exitosamente.")
