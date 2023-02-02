import psycopg2

def create_db(conn):
    with conn.cursor() as cur:
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
                number INT UNIQUE,
                client_id INTEGER NOT NULL REFERENCES client(id)
            );
            """)

        conn.commit()

def add_client(conn, first_name, last_name, email, phone=None):
    with conn.cursor() as cur:
        cur.execute("""
                INSERT INTO client(first_name, last_name, email)
                VALUES(%s, %s, %s)
                ;
                """, (first_name, last_name, email))

        conn.commit()

def add_phone(conn, client_id, phone):
    pass

def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    pass

def delete_phone(conn, client_id, phone):
    pass

def delete_client(conn, client_id):
    pass

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    pass

def show (conn):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT * FROM client;
        """)
        print('fetchall', cur.fetchall())
    


with psycopg2.connect(database="clients_db", user="postgres", password="postgres") as conn:
    # create_db(conn)
    add_client(conn, 'Tom', 'Delong', 'delong@blink.com', )
    show(conn)


conn.close()