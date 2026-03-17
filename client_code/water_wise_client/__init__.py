from ._anvil_designer import water_wise_clientTemplate
from anvil import *
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

      self.label_2.text = f"Selected: {data['country_name']} ({data['country_code']})"

      self.label_country.text = data["country_name"]

      self.label_safety.text = f"Safety Score: {data['safety_score']}"

      self.label_stress.text = f"Stress Level: {data['stress_level']}"

      self.label_usage.text = f"Average Water Usage: {data['water_usage']}"

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
    self.label_9.text = f"Suggested Donation: ${donation:.2f}"