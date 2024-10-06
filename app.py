import tkinter as tk
from tkinter import ttk
import sqlite3


# Function to fetch recipes from the database based on the selected category
def fetch_recipes(category):
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM recipes WHERE main_category = ?", (category,))
    recipes = cursor.fetchall()
    conn.close()
    return [recipe[0] for recipe in recipes]


# Function to fetch recipe details (ingredients and steps)
def fetch_recipe_details(recipe_name):
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()

    # Fetch ingredients
    cursor.execute(
        "SELECT ingredient, quantity, unit FROM ingredients WHERE recipe_id = (SELECT id FROM recipes WHERE name = ?)",
        (recipe_name,))
    ingredients = cursor.fetchall()

    # Fetch steps
    cursor.execute(
        "SELECT step_order, step_text FROM steps WHERE recipe_id = (SELECT id FROM recipes WHERE name = ?) ORDER BY step_order",
        (recipe_name,))
    steps = cursor.fetchall()

    conn.close()
    return ingredients, steps


# Function to display recipe details when a recipe is selected
def display_recipe(event):
    recipe_name = recipe_listbox.get(recipe_listbox.curselection())
    ingredients, steps = fetch_recipe_details(recipe_name)

    details_text.delete(1.0, tk.END)  # Clear previous text
    details_text.insert(tk.END, f"Ingredients for {recipe_name}:\n")

    for ingredient in ingredients:
        details_text.insert(tk.END, f"- {ingredient[1]} {ingredient[2]} of {ingredient[0]}\n")

    details_text.insert(tk.END, "\nSteps:\n")
    for step in steps:
        details_text.insert(tk.END, f"{step[0]}. {step[1]}\n")


# Main Tkinter application
root = tk.Tk()
root.title("Recipe Application")

# Category selection
categories = ['Dinner', 'Breakfast', 'Lunch', 'Snack']
category_label = tk.Label(root, text="Select Category:")
category_label.pack()

category_combobox = ttk.Combobox(root, values=categories)
category_combobox.pack()

# Recipe listbox
recipe_listbox = tk.Listbox(root)
recipe_listbox.pack()

# Recipe details text area
details_text = tk.Text(root, width=75, height=15)
details_text.pack()


# Function to update recipe list based on selected category
def update_recipes(event):
    selected_category = category_combobox.get()
    recipes = fetch_recipes(selected_category)
    recipe_listbox.delete(0, tk.END)  # Clear the listbox
    for recipe in recipes:
        recipe_listbox.insert(tk.END, recipe)


# Bind the category selection
category_combobox.bind("<<ComboboxSelected>>", update_recipes)

# Bind the recipe selection
recipe_listbox.bind("<<ListboxSelect>>", display_recipe)

# Run the Tkinter main loop
root.mainloop()


