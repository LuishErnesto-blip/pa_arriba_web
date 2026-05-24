with open('termometro/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = "    return render(request, 'termometro/resultado.html', {\n        'fase_final': fase_final,\n        'puntaje_caos': puntaje_total,\n        'nombre': request.POST.get('nombre'),\n        'whatsapp': request.POST.get('whatsapp'),\n    })"

new = "    nombre = request.POST.get('nombre', '')\n    whatsapp_msg = f'Hola, soy {nombre}. Completé el diagnóstico Pa Arriba y mi resultado es {fase_final} (puntaje {puntaje_total}/16). Quiero saber cómo mejorar mi negocio.'\n    import urllib.parse\n    return render(request, 'termometro/resultado.html', {\n        'fase_final': fase_final,\n        'puntaje_caos': puntaje_total,\n        'nombre': nombre,\n        'whatsapp': request.POST.get('whatsapp'),\n        'whatsapp_message': urllib.parse.quote(whatsapp_msg),\n    })"

result = content.replace(old, new)
print('Cambio aplicado:', old in content and old not in result)
with open('termometro/views.py', 'w', encoding='utf-8') as f:
    f.write(result)
