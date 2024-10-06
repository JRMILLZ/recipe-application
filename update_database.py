import os

# Delete the existing database file
db_file = 'recipes.db'
if os.path.exists(db_file):
    os.remove(db_file)
    print("Database deleted.")
else:
    print("No database file found.")
