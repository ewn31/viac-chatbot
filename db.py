import sqlite3

dbname =  'ChatBot'
#multiple threads can write using same connection can lead to unwanted modifications
#will have to serialize in the future
con =  sqlite3.connect(dbname, check_same_thread=False)
if con:
    print('Database connected')
else:
    print('Failed to connect to database')

def create_table(dbname):
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS memories(user_id PRIMARY KEY, memory_string)')
    print(f'Table memory created in database {dbname}')
    #cur.execute('CREATE TABLE users(user_id)')
    cur.close()
    con.commit()
    
create_table(dbname)

cursor = con.cursor()
cursor.execute('select * from memories')
print(cursor.fetchall())
cursor.close()

def save_user(user_id, mem):
    cur = con.cursor()
    cur.execute('INSERT INTO memories(user_id, memory_string) values(?, ?)', (user_id, mem))
    con.commit()
    print(f'User : {user_id} inserted succesfully')
    cur.close()

def save_memory(user_id, memory_data):
    cur = con.cursor()
    cur.execute('UPDATE memories SET memory_string = ? where user_id = ?', (memory_data, user_id))
    con.commit()
    print(cur.execute('select memory_string from memories where user_id = ?', (user_id,)).fetchone())
    print(f'{user_id} memory saved')    
    cur.close()

def get_memory(user_id):
    cur = con.cursor()
    res = cur.execute('select memory_string from memories where user_id = ?', (user_id,))
    mem = res.fetchone()
    print(f'User: {user_id} memory : {mem} succesfully retrieved')
    cur.close()
    return list(mem)

def user_exist(user_id):
    cur = con.cursor()
    res = cur.execute('select user_id from memories where user_id = ?', (user_id, ))
    user = res.fetchone()
    cur.close()
    if user:
        print(f'User: {user_id} retrieved succesfully')
        return True
    else:
        print(f'User : {user} not in database')
        return False

def drop_table():   
    cur = con.cursor()
    cur.execute('DROP TABLE IF EXISTS memories')
    print(f'Table: memories dropped succesfully')
    con.commit()
    cur.close()
if __name__ == '__main__' :
    test_user_id, test_memory = '001','Welcome' 
    dbname = 'ChatBot'
    create_table(dbname)
    save_user(test_user_id, test_memory)
    save_memory(test_user_id, 'New Memory')
    print(user_exist(test_user_id))
    print(get_memory(test_user_id))
    drop_table()
    
