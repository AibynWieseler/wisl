import psycopg2
import csv
import json

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="1939",
    host="localhost",
    port="5432"
)

cur = conn.cursor() 
def create_tables():
    cur.execute("""
    CREATE TABLE IF NOT EXISTS groups (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) UNIQUE
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) UNIQUE,
        email VARCHAR(100),
        birthday DATE,
        group_id INTEGER REFERENCES groups(id),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS phones (
        id SERIAL PRIMARY KEY,
        contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
        phone VARCHAR(20),
        type VARCHAR(10)
    );
    """)

    conn.commit()

def insert_from_console(): #everything for inserting
    name = input("name: ")
    email = input("email: ")
    birthday = input("birthday (YYYY-MM-DD): ")
    group = input("group: ")

    #insert group
    cur.execute("INSERT INTO groups(name) VALUES (%s) ON CONFLICT DO NOTHING", (group,))
    cur.execute("SELECT id FROM groups WHERE name=%s", (group,))
    gid = cur.fetchone()[0]

    #insert contact
    cur.execute("""
        INSERT INTO contacts(name, email, birthday, group_id)
        VALUES (%s, %s, %s, %s)
        RETURNING id
    """, (name, email, birthday, gid))

    cid = cur.fetchone()[0]

    #multiple phones
    while True:
        phone = input("phone('stop' to stop): ")
        if phone == "stop":
            break
        ptype = input("write (home/work/mobile): ")

        cur.execute("""
            INSERT INTO phones(contact_id, phone, type)
            VALUES (%s, %s, %s)
        """, (cid, phone, ptype))

    conn.commit()

#search, filter
def search_contacts(query):
    cur.execute("SELECT * FROM search_contacts(%s)", (query,))
    for row in cur.fetchall():
        print(row)

def filter_by_group(group):
    cur.execute("""
        SELECT c.name, c.email
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        WHERE g.name = %s
    """, (group,))
    print(cur.fetchall())

def search_email(keyword):
    cur.execute("""
        SELECT name, email FROM contacts
        WHERE email ILIKE %s
    """, ('%' + keyword + '%',))
    print(cur.fetchall())

def sort_contacts(field):
    if field not in ['name', 'birthday', 'created_at']:
        print("Invalid sort field")
        return

    cur.execute(f"SELECT name, email FROM contacts ORDER BY {field}")
    print(cur.fetchall())

#pagination
def paginate():
    page = 0
    limit = 5

    while True:
        cur.execute("SELECT name, email FROM contacts LIMIT %s OFFSET %s",
                    (limit, page * limit))

        rows = cur.fetchall()
        print("\nPage:", page)

        for r in rows:
            print(r)

        cmd = input("next/prev/quit: ")

        if cmd == "next":
            page += 1
        elif cmd == "prev" and page > 0:
            page -= 1
        elif cmd == "quit":
            break

#json export
def export_json():
    cur.execute("""
    SELECT c.name, c.email, c.birthday, g.name,
           json_agg(json_build_object('phone', p.phone, 'type', p.type))
    FROM contacts c
    LEFT JOIN phones p ON c.id = p.contact_id
    LEFT JOIN groups g ON c.group_id = g.id
    GROUP BY c.id, g.name
    """)

    data = cur.fetchall()

    with open("contacts.json", "w") as f:
        json.dump(data, f, default=str, indent=4)

    print("exported to contacts.json")

#import
def import_json():
    with open("contacts.json") as f:
        data = json.load(f)

    for entry in data:
        name, email, birthday, group, phones = entry

        cur.execute("SELECT id FROM contacts WHERE name=%s", (name,))
        exists = cur.fetchone()

        if exists:
            choice = input(f"{name} exists. skip/overwrite? ")
            if choice == "skip":
                continue
            elif choice == "overwrite":
                cur.execute("DELETE FROM contacts WHERE name=%s", (name,))

        #group
        cur.execute("INSERT INTO groups(name) VALUES (%s) ON CONFLICT DO NOTHING", (group,))
        cur.execute("SELECT id FROM groups WHERE name=%s", (group,))
        gid = cur.fetchone()[0]

        #contact
        cur.execute("""
            INSERT INTO contacts(name, email, birthday, group_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (name, email, birthday, gid))

        cid = cur.fetchone()[0]

        #phones
        if phones:
            for p in phones:
                cur.execute("""
                    INSERT INTO phones(contact_id, phone, type)
                    VALUES (%s, %s, %s)
                """, (cid, p['phone'], p['type']))

    conn.commit()
    print("import complete")

#csv import
def import_csv(file_path):
    with open(file_path) as f:
        reader = csv.DictReader(f)

        for row in reader:
            name = row['name']
            email = row['email']
            birthday = row['birthday']
            group = row['group']
            phone = row['phone']
            ptype = row['type']

            cur.execute("INSERT INTO groups(name) VALUES (%s) ON CONFLICT DO NOTHING", (group,))
            cur.execute("SELECT id FROM groups WHERE name=%s", (group,))
            gid = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO contacts(name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (name) DO NOTHING
                RETURNING id
            """, (name, email, birthday, gid))

            result = cur.fetchone()

            if result:
                cid = result[0]
            else:
                cur.execute("SELECT id FROM contacts WHERE name=%s", (name,))
                cid = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s, %s, %s)
            """, (cid, phone, ptype))

    conn.commit()

#stored calls
def add_phone():
    name = input("name: ")
    phone = input("phone: ")
    ptype = input("type: ")

    cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, ptype))
    conn.commit()

def move_group():
    name = input("name: ")
    group = input("new group: ")

    cur.execute("CALL move_to_group(%s, %s)", (name, group))
    conn.commit()

#menu(do i need it tho?)
def menu():
    while True:
        print("""
1. add contact
2. search
3. filter by group
4. search email
5. sort
6. pagination
7. export JSON
8. import JSON
9. import CSV
10. add phone (procedure)
11. move group (procedure)
0. exit
        """)

        choice = input("choose: ")

        if choice == "1":
            insert_from_console()
        elif choice == "2":
            search_contacts(input("query: "))
        elif choice == "3":
            filter_by_group(input("group: "))
        elif choice == "4":
            search_email(input("email keyword: "))
        elif choice == "5":
            sort_contacts(input("sort by: "))
        elif choice == "6":
            paginate()
        elif choice == "7":
            export_json()
        elif choice == "8":
            import_json()
        elif choice == "9":
            import_csv(input("CSV path: "))
        elif choice == "10":
            add_phone()
        elif choice == "11":
            move_group()
        elif choice == "0":
            break


create_tables()
menu()

cur.close()
conn.close()