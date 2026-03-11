import anvil.server
import io
import csv
from anvil import app
# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#
COUNTRY_CODES = {
  'AFG': 'Afghanistan', 'ALB': 'Albania', 'DZA': 'Algeria', 'AGO': 'Angola', 'ATG': 'Antigua and Barbuda',
  'ARG': 'Argentina', 'ARM': 'Armenia', 'AUS': 'Australia', 'AUT': 'Austria', 'AZE': 'Azerbaijan',
  'BHR': 'Bahrain', 'BGD': 'Bangladesh', 'BRB': 'Barbados', 'BLR': 'Belarus', 'BEL': 'Belgium',
  'BLZ': 'Belize', 'BEN': 'Benin', 'BTN': 'Bhutan', 'BOL': 'Bolivia', 'BWA': 'Botswana',
  'BRA': 'Brazil', 'BGR': 'Bulgaria', 'BFA': 'Burkina Faso', 'BDI': 'Burundi', 'CPV': 'Cape Verde',
  'KHM': 'Cambodia', 'CMR': 'Cameroon', 'CAN': 'Canada', 'CAF': 'Central African Republic', 'TCD': 'Chad',
  'CHL': 'Chile', 'CHN': 'China', 'COL': 'Colombia', 'COM': 'Comoros', 'CRI': 'Costa Rica',
  'HRV': 'Croatia', 'CUB': 'Cuba', 'CYP': 'Cyprus', 'CZE': 'Czech Republic', 'DNK': 'Denmark',
  'DOM': 'Dominican Republic', 'ECU': 'Ecuador', 'SLV': 'El Salvador', 'ERI': 'Eritrea', 'EST': 'Estonia',
  'SWZ': 'Eswatini', 'ETH': 'Ethiopia', 'FJI': 'Fiji', 'FIN': 'Finland', 'FRA': 'France',
  'GAB': 'Gabon', 'GEO': 'Georgia', 'DEU': 'Germany', 'GHA': 'Ghana', 'GRC': 'Greece',
  'GTM': 'Guatemala', 'GIN': 'Guinea', 'GNB': 'Guinea-Bissau', 'GUY': 'Guyana', 'HTI': 'Haiti',
  'HND': 'Honduras', 'HUN': 'Hungary', 'ISL': 'Iceland', 'IND': 'India', 'IDN': 'Indonesia',
  'IRQ': 'Iraq', 'IRL': 'Ireland', 'ISR': 'Israel', 'ITA': 'Italy', 'JAM': 'Jamaica',
  'JPN': 'Japan', 'JOR': 'Jordan', 'KAZ': 'Kazakhstan', 'KEN': 'Kenya', 'KWT': 'Kuwait',
  'KGZ': 'Kyrgyzstan', 'LVA': 'Latvia', 'LBN': 'Lebanon', 'LSO': 'Lesotho', 'LBR': 'Liberia',
  'LBY': 'Libya', 'LTU': 'Lithuania', 'LUX': 'Luxembourg', 'MDG': 'Madagascar', 'MWI': 'Malawi',
  'MYS': 'Malaysia', 'MLI': 'Mali', 'MLT': 'Malta', 'MRT': 'Mauritania', 'MUS': 'Mauritius',
  'MEX': 'Mexico', 'MNG': 'Mongolia', 'MAR': 'Morocco', 'MOZ': 'Mozambique', 'MMR': 'Myanmar',
  'NAM': 'Namibia', 'NPL': 'Nepal', 'NLD': 'Netherlands', 'NZL': 'New Zealand', 'NIC': 'Nicaragua',
  'NER': 'Niger', 'NGA': 'Nigeria', 'MKD': 'North Macedonia', 'NOR': 'Norway', 'OMN': 'Oman',
  'PAK': 'Pakistan', 'PAN': 'Panama', 'PRY': 'Paraguay', 'PER': 'Peru', 'PHL': 'Philippines',
  'POL': 'Poland', 'PRT': 'Portugal', 'QAT': 'Qatar', 'MDA': 'Moldova', 'ROU': 'Romania',
  'RUS': 'Russia', 'RWA': 'Rwanda', 'STP': 'São Tomé and Príncipe', 'SAU': 'Saudi Arabia',
  'SEN': 'Senegal', 'SRB': 'Serbia', 'SLE': 'Sierra Leone', 'SVK': 'Slovakia', 'SVN': 'Slovenia',
  'ZAF': 'South Africa', 'SSD': 'South Sudan', 'ESP': 'Spain', 'LKA': 'Sri Lanka', 'SDN': 'Sudan',
  'SUR': 'Suriname', 'SWE': 'Sweden', 'CHE': 'Switzerland', 'SYR': 'Syria', 'TJK': 'Tajikistan',
  'THA': 'Thailand', 'TLS': 'Timor-Leste', 'TGO': 'Togo', 'TTO': 'Trinidad and Tobago',
  'TUN': 'Tunisia', 'TUR': 'Turkey', 'TKM': 'Turkmenistan', 'UGA': 'Uganda', 'UKR': 'Ukraine',
  'ARE': 'United Arab Emirates', 'GBR': 'United Kingdom', 'TZA': 'Tanzania', 'USA': 'United States',
    'URY': 'Uruguay', 'UZB': 'Uzbekistan', 'VNM': 'Vietnam', 'ZMB': 'Zambia', 'ZWE': 'Zimbabwe'
}

# Load country data from CSV file in Data Files
def load_country_data():
  """Load country data from CSV file stored in Anvil Data Files"""
  try:
    # Get the CSV file from Data Files
    csv_file = app.get_asset('WaterWise_db (1).csv')

    # Read the CSV content
    csv_content = csv_file.get_bytes().decode('utf-8')
    csv_reader = csv.DictReader(io.StringIO(csv_content))

    countries_data = {}
    for row in csv_reader:
      country_code = row['Country_Code']
      country_name = COUNTRY_CODES.get(country_code, country_code)

      countries_data[country_code] = {
        'country_code': country_code,
        'country_name': country_name,
        'safety_score': float(row['Safety_Score']) if row['Safety_Score'] else 0,
        'stress_level': float(row['Stress_Level']) if row['Stress_Level'] else 0,
        'water_usage': float(row['Average_Usage']) if row['Average_Usage'] else 0
      }

    return countries_data
  except Exception as e:
    print(f"Error loading CSV data: {str(e)}")
    return {}# Cache the data when server starts
COUNTRIES_DATA = load_country_data()
@anvil.server.callable
def get_countries_list():
  countries = []
  for country_code, country_name in COUNTRY_CODES.items():
    countries.append((country_name, country_code))
  return countries

