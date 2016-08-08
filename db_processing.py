import sqlite3
def create_db():
    conn = sqlite3.connect('schools.db')
    c = conn.cursor()
    c.execute('CREATE TABLE schools (chat_id text, school_id text)')
    conn.close()
    
def db_update(chat_id, sc_id):
    conn = sqlite3.connect('schools.db')
    c = conn.cursor()
    c.execute('SELECT school_id FROM schools WHERE chat_id = %s' % chat_id)
    if c.fetchone():
        c.execute('UPDATE schools SET school_id=%s WHERE chat_id=%s' % (sc_id, chat_id))
    else:
        c.execute('INSERT INTO schools VALUES (%s, %s)' % (chat_id, sc_id))
    conn.commit()
    conn.close()

def db_check(chat_id):
    conn = sqlite3.connect('schools.db')
    c = conn.cursor()
    c.execute('SELECT school_id FROM schools WHERE chat_id = %s' % chat_id)
    school_id = c.fetchone()[0]
    return school_id
    
