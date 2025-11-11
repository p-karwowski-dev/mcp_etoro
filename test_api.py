import requests
import json

# Fetch data from eToro API
url = "https://api.etorostatic.com/sapi/instrumentsmetadata/V1.1/instruments"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    
    # Print top-level keys
    print("Top-level keys in response:")
    print(data.keys())
    print()
    
    # Print first instrument to see its structure
    if "InstrumentDisplayDatas" in data and len(data["InstrumentDisplayDatas"]) > 0:
        print("First instrument structure:")
        first_instrument = data["InstrumentDisplayDatas"][0]
        print(json.dumps(first_instrument, indent=2))
        print()
        print("Available keys in instrument:")
        print(first_instrument.keys())
    else:
        print("InstrumentDisplayDatas not found or empty")
        print("Available keys:", list(data.keys()))
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
