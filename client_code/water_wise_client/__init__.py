from ._anvil_designer import water_wise_clientTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server


class water_wise_client(water_wise_clientTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    self.country_data = None

    # Load dropdown items
    self.load_countries()


  def load_countries(self):
    try:
      countries = anvil.server.call("get_countries_list")

      # dropdown format: (label, value)
      self.drop_down_1.items = countries
      self.drop_down_1.selected_value = None

    except Exception as e:
      print("Error loading countries:", e)

  @handle("drop_down_1", "change")
  def drop_down_1_change(self, **event_args):
    print("dropdown function called")

    country_code = self.drop_down_1.selected_value

    if not country_code:
      return

    # call server
    data = anvil.server.call("get_country_data", country_code)

    # save data locally
    self.country_data = data

    if data:

      
      self.label_country.text = data["country_name"]

            # --- FORMAT VALUES ---
      safety = int(data['safety_score']) if data['safety_score'] else None
      stress_percent = round(data['stress_level'], 3)
      usage = (round(data['water_usage'], 3))*1000
      
      # --- SAFETY SCORE ---
      if safety:
        self.label_safety.text = f"Safety Score: {safety}/5"
      else:
        self.label_safety.text = "Safety Score: —/5"
      
      # color logic
      if safety in [1, 2]:
        self.label_safety.foreground = "red"
      elif safety == 3:
        self.label_safety.foreground = "orange"
      elif safety in [4, 5]:
        self.label_safety.foreground = "green"
      
      # user-friendly description
      self.label_safety.text += "\nHow safe the water is to use. Lower scores mean the water may not be safe, while higher scores mean it is cleaner and safer."
      
      # --- STRESS LEVEL ---
      self.label_stress.text = f"Water Stress Level: {stress_percent}%"
      
      if stress_percent < 33:
        self.label_stress.foreground = "green"
      elif stress_percent <= 66:
        self.label_stress.foreground = "orange"
      else:
        self.label_stress.foreground = "red"
      
      self.label_stress.text += "\nShows how much of a country’s water supply is being used. Higher values mean the country is using more of its available water."
      
      # --- WATER USAGE ---
      self.label_usage.text = f"Average Water Usage: {usage} Liters/person/day"
      
      self.label_usage.text += "\nThe average amount of freshwater per capita that a person in this country uses per day. Larger numbers mean higher overall water demand."
  #deals with user input related to calculate button click
  @handle("button_1", "click")
  def button_1_handler(self, **event_args):

    self.label_6.text = ""
    self.label_7.text = ""
    self.label_8.text = ""

    numberDays = self.text_box_1.text
    numberShowers = self.text_box_2.text
    averageDuration = self.text_box_3.text

    # validation
    if not numberDays:
      self.label_6.text = "Please enter the number of days"
      return

    if not numberShowers:
      self.label_7.text = "Please enter the number of showers"
      return

    if not averageDuration:
      self.label_8.text = "Please enter the average shower duration"
      return

    if not self.country_data:
      alert("Please select a country first")
      return

    try:
      days = int(numberDays)
      showers = int(numberShowers)
      duration = float(averageDuration)
    except:
      alert("Enter valid numbers")
      return

    country_code = self.country_data["country_code"]

    #  call server function
    donation = anvil.server.call(
      "get_donation_amount",
      country_code,
      days,
      showers,
      duration
    )

    # display result
    self.label_9.text = f"Suggested Donation to Offset Water Use: ${donation:.2f}"


    # --- USER DAILY USAGE ---
    user_daily = (anvil.server.call(
      "calculate_user_daily_usage",
      days,
      showers,
      duration
    ))*1000
    
    # --- COUNTRY DAILY USAGE ---
    country_yearly = (self.country_data["water_usage"])*1000
    
    # --- DISPLAY TEXT (THIS FIXES WARNING) ---
    
    self.show_chart(user_daily, country_yearly)
  def show_chart(self, traveler_use, local_use):

    fig = go.Figure(
      data=[
        go.Bar(
          x=["Your Daily Water Use", "Average Daily Water Usage of a Person in this Country"],
          y=[traveler_use, local_use],
          text = [round(traveler_use, 3), round(local_use, 3)],
          textposition = "outside",
          marker_color=["#1f77b4", "#ff7f0e"] 
        )
      ]
    )

    fig.update_layout(
      title="Daily Water Use Comparison",
      yaxis_title="Liters per Day"
    )

    self.plot_1.figure = fig



  