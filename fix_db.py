with open('pa_arriba_project/settings.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_block = (
    "# Database\n"
    "# -------------------------------------------------------\n"
    "# BASE DE DATOS FORZADA A SQLITE\n"
    "# NO se usa Postgres\n"
    "# NO se lee DATABASE_URL\n"
    "# NO se intenta conexión remota\n"
    "if dj_database_url:\n"
    "    DATABASES = {\n"
    "        'default': dj_database_url.config(\n"
    "            default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'),\n"
    "            conn_max_age=600\n"
    "        )\n"
    "    }\n"
    "else:\n"
    "    DATABASES = {\n"
    '        "default": {\n'
    '            "ENGINE": "django.db.backends.sqlite3",\n'
    '            "NAME": BASE_DIR / "db.sqlite3",\n'
    "        }\n"
    "    }"
)

new_block = (
    "# Database\n"
    "# -------------------------------------------------------\n"
    "# PostgreSQL en produccion (DATABASE_URL via env var)\n"
    "# SQLite como fallback local\n"
    "DATABASE_URL = os.environ.get('DATABASE_URL')\n"
    "\n"
    "if DATABASE_URL:\n"
    "    DATABASES = {\n"
    "        'default': dj_database_url.config(\n"
    "            default=DATABASE_URL,\n"
    "            conn_max_age=600\n"
    "        )\n"
    "    }\n"
    "else:\n"
    "    DATABASES = {\n"
    '        "default": {\n'
    '            "ENGINE": "django.db.backends.sqlite3",\n'
    '            "NAME": BASE_DIR / "db.sqlite3",\n'
    "        }\n"
    "    }"
)

if old_block in content:
    content = content.replace(old_block, new_block)
    with open('pa_arriba_project/settings.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('REEMPLAZO EXITOSO')
else:
    print('ERROR: texto no encontrado - no se modifico nada')
