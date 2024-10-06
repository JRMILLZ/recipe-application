import sqlite3

# Connect to the new database
conn = sqlite3.connect('recipes.db')
cursor = conn.cursor()

# Create the recipes table with main_category and sub_category columns
cursor.execute('''
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        main_category TEXT NOT NULL,
        sub_category TEXT
    )
''')

# Create the ingredients table with separate quantity and unit columns
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_id INTEGER,
        ingredient TEXT NOT NULL,
        quantity REAL,
        unit TEXT,
        FOREIGN KEY (recipe_id) REFERENCES recipes (id)
    )
''')

# Create the steps table to store recipe steps in order
cursor.execute('''
    CREATE TABLE IF NOT EXISTS steps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_id INTEGER,
        step_order INTEGER,
        step_text TEXT NOT NULL,
        FOREIGN KEY (recipe_id) REFERENCES recipes (id)
    )
''')

conn.commit()
conn.close()

print("New database structure created with main_category and sub_category columns.")

