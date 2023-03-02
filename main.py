import tkinter as tk
import requests
import mysql.connector as mysql
from tkcalendar import Calendar, DateEntry
import datetime
from tkinter import ttk

db = mysql.connect(
    host="localhost",
    user="root",
    password="200463",
    database="gym"
)

cursor = db.cursor()


def calendar():
  second_window = tk.Toplevel()
  second_window.title("Calendar with Events")
  def get_events(date):
    events_list.delete(0, tk.END)
    query = "SELECT event FROM events WHERE date = %s"
    cursor.execute(query, (date,))
    rows = cursor.fetchall()
    for row in rows:
        events_list.insert(tk.END, row[0])

    # Define a function to add an event to the database
  def add_event():
    date = datetime.datetime(int(cal.get_date().split("/")[1]),int(cal.get_date().split("/")[0]),int(cal.get_date().split("/")[2]))
    event = event_entry.get()
    query = "INSERT INTO events (date, event) VALUES (%s, %s)"
    cursor.execute(query, (date, event))
    db.commit()
    get_events(date)
  # Create the calendar widget
  cal = Calendar(second_window, selectmode="day", year=2023, month=3, day=1)
  cal.pack()

# TODO: Add dedicated fields for "weight, calorie intake, etc."
  # Create the event entry widget
  event_entry = tk.Entry(second_window)
  event_entry.pack()

  # Create the add event button
  add_button = tk.Button(second_window, text="Add Event", command=add_event)
  add_button.pack()

  # Create the events list widget
  events_list = tk.Listbox(second_window)
  events_list.pack()

  # Bind the calendar widget to the get_events function
  cal.bind("<<CalendarSelected>>", lambda event: get_events(datetime.datetime(int(cal.get_date().split("/")[1]),int(cal.get_date().split("/")[0]),int(cal.get_date().split("/")[2]))))




def calculate_bmi(weight, height):
  # Calculate BMI
  bmi = weight / (height ** 2)
  return bmi

def onExit(self):
  self.quit()

def calculate_calorie_intake(bmr, activity_level):
  # Calculate calorie intake based on BMR and activity level
  if activity_level == "sedentary":
    calorie_intake = bmr * 1.2
  elif activity_level == "lightly active":
    calorie_intake = bmr * 1.375
  elif activity_level == "moderately active":
    calorie_intake = bmr * 1.55
  elif activity_level == "very active":
    calorie_intake = bmr * 1.725
  elif activity_level == "extra active":
    calorie_intake = bmr * 1.9
  else:
    calorie_intake = 0
  return calorie_intake

def calculate_bmr(weight, height, age, gender):
  # Calculate BMR using the Harris-Benedict equation
  if gender == "male":
    bmr = 66 + (6.3 * weight) + (12.9 * height) - (6.8 * age)
  elif gender == "female":
    bmr = 655 + (4.3 * weight) + (4.7 * height) - (4.7 * age)
  else:
    bmr = 0
  return bmr

def get_nutrition_info(food):
  # Use an API to retrieve nutrition information for the specified food
  api_key = "5e214b5995a7385cd7308a1e622e96e9"
  base_url = "https://api.edamam.com/api/food-database/parser"
  params = {
    "ingr": food,
    "app_id": "c35c66c1",
    "app_key": api_key
  }
  response = requests.get(base_url, params=params)
  data = response.json()
  nutrition_info = {}
  if "error" not in data:
    # Extract nutrition information from the API response
    nutrition_info["calories"] = data["parsed"][0]["food"]["nutrients"]["ENERC_KCAL"]
    nutrition_info["fat"] = data["parsed"][0]["food"]["nutrients"]["FAT"]
    nutrition_info["carbohydrates"] = data["parsed"][0]["food"]["nutrients"]["CHOCDF"]
    nutrition_info["protein"] = data["parsed"][0]["food"]["nutrients"]["PROCNT"]
  return nutrition_info

def calculate_button_clicked():
  # Calculate BMI, calorie intake, and BMR when the calculate button is clicked
  weight = float(weight_entry.get())
  height = float(height_entry.get())
  age = int(age_entry.get())
  gender =gender_variable.get()
  activity_level = activity_level_variable.get()
  bmi = calculate_bmi(weight, height)
  bmr = calculate_bmr(weight, height, age, gender)
  calorie_intake = calculate_calorie_intake(bmr, activity_level)
  food = food_entry.get()
  nutrition_info = get_nutrition_info(food)
  # Display the results
  bmi_label.config(text="BMI: {:.2f}".format(bmi))
  calorie_intake_label.config(text="Calorie intake: {:.2f}".format(calorie_intake))
  bmr_label.config(text="BMR: {:.2f}".format(bmr))
  calories_label.config(text="Calories: {:.2f}".format(nutrition_info["calories"]))
  fat_label.config(text="Fat: {:.2f} g".format(nutrition_info["fat"]))
  carbs_label.config(text="Carbohydrates: {:.2f} g".format(nutrition_info["carbohydrates"]))
  protein_label.config(text="Protein: {:.2f} g".format(nutrition_info["protein"]))

# Create the main window
window = tk.Tk()
window.title("BMI Calculator")

# Create the input fields
weight_label = tk.Label(text="Weight (kg)")
weight_label.grid(row=0, column=0)
weight_entry = tk.Entry()
weight_entry.grid(row=0, column=1)

height_label = tk.Label(text="Height (m)")
height_label.grid(row=1, column=0)
height_entry = tk.Entry()
height_entry.grid(row=1, column=1)

age_label = tk.Label(text="Age (years)")
age_label.grid(row=2, column=0)
age_entry = tk.Entry()
age_entry.grid(row=2, column=1)

gender_label = tk.Label(text="Gender")
gender_label.grid(row=3, column=0)
gender_variable = tk.StringVar(window)
gender_variable.set("male")
gender_menu = tk.OptionMenu(window, gender_variable, "male", "female")
gender_menu.grid(row=3, column=1)

activity_level_label = tk.Label(text="Activity level")
activity_level_label.grid(row=4, column=0)
activity_level_variable = tk.StringVar(window)
activity_level_variable.set("sedentary")
activity_level_menu = tk.OptionMenu(window, activity_level_variable, "sedentary", "lightly active", "moderately active", "very active", "extra active")
activity_level_menu.grid(row=4, column=1)

food_label = tk.Label(text="Food")
food_label.grid(row=5, column=0)
food_entry = tk.Entry()
food_entry.grid(row=5, column=1)

# Create the calculate button
calculate_button = tk.Button(text="Calculate", command=calculate_button_clicked)
calculate_button.grid(row=6, column=0, columnspan=2)

# Create the result labels
bmi_label = tk.Label(text="BMI:")
bmi_label.grid(row=7, column=0)
calorie_intake_label = tk.Label(text="Calorie intake:")
calorie_intake_label.grid(row=8, column=0)
bmr_label = tk.Label(text="BMR:")
bmr_label.grid(row=9, column=0)
calories_label = tk.Label(text="Calories:")
calories_label.grid(row=7, column=1)
fat_label = tk.Label(text="Fat:")
fat_label.grid(row=8, column=1)
carbs_label = tk.Label(text="Carbohydrates:")
carbs_label.grid(row=9, column=1)
protein_label = tk.Label(text="Protein:")
protein_label.grid(row=10, column=1)

menubar = tk.Menu(window.master)

fileMenu = tk.Menu(menubar)
fileMenu.add_command(label="Calendar", command=calendar)
fileMenu.add_command(label="Exit", command=onExit)
menubar.add_cascade(label="File", menu=fileMenu)

window.config(menu=menubar)

# Run the main loop
window.mainloop()

