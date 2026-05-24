import json

with open('termometro_backup.json', 'r', encoding='utf-16') as f:
    data = json.load(f)

with open('termometro_import.sql', 'w', encoding='utf-8') as out:
    out.write('-- Termometro import\n')
    for obj in data:
        fields = obj['fields']
        out.write(f"""INSERT INTO termometro_termometrorespuesta (id, nombre, telefono, correo, tipo_negocio, fase_actual, ingresos_mes, mayor_problema, herramienta_actual, interes_demo, fecha_respuesta, fase_final, puntaje_total) VALUES ({obj['pk']}, {json.dumps(fields.get('nombre',''))}, {json.dumps(fields.get('telefono',''))}, {json.dumps(fields.get('correo',''))}, {json.dumps(fields.get('tipo_negocio',''))}, {json.dumps(fields.get('fase_actual',''))}, {json.dumps(fields.get('ingresos_mes',''))}, {json.dumps(fields.get('mayor_problema',''))}, {json.dumps(fields.get('herramienta_actual',''))}, {json.dumps(fields.get('interes_demo',''))}, {json.dumps(fields.get('fecha_respuesta',''))}, {json.dumps(fields.get('fase_final',''))}, {fields.get('puntaje_total', 0)}) ON CONFLICT (id) DO NOTHING;\n""")

print(f'Generado termometro_import.sql con {len(data)} registros')
