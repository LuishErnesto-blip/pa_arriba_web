with open('termometro/templates/termometro/resultado.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = 'perdiendo entre <strong> y </strong> mensuales en fugas silenciosas.'
new = 'perdiendo entre <strong>300 y 800 dolares</strong> mensuales en fugas silenciosas.'

result = content.replace(old, new)
print('Cambio aplicado:', old in content and old not in result)

with open('termometro/templates/termometro/resultado.html', 'w', encoding='utf-8') as f:
    f.write(result)
