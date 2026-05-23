import sqlite3

conn = sqlite3.connect('db.sqlite3')
rows = conn.execute('SELECT id, title, published_date, author, slug, image, keywords, image_alt_text, meta_description, is_published, content FROM blog_post').fetchall()

def esc(v):
    if v is None:
        return 'NULL'
    return "'" + str(v).replace("'", "''") + "'"

with open('blog_data.sql', 'w', encoding='utf-8') as f:
    f.write('-- Blog posts migration\n')
    for r in rows:
        line = 'INSERT INTO blog_post (id, title, published_date, author, slug, image, keywords, image_alt_text, meta_description, is_published, content) VALUES ('
        line += ','.join([esc(r[0]), esc(r[1]), esc(r[2]), esc(r[3]), esc(r[4]), esc(r[5]), esc(r[6]), esc(r[7]), esc(r[8]), str(r[9]), esc(r[10])])
        line += ') ON CONFLICT (id) DO NOTHING;\n'
        f.write(line)

print('OK', len(rows), 'registros')
