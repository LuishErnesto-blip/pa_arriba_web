with open('termometro/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = '    request.session["exito"] = True\n    request.session["fase_final"] = fase_final\n    request.session["puntaje_caos"] = puntaje_total\n\n    # Redirigimos de vuelta a la vista de la landing para mostrar el mensaje de \u00e9xito\n    return redirect(\'termometro:diagnostico\')'

new = '    return render(request, \'termometro/resultado.html\', {\n        \'fase_final\': fase_final,\n        \'puntaje_caos\': puntaje_total,\n        \'nombre\': request.POST.get(\'nombre\'),\n        \'whatsapp\': request.POST.get(\'whatsapp\'),\n    })'

result = content.replace(old, new)
print('Cambio aplicado:', old in content and old not in result)
with open('termometro/views.py', 'w', encoding='utf-8') as f:
    f.write(result)
