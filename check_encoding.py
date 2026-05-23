import sqlite3

conn = sqlite3.connect('db.sqlite3')
rows = conn.execute('SELECT id, title FROM blog_post').fetchall()
for r in rows:
    raw = r[1]
    print('RAW:', repr(raw[:80]))
    try:
        fixed = raw.encode('latin-1').decode('utf-8')
        print('FIXED:', fixed[:80])
    except:
        print('FIXED: no se pudo corregir')
    print()
