import requests, json, time

# Define Overpass API URL
OVERPASS_URL = "http://overpass-api.de/api/interpreter"

places = [
    {"name": "Benbecula", "lat": 57.46833301010631, "long": -7.359285555536759},
    {"name": "Barra", "lat": 56.955717226858155,"long": -7.501365917913401},
    {"name": "Mallaig", "lat": 57.005591816840855, "long": -5.832235278415086},
    {"name": "Gairloch", "lat": 57.72883632790659, "long": -5.694005677912755},
    {"name": "Isles of Scilly", "lat": 49.914376, "long": -6.315301},
    {"name": "Inveraray", "lat": 56.231417596356486, "long": -5.072371435294118},
    {"name": "Forfar", "lat": 56.642528, "long": -2.889245},
    {"name": "Abroath", "lat": 56.47852877793694, "long": -3.007638737169701},
    {"name": "Ullapool", "lat": 57.90273078514585, "long": -5.1649214313414555},
    {"name": "Ballater", "lat": 57.05008595786217, "long": -3.0397023381167014},
    {"name": "Luton", "lat": 51.87778678682625, "long": -0.4202599314404703},
    {"name": "Cannock", "lat": 52.66443772604315, "long": -1.0804322657405634},
    {"name": "Crawley", "lat": 51.08101436324684, "long": -0.20192178333333333},
    {"name": "Wednesbury", "lat": 52.55569933273981, "long": -2.012876702859989},
    {"name": "Norris Green", "lat": 53.44457137601863, "long": -2.9298301376560696},
    {"name": "Chingford", "lat": 51.63347179400828, "long": 0.009069325917122555},
    {"name": "Belvedere", "lat": 51.483664948330095, "long": 0.14234896655428858},
    {"name": "Featherstone", "lat": 52.64048874722983, "long": -2.113788045182853},
    {"name": "Speke", "lat": 53.348919, "long": -2.884954},
    {"name": "Wolverhampton", "lat": 52.563445, "long": -2.102172},
]

random_places = [
    {"name": "Yeovil", "lat": 50.943736, "long":-2.660908},
    {"name": "Grantown-On-Spey", "lat": 57.327001, "long": -3.609572},
    {"name": "Bristol (Avonmouth)", "lat": 51.517304, "long":-2.682846},
    {"name": "Boston", "lat": 52.970192, "long":-0.030705},
    {"name": "Hornchurch (London)", "lat": 51.559275, "long":0.220933},
    {"name": "Eastbourne", "lat": 50.782312, "long":0.308939},
    {"name": "Slough (London)", "lat": 51.508845, "long":-0.545246},
    {"name": "Heckmondwike", "lat": 53.707419, "long":-1.671319},
    {"name": "Birmingham (Garretts Green)", "lat": 52.472482, "long":-1.771321},
    {"name": "Nottingham (Chilwell)", "lat": 52.904589, "long":-1.238241},
    {"name": "Rochdale (Manchester)", "lat": 53.609473, "long":-2.138784},
]

results = {}
radius = 6000  # 6km

# Function to make a request to the Overpass API with retry mechanism
def make_request(query):
    max_retries = 5
    retry_delay = 60  # 60 seconds delay between retries
    for attempt in range(max_retries):
        response = requests.get(OVERPASS_URL, params={'data': query})
        if response.status_code == 200:
            print("hit")
            return response.json()
        elif response.status_code == 429:
            print(f"Rate limit exceeded. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
    raise Exception("Max retries exceeded")

# Overpass Query including mini-roundabouts and intersections
for place in random_places:
    query = f"""
    [out:json];
    (
      way(around:{radius}, {place["lat"]}, {place["long"]})["junction"="roundabout"];
      node(around:{radius}, {place["lat"]}, {place["long"]})["highway"="mini_roundabout"];
      way(around:{radius}, {place["lat"]}, {place["long"]})["junction"]["junction"!="roundabout"];
      way(around:{radius}, {place["lat"]}, {place["long"]})["highway"~"primary|trunk"]["lanes"~"[4-9]"];
    );
    out body;
    """
#       node(around:{radius}, {place["lat"]}, {place["long"]});
    try:
        data = make_request(query)

        # Count roundabouts
        roundabout_count = sum(1 for element in data["elements"] if element["type"] == "way" and "junction" in element.get("tags", {}) and element["tags"]["junction"] == "roundabout")

        # Count mini-roundabouts
        mini_roundabout_count = sum(1 for element in data["elements"] if element["type"] == "node" and "highway" in element.get("tags", {}) and element["tags"]["highway"] == "mini_roundabout")

        # Count dual carriageways (primary/trunk roads with at least 2 lanes)
        dual_carriageway_count = sum(1 for element in data["elements"] if element["type"] == "way" and "highway" in element.get("tags", {}) and element["tags"]["highway"] in ["primary", "trunk"] and "lanes" in element.get("tags", {}))

        # Count all junctions except roundabouts
        all_junction_count = sum(1 for element in data["elements"] if element["type"] == "way" and "junction" in element.get("tags", {}) and element["tags"]["junction"] != "roundabout")


        results[place["name"]] = {
            "roundabout_count": roundabout_count,
            "mini_roundabout_count": mini_roundabout_count,
            "dual_carriageway_count": dual_carriageway_count,
            "all_junction_count": all_junction_count,
        }
        print("Successfully processed", place["name"])
    except Exception as e:
        print(f"Error for {place['name']}: {e}")

# Write the random results to a file
with open('results_sorted_random.json', 'w') as file:
    json.dump(results, file, indent=4)

# Write the extreme results to a file
with open('results_sorted.json', 'w') as file:
    json.dump(results, file, indent=4)

print("Results written to results_sorted_random.json and results_sorted.json")