import sqlite3

# Create a sqlite3.Connection object and a sqlite3.Cursor object
CONN = sqlite3.connect("dogs.db")
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed
        self.id = None  # We will set this when the object is saved to the database

    @classmethod
    def create_table(cls):
        # Create the dogs table if it doesn't exist
        CURSOR.execute('''CREATE TABLE IF NOT EXISTS dogs (
                           id INTEGER PRIMARY KEY,
                           name TEXT,
                           breed TEXT)''')
        CONN.commit()

    @classmethod
    def drop_table(cls):
        # Drop the dogs table if it exists
        CURSOR.execute("DROP TABLE IF EXISTS dogs")
        CONN.commit()

    def save(self):
        if self.id is None:
            # Insert a new row into the database
            CURSOR.execute("INSERT INTO dogs (name, breed) VALUES (?, ?)",
                           (self.name, self.breed))
            CONN.commit()
            self.id = CURSOR.lastrowid
        else:
            # Update an existing row in the database
            CURSOR.execute("UPDATE dogs SET name=?, breed=? WHERE id=?",
                           (self.name, self.breed, self.id))
            CONN.commit()

    @classmethod
    def create(cls, name, breed):
        # Create a new Dog instance and save it to the database
        dog = cls(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, data):
        # Create a Dog instance from a database row (data)
        dog = cls(data[1], data[2])
        dog.id = data[0]
        return dog

    @classmethod
    def get_all(cls):
        # Retrieve all Dog instances from the database
        CURSOR.execute("SELECT * FROM dogs")
        rows = CURSOR.fetchall()
        dogs = [cls.new_from_db(row) for row in rows]
        return dogs

    @classmethod
    def find_by_name(cls, name):
        # Find a Dog by name and return a Dog instance
        CURSOR.execute("SELECT * FROM dogs WHERE name=?", (name,))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        else:
            return None

    @classmethod
    def find_by_id(cls, id):
        # Find a Dog by ID and return a Dog instance
        CURSOR.execute("SELECT * FROM dogs WHERE id=?", (id,))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        else:
            return None
