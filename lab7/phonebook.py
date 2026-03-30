import psycopg2
import csv

conn = psycopg2.connect(dbname = "postgres", user = "postgres", password = "1939", host = "localhost", port = "5432")

cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS phonebook (
    first_name VARCHAR(255),
    phone VARCHAR(20)
);
""")

#csv reading
def insert_from_csv(file_path):
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        for name, phone in reader:
            cur.execute(
                "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                (name, phone)
            )
    conn.commit()

#insert from console
def insert_from_console():
    name = input("enter name: ")
    phone = input("enter phone: ")

    cur.execute(
        "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)",
        (name, phone)
    )
    conn.commit()

#updating
def update_name_by_phone(phone, new_name):
    cur.execute(
        "UPDATE phonebook SET first_name=%s WHERE phone=%s",
        (new_name, phone)
    )
    conn.commit()

#query
def get_all():
    cur.execute("SELECT * FROM phonebook")
    return cur.fetchall()

def find_by_name(name):
    cur.execute(
        "SELECT * FROM phonebook WHERE first_name ILIKE %s",
        (f"%{name}%",)
    )
    return cur.fetchall()

#deleting
def delete_by_phone(phone):
    cur.execute(
        "DELETE FROM phonebook WHERE phone=%s",
        (phone,)
    )
    conn.commit()

insert_from_console()
rows = get_all()
print("\ncurrent phonebook:")
for r in rows:
    print(r)

#update_name_by_phone("77712", "Wiesel") #updating
#print(find_by_name("ali")) #query
#delete_by_phone("87001234567") #deleting


cur.close()
conn.close()