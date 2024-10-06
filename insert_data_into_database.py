import os
import csv
import sqlite3

# Step 1: Delete the existing database file if it exists
db_file = 'recipes.db'
if os.path.exists(db_file):
    os.remove(db_file)
    print("Existing database deleted.")

# Step 2: Create the new database structure
conn = sqlite3.connect(db_file)
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

# Commit changes to the database
conn.commit()

# Step 3: Insert recipes from recipes.csv
def insert_recipes_from_csv():
    with open('recipes.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            main_category = row['main_category']
            sub_category = row['sub_category']
            recipe_name = row['name']
            cursor.execute("INSERT INTO recipes (main_category, sub_category, name) VALUES (?, ?, ?)",
                           (main_category, sub_category, recipe_name))

# Step 4: Insert ingredients and steps from ingredients_steps.csv
def insert_ingredients_steps_from_csv():
    with open('ingredients_steps.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            recipe_name = row['recipe_name']
            item = row['ingredient']
            quantity = row['quantity'] if row['quantity'] else None
            unit = row['unit'] if row['unit'] else None
            item_type = row['type']
            step_order = int(row['step_order']) if row['step_order'] else None

            # Get recipe ID
            cursor.execute("SELECT id FROM recipes WHERE name = ?", (recipe_name,))
            recipe_id = cursor.fetchone()
            if recipe_id:
                recipe_id = recipe_id[0]

                if item_type == 'ingredient':
                    cursor.execute("INSERT INTO ingredients (recipe_id, ingredient, quantity, unit) VALUES (?, ?, ?, ?)",
                                   (recipe_id, item, quantity, unit))
                elif item_type == 'step' and step_order is not None:
                    cursor.execute("INSERT INTO steps (recipe_id, step_order, step_text) VALUES (?, ?, ?)",
                                   (recipe_id, step_order, item))

# Insert data from the CSV files
insert_recipes_from_csv()
insert_ingredients_steps_from_csv()

# Commit changes and close the connection
conn.commit()
conn.close()

print("Data inserted successfully!")
