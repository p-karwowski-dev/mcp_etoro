import json
import requests
from enum import Enum
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
eToro_server = FastMCP(
    "eToro Finance MCP Server",
    instructions="""
# eToro Finance MCP Server

This server is used to get information about financial instruments available on the platform.

Available tools:
- get_instruments : Get list of available financial instruments available for trading on the eToro platform.
""",
)

@eToro_server.tool(
    "get_instruments",
    description="""Get list of available financial instruments available for trading on the eToro platform.
    Arguments: 
    - instrument_type (str, optional): Type of financial instrument to filter by (e.g., "stocks", "cryptocurrencies", "commodities", "forex", "indexes"). If not provided or wrong value, returns all instruments.
    """
)
async def get_instruments(instrument_type: str = None) -> str:
    
    instrumentTypeIdMap = {
        "forex": 1,
        "commodities": 2,
        "cryptocurrencies": 3,
        "stocks": 4,
        "indexes": 5,
    }

    # Fetch instruments data from eToro API
    url = "https://api.etorostatic.com/sapi/instrumentsmetadata/V1.1/instruments"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            error_msg = f"Failed to fetch data. Status code: {response.status_code}"
            print(error_msg)
            return json.dumps({"error": error_msg})
        
        data = response.json()
        print("Fetched data successfully.")
        
    except Exception as e:
        error_msg = f"Error fetching data: {e}"
        print(error_msg)
        return json.dumps({"error": error_msg})

    # Filter instruments by type if instrument_type_id is provided
    try:
        if instrument_type:
            instruments = [
                instrument for instrument in data["InstrumentDisplayDatas"]
                if instrument["InstrumentTypeID"] == instrumentTypeIdMap.get(instrument_type.lower())
            ]
        else:
            instruments = data["InstrumentDisplayDatas"]

        # Create a simplified list of instruments
        instruments = [
            {
                "InstrumentID": instrument["InstrumentID"],
                "InstrumentName": instrument["InstrumentDisplayName"],
                "InstrumentTypeID": instrument["InstrumentTypeID"],
                "Symbol": instrument["SymbolFull"],
            }
            for instrument in instruments
        ]
        
        return json.dumps(instruments, indent=2)
        
    except KeyError as e:
        error_msg = f"Missing expected key in API response: {e}"
        print(error_msg)
        return json.dumps({"error": error_msg})
    except Exception as e:
        error_msg = f"Error processing instruments: {e}"
        print(error_msg)
        return json.dumps({"error": error_msg})

if __name__ == "__main__":
    # Initialize and run the server
    print("Starting eToro Finance MCP server...")
    eToro_server.run()