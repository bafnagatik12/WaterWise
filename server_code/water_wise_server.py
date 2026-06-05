import anvil.server
import io
import csv
from anvil.files import data_files

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


def load_country_data():
  print("load country data called")
  try:
    with data_files.open('WaterWise_db (1).csv', 'rb') as f:
      csv_content = f.read().decode('utf-8')
      csv_reader = csv.DictReader(io.StringIO(csv_content))
      countries_data = {}
      for row in csv_reader:
        country_code = row['Country_Code']
        country_name = COUNTRY_CODES.get(country_code, country_code)
        countries_data[country_code] = {
          "country_code": country_code,
          "country_name": country_name,
          "safety_score": float(row['Safety_Score']) if row['Safety_Score'] else 0,
          "stress_level": float(row['Stress_Level']) if row['Stress_Level'] else 0,
          "water_usage": (float(row['Average_Usage']) * 10**9 / float(row['Population']) / 365) if row['Average_Usage'] and row['Population'] else 0,
          "water_value": float(row['Water_Value']) if row['Water_Value'] else 0
        }
      print(countries_data)
      return countries_data
  except Exception as e:
    print("Error loading CSV data:", e)
    return {}


COUNTRIES_DATA = load_country_data()


@anvil.server.callable
def get_countries_list():
  countries = []
  for code, name in COUNTRY_CODES.items():
    if code in COUNTRIES_DATA:
      countries.append((name, code))
  countries.sort(key=lambda x: x[0])
  return countries


@anvil.server.callable
def get_country_data(country_code):
  return COUNTRIES_DATA.get(country_code)


@anvil.server.callable
def get_donation_amount(country_code, days, showers, avgShowerDuration):
  if country_code not in COUNTRIES_DATA:
    return 0

  country = COUNTRIES_DATA[country_code]

  # Full daily footprint in m3 — same components as the chart
  shower_daily_m3 = (showers * avgShowerDuration * 12) / days / 1000
  hygiene_daily_m3 = 0.080
  food_daily_m3 = 2.500
  hotel_daily_m3 = 0.150

  total_daily_m3 = shower_daily_m3 + hygiene_daily_m3 + food_daily_m3 + hotel_daily_m3
  total_m3 = total_daily_m3 * days

  # NGO delivery cost baseline: $2.50/m3
  base_cost = 2.50

  stress = country.get("stress_level", 10)
  if stress > 100:
    scarcity = 2.5
  elif stress > 50:
    scarcity = 1.8
  elif stress > 20:
    scarcity = 1.3
  else:
    scarcity = 1.0

  safety = country.get("safety_score", 3)
  safety_factor = 1.0 + (5 - safety) * 0.15

  donation = total_m3 * base_cost * scarcity * safety_factor
  return round(donation, 2)


@anvil.server.callable
def calculate_traveler_footprint_breakdown(days, showers, avgShowerDuration):
  if days == 0:
    return {"shower": 0, "hygiene": 0, "food": 0, "hotel": 0, "total": 0}

  shower_daily = (showers * avgShowerDuration * 12) / days
  hygiene_daily = 80
  food_daily = 2500
  hotel_daily = 150
  total = shower_daily + hygiene_daily + food_daily + hotel_daily

  return {
    "shower": round(shower_daily, 1),
    "hygiene": float(hygiene_daily),
    "food": float(food_daily),
    "hotel": float(hotel_daily),
    "total": round(total, 1)
  }