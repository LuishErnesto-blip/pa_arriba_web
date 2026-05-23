import sqlite3
conn = sqlite3.connect("db.sqlite3")

# Ver estructura de la tabla
cols = conn.execute("PRAGMA table_info(blog_prospecto)").fetchall()
print("=== COLUMNAS blog_prospecto ===")
for c in cols:
    print(c[1], c[2])

# Ver registros existentes
print("\n=== REGISTROS ===")
rows = conn.execute("SELECT * FROM blog_prospecto").fetchall()
for r in rows:
    print(r)
