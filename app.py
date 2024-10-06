import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Create the main Tkinter application
root = tk.Tk()
root.title("Recipe Application")

# Set the absolute path for the theme file
theme_path = r'C:\Users\Jon\PycharmProjects\recipe_app\Forest-ttk-theme-master\Forest-ttk-theme-master\forest-light.tcl'  # or 'forest-dark.tcl'

# Import the theme file
try:
    # Load the theme file
    root.tk.call('source', theme_path)
    ttk.Style().theme_use('forest-light')  # or 'forest-dark'
except Exception as e:
    messagebox.showerror("Error", f"Failed to load theme: {e}")

# Function to fetch the count of recipes for each category
def fetch_recipe_counts():
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    cursor.execute("SELECT main_category, COUNT(*) FROM recipes GROUP BY main_category")
    counts = cursor.fetchall()
    conn.close()
    return dict(counts)

# Function to create the pie chart
def show_pie_chart():
    counts = fetch_recipe_counts()
    categories = list(counts.keys())
    values = list(counts.values())

    fig, ax = plt.subplots()
    ax.pie(values, labels=categories, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Embed the pie chart in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()

    canvas.draw()

# Function to switch to the recipe viewing page
def view_recipes():
    # Clear the main window
    for widget in root.winfo_children():
        widget.destroy()

    # Create a button to go back to the main dashboard
    back_button = ttk.Button(root, text="Back", command=create_dashboard)
    back_button.pack(pady=10)

    # Create the category selection label
    category_label = tk.Label(root, text="Select Category:")
    category_label.pack()

    # Category selection
    categories = ['Dinner', 'Breakfast', 'Lunch']
    category_combobox = ttk.Combobox(root, values=categories)
    category_combobox.pack()

    # Recipe listbox
    recipe_listbox = tk.Listbox(root, width=30, height=10)
    recipe_listbox.pack()

    # Recipe details text area with scrollbar
    details_frame = tk.Frame(root)
    details_frame.pack()

    details_text = tk.Text(details_frame, width=75, height=10)
    details_text.pack(side=tk.LEFT)

    scrollbar = tk.Scrollbar(details_frame, command=details_text.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    details_text['yscrollcommand'] = scrollbar.set

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
        try:
            recipe_name = recipe_listbox.get(recipe_listbox.curselection())
            ingredients, steps = fetch_recipe_details(recipe_name)

            details_text.delete(1.0, tk.END)  # Clear previous text
            details_text.insert(tk.END, f"Ingredients for {recipe_name}:\n")

            for ingredient in ingredients:
                details_text.insert(tk.END, f"- {ingredient[1]} {ingredient[2]} of {ingredient[0]}\n")

            details_text.insert(tk.END, "\nSteps:\n")
            for step in steps:
                details_text.insert(tk.END, f"{step[0]}. {step[1]}\n")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

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

    # Set default category and fetch recipes
    category_combobox.current(0)  # Set to first category (Dinner)
    update_recipes(None)  # Fetch recipes for default category

# Create the dashboard layout
def create_dashboard():
    # Clear the main window
    for widget in root.winfo_children():
        widget.destroy()

    # Create a button to view recipes
    view_recipes_button = ttk.Button(root, text="View Recipes", command=view_recipes)
    view_recipes_button.pack(pady=10)

    # Create a button to add recipes (no functionality yet)
    add_recipes_button = ttk.Button(root, text="Add Recipes", command=lambda: messagebox.showinfo("Info", "Add Recipes functionality not implemented yet."))
    add_recipes_button.pack(pady=10)

    # Display the pie chart
    show_pie_chart()

# Call the dashboard creation function on startup
create_dashboard()

# Run the Tkinter main loop
root.mainloop()




