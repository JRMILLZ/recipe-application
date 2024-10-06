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
theme_path = r'C:\Users\Jon\PycharmProjects\recipe_app\Forest-ttk-theme-master\Forest-ttk-theme-master\forest-light.tcl'

# Import the theme file
try:
    root.tk.call('source', theme_path)
    ttk.Style().theme_use('forest-light')
except Exception as e:
    messagebox.showerror("Error", f"Failed to load theme: {e}")

# Function to fetch the total number of recipes
def fetch_recipe_counts_total():
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(DISTINCT id) FROM recipes")
    total_count = cursor.fetchone()[0]
    conn.close()
    return total_count

# Create the dashboard layout
def create_dashboard():
    # Clear the main window
    for widget in root.winfo_children():
        widget.destroy()

    # Create a frame to contain the buttons and align it to the top-left corner
    button_frame = tk.Frame(root)
    button_frame.pack(anchor='nw', padx=10, pady=10)  # Padding for spacing from edges

    # Create the View Recipes button
    view_recipes_button = ttk.Button(button_frame, text="View Recipes", command=view_recipes)
    view_recipes_button.pack(side=tk.TOP, anchor='w', fill=tk.X, pady=2)

    # Create the Add Recipes button
    add_recipes_button = ttk.Button(button_frame, text="Add Recipes", command=lambda: messagebox.showinfo("Info", "Add Recipes functionality not implemented yet."))
    add_recipes_button.pack(side=tk.TOP, anchor='w', fill=tk.X, pady=2)

    # Add the Exit button
    exit_button = ttk.Button(button_frame, text="Exit", command=root.destroy)
    exit_button.pack(side=tk.TOP, anchor='w', fill=tk.X, pady=2)

    # Card-like display for total number of recipes
    total_recipes_frame = ttk.LabelFrame(root, text="Total # of Recipes", padding=(20,10))
    total_recipes_frame.pack(pady=10)

    # Fetch total recipes count and display it in the label
    total_recipes_label = tk.Label(total_recipes_frame, font=("Arial", 24), fg="black")
    total_recipes_label.pack()
    total_recipes = fetch_recipe_counts_total()
    total_recipes_label.config(text=str(total_recipes))

    # Display the pie chart
    show_pie_chart()

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

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()

# Function to switch to the recipe viewing page
def view_recipes():
    for widget in root.winfo_children():
        widget.destroy()

    # Button to go back to the dashboard
    back_button = ttk.Button(root, text="Back", command=create_dashboard)
    back_button.pack(anchor='nw', padx=10, pady=10)

    # Category selection
    category_label = tk.Label(root, text="Select Category:")
    category_label.pack()
    categories = ['Dinner', 'Breakfast', 'Lunch']
    category_combobox = ttk.Combobox(root, values=categories)
    category_combobox.pack()

    recipe_listbox = tk.Listbox(root, width=30, height=10)
    recipe_listbox.pack()

    details_frame = tk.Frame(root)
    details_frame.pack()
    details_text = tk.Text(details_frame, width=75, height=10)
    details_text.pack(side=tk.LEFT)
    scrollbar = tk.Scrollbar(details_frame, command=details_text.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    details_text['yscrollcommand'] = scrollbar.set

    # Functions for recipe details
    def fetch_recipes(category):
        conn = sqlite3.connect('recipes.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM recipes WHERE main_category = ?", (category,))
        recipes = cursor.fetchall()
        conn.close()
        return [recipe[0] for recipe in recipes]

    def fetch_recipe_details(recipe_name):
        conn = sqlite3.connect('recipes.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT ingredient, quantity, unit FROM ingredients WHERE recipe_id = (SELECT id FROM recipes WHERE name = ?)",
            (recipe_name,))
        ingredients = cursor.fetchall()
        cursor.execute(
            "SELECT step_order, step_text FROM steps WHERE recipe_id = (SELECT id FROM recipes WHERE name = ?) ORDER BY step_order",
            (recipe_name,))
        steps = cursor.fetchall()
        conn.close()
        return ingredients, steps

    def display_recipe(event):
        try:
            recipe_name = recipe_listbox.get(recipe_listbox.curselection())
            ingredients, steps = fetch_recipe_details(recipe_name)

            details_text.delete(1.0, tk.END)
            details_text.insert(tk.END, f"Ingredients for {recipe_name}:\n")
            for ingredient in ingredients:
                details_text.insert(tk.END, f"- {ingredient[1]} {ingredient[2]} of {ingredient[0]}\n")
            details_text.insert(tk.END, "\nSteps:\n")
            for step in steps:
                details_text.insert(tk.END, f"{step[0]}. {step[1]}\n")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def update_recipes(event):
        selected_category = category_combobox.get()
        recipes = fetch_recipes(selected_category)
        recipe_listbox.delete(0, tk.END)
        for recipe in recipes:
            recipe_listbox.insert(tk.END, recipe)

    category_combobox.bind("<<ComboboxSelected>>", update_recipes)
    recipe_listbox.bind("<<ListboxSelect>>", display_recipe)
    category_combobox.current(0)
    update_recipes(None)

# Initialize dashboard
create_dashboard()
root.mainloop()






