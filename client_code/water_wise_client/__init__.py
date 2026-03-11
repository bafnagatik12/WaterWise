from ._anvil_designer import water_wise_clientTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class water_wise_client(water_wise_clientTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Load countries into dropdown
    self.load_countries()
  def load_countries(self):
    """Load countries into dropdown"""
    try:
      # Get countries from server
      countries = anvil.server.call('get_countries_list')

      # Set dropdown items
      self.drop_down_1.items = countries

    except Exception as e:
      print(f"Error loading countries: {e}")

  @handle('drop_down_1','change')
  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    selected_country_code = self.drop_down_1.selected_value

    if selected_country_code:
      # Find the country name from the dropdown items
      selected_country_name = None
      for name, code in self.drop_down_1.items:
        if code == selected_country_code:
          selected_country_name = name
          break

      if selected_country_name:
        self.label_2.text = f"Selected: {selected_country_name} ({selected_country_code})"
    else:
      self.label_2.text = "No country selected"



