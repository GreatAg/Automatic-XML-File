import psycopg2
con = psycopg2.connect(host="94.130.7.131", database="solish", user="ali_ag", password="Im_FoCkinG-@g")

# cur = con.cursor()
# # # cur.execute('''SELECT main_text , id FROM mode''')
# # # result = cur.fetchall()
# # # for i in result:
# # #     text =f'{i[1]}:{i[0]}'
# # #     cur.execute(f'''UPDATE mode
# # #                SET main_text=%(text)s
# # #                Where id = %(id)s''',{'id': i[1], 'text': text})
# cur.execute('''SELECT main_text , type ,id FROM mode''')
# load = cur.fetchall()
# database.insert_date(load)
# con.commit()
# cur.close()


def add_main_text(id,text):
    cur = con.cursor()
    #cur.execute(f"""INSERT INTO mode (id,main_text)
    #           VALUES (%(id)s,%(text)s)""",{'id': id,'text': f'{text}'})
    cur.execute(f'''UPDATE ali_ag_db.mode
                SET main_text=%(text)s
                 Where id = %(id)s''',{'id':f'{id}', 'text': f'{text}'})
    con.commit()
    cur.close()


def add_main_id(id):
    cur = con.cursor()
    cur.execute(f"""INSERT INTO ali_ag_db.mode (id) 
               VALUES ({id})""")
    con.commit()
    cur.close()


def add_main_key(keys):
    cur = con.cursor()
    cur.execute(f"""UPDATE ali_ag_db.mode
               SET main_key = %(keys)s""",{'keys': f'{keys}'})
    con.commit()
    cur.close()


def insert_information(user_id,name):
    cur = con.cursor()
    cur.execute(f"""INSERT INTO ali_ag_db.projects (user_id,project_name) 
               VALUES (%(user_id)s,%(project_name)s)""",{'user_id': user_id,'project_name': f'{name}'})
    con.commit()
    cur.close()


def load_pj(user_id):
    cur = con.cursor()
    cur.execute("""SELECT project_name FROM ali_ag_db.projects
                 WHERE user_id = %(user_id)s""",{'user_id': user_id})
    load = cur.fetchall()
    con.commit()
    cur.close()
    load = [i[0] for i in load]
    return load


def load_types():
    cur = con.cursor()
    cur.execute('''SELECT DISTINCT type FROM ali_ag_db.mode''')
    load = cur.fetchall()
    con.commit()
    cur.close()
    load = [i[0] for i in load]
    return load


def load_text(name):
    cur = con.cursor()
    cur.execute('''SELECT DISTINCT main_text FROM ali_ag_db.mode
                   WHERE type = %(name)s''', {'name':name})
    load = cur.fetchall()
    con.commit()
    cur.close()
    load = [i[0] for i in load]
    return load


def load_txt(id):
    cur = con.cursor()
    cur.execute('''SELECT  main_text FROM ali_ag_db.mode
                   WHERE id = %(id)s''', {'id':id})
    load = cur.fetchone()
    con.commit()
    cur.close()
    return load


def load_text_id(text):
    cur = con.cursor()
    cur.execute('''SELECT id FROM ali_ag_db.mode
                   WHERE main_text = %(text)s''', {'text': text})
    load = cur.fetchone()
    con.commit()
    cur.close()
    return load


def load_user_text(id, user_id,name):
    cur = con.cursor()
    cur.execute('''SELECT user_text FROM ali_ag_db.users
                WHERE user_id=%(user_id)s AND text_id = %(id)s AND project_name=%(name)s''',{'user_id': user_id , 'id':id, 'name': name})
    load = cur.fetchone()
    con.commit()
    cur.close()
    if load is None:
        return load
    return load


def update_text(text,name,id,user_id):
    cur = con.cursor()
    cur.execute('''UPDATE ali_ag_db.users SET user_text=%(text)s WHERE user_id=%(user_id)s AND text_id = %(id)s AND project_name = %(name)s;
    INSERT INTO ali_ag_db.users (text_id, user_id, user_text,project_name)
       SELECT %(id)s, %(user_id)s, %(text)s, %(name)s
       WHERE NOT EXISTS (SELECT 1 FROM ali_ag_db.users WHERE user_id=%(user_id)s AND text_id = %(id)s AND project_name = %(name)s);''',{'id':id , 'user_id':user_id,'text':f'{text}','name':f'{name}'})
    con.commit()
    cur.close()


def changename(user_id,name,change):
    cur = con.cursor()
    cur.execute('''UPDATE ali_ag_db.projects SET project_name=%(change)s
                WHERE user_id=%(user_id)s AND project_name = %(name)s''',{'change':f'{change}' , 'user_id':user_id, 'name':f'{name}'})

    cur.execute('''UPDATE ali_ag_db.users SET project_name=%(change)s
                    WHERE user_id=%(user_id)s AND project_name = %(name)s''',
                {'change':f'{change}' , 'user_id':user_id, 'name':f'{name}'})
    con.commit()
    cur.close()


def delete_project(user_id,name):
    cur = con.cursor()
    cur.execute('''DELETE FROM ali_ag_db.users
                 WHERE user_id = %(user_id)s AND project_name=%(name)s''',{'user_id':user_id, 'name':f'{name}'})

    cur.execute('''DELETE FROM ali_ag_db.projects
                 WHERE user_id = %(user_id)s AND project_name=%(name)s''',{'user_id':user_id, 'name':f'{name}'})
    con.commit()
    cur.close()