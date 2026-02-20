import os
import psycopg2
from dotenv import load_dotenv

# Load your secret .env file
load_dotenv()

def create_tables():
    """ Creates tables in the PostgreSQL database """
    commands = (
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            user_name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS projects (
            project_id SERIAL PRIMARY KEY,
            project_name VARCHAR(255) NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id)
                REFERENCES users (user_id)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """
    )
    
    conn = None
    try:
        # Connect using variables from your .env
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            port=os.getenv("DB_PORT")
        )
        cur = conn.cursor()
        
        # Create tables one by one
        for command in commands:
            cur.execute(command)
            
        # Close communication with the PostgreSQL database server
        cur.close()
        # Commit the changes
        conn.commit()
        print("✅ Tables created successfully!")
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"❌ Error: {error}")
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    create_tables()
