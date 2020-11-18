import json
import csv
import urllib.request
with urllib.request.urlopen("https://<any_website_link>") as url:
    data = json.loads(url.read().decode())

fname = "name.csv"

with open(fname, "w") as file:
    csv_file = csv.writer(file)
    csv_file.writerow(["scope","date","city","time"])
    for item in data["raw_data"]:
        csv_file.writerow([item['scope'],item['date'],item['city'],item['time']])




    fname = "route.csv"
    df = pd.json_normalize(data)
    df.to_csv(fname, "a", index=False)

    df = pd.json_normalize(parameters)