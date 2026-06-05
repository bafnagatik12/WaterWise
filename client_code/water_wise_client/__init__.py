from ._anvil_designer import water_wise_clientTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server


class water_wise_client(water_wise_clientTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.country_data = None
    self.load_countries()
    self.drop_down_1.set_event_handler('change', self.drop_down_1_change)
    self.button_1.set_event_handler('click', self.button_1_click)

  def load_countries(self):
    try:
      countries = anvil.server.call("get_countries_list")
      self.drop_down_1.items = countries
      self.drop_down_1.selected_value = None
    except Exception as e:
      print("Error loading countries:", e)

  def drop_down_1_change(self, **event_args):
    country_code = self.drop_down_1.selected_value
    if not country_code:
      return

    data = anvil.server.call("get_country_data", country_code)
    self.country_data = data

    if data:
      self.label_country.text = data["country_name"]

      safety = int(data['safety_score']) if data['safety_score'] else None
      stress_percent = round(data['stress_level'], 3)
      usage = round(data['water_usage'], 3) * 1000

      if safety:
        self.label_safety.text = "Safety Score: " + str(safety) + "/5"
      else:
        self.label_safety.text = "Safety Score: -/5"

      if safety in [1, 2]:
        self.label_safety.foreground = "red"
      elif safety == 3:
        self.label_safety.foreground = "orange"
      elif safety in [4, 5]:
        self.label_safety.foreground = "green"

      self.label_safety.text += "\nHow safe the water is to use. Lower scores mean the water may not be safe, while higher scores mean it is cleaner and safer."

      self.label_stress.text = "Water Stress Level: " + str(stress_percent) + "%"
      if stress_percent < 33:
        self.label_stress.foreground = "green"
      elif stress_percent <= 66:
        self.label_stress.foreground = "orange"
      else:
        self.label_stress.foreground = "red"
      self.label_stress.text += "\nShows how much of a country's water supply is being used. Higher values mean the country is using more of its available water."

      self.label_usage.text = "Average Water Usage: " + str(usage) + " Liters/person/day"
      self.label_usage.text += "\nThe average total freshwater withdrawn per person per day in this country, including agricultural, industrial, and household use."

  def button_1_click(self, **event_args):
    self.label_6.text = ""
    self.label_7.text = ""
    self.label_8.text = ""

    numberDays = self.text_box_1.text
    numberShowers = self.text_box_2.text
    averageDuration = self.text_box_3.text

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
    except Exception:
      alert("Enter valid numbers")
      return

    country_code = self.country_data["country_code"]

    donation = anvil.server.call("get_donation_amount", country_code, days, showers, duration)
    self.label_9.text = "Suggested Donation to Offset Water Use: $" + "{:.2f}".format(donation)

    breakdown = anvil.server.call("calculate_traveler_footprint_breakdown", days, showers, duration)
    country_daily = self.country_data["water_usage"] * 1000

    self.show_chart(breakdown, country_daily)

  def show_chart(self, breakdown, country_daily):
    traveler_label = "Your Daily Water Footprint"
    country_label = "Local Person's Daily Footprint"

    direct = round(breakdown["shower"] + breakdown["hygiene"], 1)
    food = round(breakdown["food"], 1)
    hotel = round(breakdown["hotel"], 1)
    total = round(breakdown["total"], 1)
    country_val = round(country_daily, 1)

    bar1 = go.Bar(
      name="Showers & Hygiene",
      x=[traveler_label, country_label],
      y=[direct, 0],
      marker_color="#1a6faf"
    )

    bar2 = go.Bar(
      name="Food (Virtual Water)",
      x=[traveler_label, country_label],
      y=[food, 0],
      marker_color="#5ba4d4"
    )

    bar3 = go.Bar(
      name="Hotel & Services",
      x=[traveler_label, country_label],
      y=[hotel, 0],
      marker_color="#a8d4f0"
    )

    bar4 = go.Bar(
      name="Local Total Footprint",
      x=[traveler_label, country_label],
      y=[0, country_val],
      marker_color="#e07b20"
    )

    fig = go.Figure(data=[bar1, bar2, bar3, bar4])

    fig.update_layout(
      barmode="stack",
      title="Your Daily Water Footprint vs. A Local Person's (Liters)",
      yaxis_title="Liters per Day"
    )

    self.plot_1.figure = fig