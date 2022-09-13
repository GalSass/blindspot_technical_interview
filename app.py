from flask import Flask, request, render_template
import pandas as pd
from geopy.geocoders import Nominatim
from geopy import distance
import matplotlib as mpl

geolocator = Nominatim(user_agent="app.py")
app = Flask(__name__)

@app.route('/')
def starbucks_finder():
    return render_template("starbucks_finder.html")


@app.route('/data/', methods=['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"Illegal request"
    if request.method == 'POST':
        form_data = request.form
        print(form_data['Address'], form_data['Distance'])
        table = run_search(form_data['Address'], form_data['Distance'])
        return render_template('data.html', table=table)


def starbucks_locations():
    sb_locations = pd.read_csv("Starbuckslocation.csv", sep=",", on_bad_lines="skip",
                               usecols=["StarbucksId", "Name", "Street1", "City", "CountrySubdivisionCode",
                                        "CountryCode",
                                        "Longitude", "Latitude"])
    sb_locations['point'] = sb_locations[['Latitude', 'Longitude']].apply(lambda x: ', '.join(x[x.notnull()]), axis=1)

    return sb_locations


def get_coordinates(address):
    try:
        coords = geolocator.geocode(address)
        return coords.latitude, coords.longitude
    except:
        print("Could not locate the given address")


def check_relevant_distance(sb_locations, coords, radius):
    relevant_sb_indexes = []
    distance_list = []
    for i in sb_locations.index:
        try:
            if distance.distance(coords, sb_locations['point'][i]).km < float(radius):
                relevant_sb_indexes.append(i)
        except:
            continue
    return relevant_sb_indexes


def create_relevant_table(sb_locations, relevant_sb_indexes):
    relevant_sb_df = sb_locations.iloc[relevant_sb_indexes]
    return relevant_sb_df

def df_to_html(relevant_sb_df):
    decorated_df = relevant_sb_df.style.set_properties(**{'color': 'black', 'background': 'white','axis-color': 'grey'})
    html_table = decorated_df.to_html(header="true", table_id="relevant_sb_df")
    return html_table


def run_search(address, distance_from_sb):
    sb_locations = starbucks_locations()
    while True:
        address = address
        radius = distance_from_sb
        coords = (get_coordinates(address))
        if coords is None:
            pass
        else:
            relevant_sb_indexes = check_relevant_distance(sb_locations, coords, radius)
            if not relevant_sb_indexes:
                pass
            else:
                break

    relevant_sb_df = create_relevant_table(sb_locations, relevant_sb_indexes)
    return df_to_html(relevant_sb_df)


if __name__ == '__main__':
    app.run(debug=True)

