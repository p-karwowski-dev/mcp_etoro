# 0. Setup standard python server environment
# 1. Create algorithm which will hit the eToro API to get instruments data 
# 2. Create local json file as a map of unique instruments

import requests
import json
import sys

def fetch_instruments():
    """Fetch instruments data from eToro API"""
    url = "https://api.etorostatic.com/sapi/instrumentsmetadata/V1.1/instruments"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return None
        
        data = response.json()
        print(f"Fetched {len(data.get('InstrumentDisplayDatas', []))} instruments successfully.")
        return data.get('InstrumentDisplayDatas', [])
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def create_instrument_map(instruments):
    """Create a map of unique instruments with essential information"""
    instrument_map = {}
    
    for instrument in instruments:
        symbol = instrument.get("SymbolFull", "")
        mapped_id = symbol.split('.')[0].split('_')[0]
        
        if mapped_id and mapped_id not in instrument_map:
            instrument_map[mapped_id] = {
                "InstrumentID": instrument.get("InstrumentID"),
                "InstrumentName": instrument.get("InstrumentDisplayName"),
                "InstrumentTypeID": instrument.get("InstrumentTypeID"),
                "Symbol": instrument.get("SymbolFull"),
            }
    
    return instrument_map

def save_to_json(data, filename="instruments.json"):
    """Save instrument map to a local JSON file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(data)} instruments to {filename}")
        return True
    except Exception as e:
        print(f"Error saving to file: {e}")
        return False

def main():
    """Main execution function"""
    print("▶️ Starting...")
    
    # Fetch instruments from API
    instruments = fetch_instruments()
    if not instruments:
        print("Failed to fetch instruments. Exiting.")
        return
    
    # Create instrument map
    instrument_map = create_instrument_map(instruments)
    print(f"Created map with {len(instrument_map)} unique instruments")
    
    # Save to JSON file
    save_to_json(instrument_map)
    
    print("Process completed successfully!")

    # Exit the script successfully
    print("▶️ Finishing...")
    sys.exit(0)

if __name__ == "__main__":
    main()

