from django.db import connection

with connection.cursor() as cursor:
    cursor.execute('''
        DROP SCHEMA public CASCADE;
        CREATE SCHEMA public;
        GRANT ALL ON SCHEMA public TO postgres;
        GRANT ALL ON SCHEMA public TO public;
    ''')
print("Dropped and recreated public schema.")
