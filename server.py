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
    - instrument_type (str, optional): Type of financial instrument to filter by (e.g., "stocks", "cryptocurrencies", "commodities", "forex", "indices"). If not provided or wrong value, returns all instruments.
    """
)
async def get_instruments(instrument_type: str = None) -> str:
    # InstrumentTypeID Enum
    class InstrumentTypeID(Enum):
        FOREX = 1
        COMMODITIES = 2
        CRYPTOCURRENCIES = 3
        STOCKS = 4
        INDICES = 5

    # Mapping of instrument types to their IDs
    instrument_type_id = None
    if instrument_type:
        instrument_type_mapping = {
            "forex": InstrumentTypeID.FOREX,
            "commodities": InstrumentTypeID.COMMODITIES,
            "cryptocurrencies": InstrumentTypeID.CRYPTOCURRENCIES,
            "stocks": InstrumentTypeID.STOCKS,
            "indices": InstrumentTypeID.INDICES,
        }
        instrument_type_id = instrument_type_mapping.get(instrument_type.lower())


    # Fetch instruments data from eToro API
    url = "https://api.etorostatic.com/sapi/instrumentsmetadata/V1.1/instruments"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print("Fetched data successfully.")
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return json.dumps({"error": f"Failed to fetch data. Status code: {response.status_code}"})

    # Filter instruments by type if instrument_type_id is provided
    if instrument_type_id:
        instruments = [
            instrument for instrument in data["InstrumentDisplayDatas"]
            if instrument["InstrumentTypeID"] == instrument_type_id.value
        ]
    else:
        instruments = data["InstrumentDisplayDatas"]

    # Create a simplified list of instruments
    instruments = [
        {
            "InstrumentID": instrument["InstrumentID"],
            "InstrumentName": instrument["InstrumentName"],
            "InstrumentTypeID": instrument["InstrumentTypeID"],
            "DisplayName": instrument["DisplayName"],
            "Symbol": instrument["Symbol"],
        }
        for instrument in instruments
    ]

    return json.dumps(instruments, indent=2)

if __name__ == "__main__":
    # Initialize and run the server
    print("Starting eToro Finance MCP server...")
    eToro_server.run()