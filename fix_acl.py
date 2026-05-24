with open('pa_arriba_project/settings.py', 'rb') as f:
    content = f.read()
old = b'GS_DEFAULT_ACL = "publicRead"\r\n'
new_val = b'GS_DEFAULT_ACL = None\r\n'
result = content.replace(old, new_val)
print('Cambio aplicado:', old in content and old not in result)
with open('pa_arriba_project/settings.py', 'wb') as f:
    f.write(result)
