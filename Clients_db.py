import psycopg2

def create_db(conn):
    cur.execute("""
        DROP TABLE phone;
        DROP TABLE client;
        """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS client(
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(40) UNIQUE,
            last_name VARCHAR(40) UNIQUE,
            email VARCHAR(40) UNIQUE
        );
        """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS phone(
            id SERIAL PRIMARY KEY,
            client_id INTEGER NOT NULL REFERENCES client(id),
            number VARCHAR(16) UNIQUE NOT NULL
        );
        """)

    conn.commit()

def add_client(conn, first_name, last_name, email, phone=None):
    cur.execute("""
            INSERT INTO client(first_name, last_name, email)
            VALUES(%s, %s, %s) RETURNING id, first_name, last_name, email
            ;
            """, (first_name, last_name, email,))

    print(cur.fetchall())

def add_phone(conn, client_id, number):
    cur.execute("""
            INSERT INTO phone(client_id, number)
            VALUES(%s, %s) RETURNING id, client_id, number
            ;
            """, (client_id, number))

    print(cur.fetchall())

def change_client(conn, id, first_name=None, last_name=None, email=None, phone=None):
    if phone != None:
        cur.execute("""
                UPDATE phone
                SET number = %s
                WHERE id = %s
                """, (phone, id))
    else:
        pass

    if email != None:
        cur.execute("""
                UPDATE client
                SET email = %s
                WHERE id = %s
                """, (email, id))
    else:
        pass

        if last_name != None:
            cur.execute("""
                    UPDATE client
                    SET last_name = %s
                    WHERE id = %s
                    """, (last_name, id))
        else:
            pass

        if first_name != None:
            cur.execute("""
                    UPDATE client
                    SET first_name = %s
                    WHERE id = %s
                    """, (first_name, id))
        else:
            pass

    cur.execute("""
             SELECT * FROM client;
             """)
    print(cur.fetchall())

def delete_phone(conn, client_id, phone):
    cur.execute("""
           DELETE FROM phone WHERE id=%s or number=%s;
           """, (client_id, phone))
    cur.execute("""
           SELECT * FROM phone;
           """)
    print(cur.fetchall())

def delete_client(conn, id):
    cur.execute("""
               DELETE FROM client WHERE id=%s;
               """, (id,))
    cur.execute("""
               SELECT * FROM client;
               """)

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    data = {}
    if first_name:
        data['first_name'] = first_name
    if last_name:
        data['last_name'] = last_name
    if email:
        data['email'] = email
    if phone:
        data['number'] = phone

    query = """SELECT first_name, last_name, email, phone.number FROM client c
            JOIN phone ON c.id  = phone.client_id
            WHERE """ + ' and '.join(f"{k} like '{v}'" for k, v in data.items())

    cur.execute(query)
    print(cur.fetchall())


with psycopg2.connect(database="clients_db", user="postgres", password="postgres") as conn:
    with conn.cursor() as cur:
        create_db(conn)
        add_client(conn, 'Tom', 'Delong', 'delong@blink.com')
        add_phone(conn, 1, '89091234695')
        change_client(conn, 1, 'Василий', 'Пупкин', None, None)
        delete_phone(conn, 1, None)
        delete_client(conn, 1)
        find_client(conn, 'Tom')

conn.close()