from mcp.server.fastmcp import FastMCP
import json
import os
import subprocess
import time

# Initialize FastMCP server
eToro_server = FastMCP(
    "eToro Finance MCP Server",
    instructions="""
# eToro Finance MCP Server

This server provides information about financial instruments available on the eToro platform.

Available tools:
- get_instruments : Get list of available financial instruments available for trading on the eToro platform.
""",
)

@eToro_server.tool(
    "get_instruments",
    description="""Get list of available financial instruments available for trading on the eToro platform.
    Arguments: 
    - intrument (string, optional): Name or partial name of the financial instrument to filter by.
    - instrument_type_ID (int, optional): Type of financial instrument to filter by (1=forex, 2=commodities, 3=cryptocurrencies, 4=indexes, 5=stocks). If not provided, returns all instruments.
    - amount (int, optional): Number of instruments to return per page. Defaults to 10.
    - page (int, optional): Page number for pagination (starts at 1). Defaults to 1.
    """
)
async def get_instruments(instrument: str = None, instrument_type_ID: int = None, amount: int = 10, page: int = 1) -> str:
    # Load instruments from file
    # Check if instruments.json exists, if not run getInstruments.py
    if not os.path.exists('./instruments.json'):
        subprocess.run(['python', 'getInstruments.py'])
        time.sleep(2)
    
    with open('./instruments.json', 'r') as f:
        all_instruments = json.load(f)
    
    # Convert dict to list if needed
    if isinstance(all_instruments, dict):
        all_instruments = list(all_instruments.values())
        # Filter by instrument name if provided
        if instrument:
            instruments = [
                inst for inst in all_instruments 
                if instrument.lower() in inst.get('InstrumentName', '').lower()
            ]
        else:
            instruments = all_instruments    
        
        # Filter by instrument_type_ID if provided
        if instrument_type_ID:
            instruments = [
                inst for inst in all_instruments 
                if inst.get('InstrumentTypeID', None) == instrument_type_ID
            ]
        else:
            instruments = all_instruments
        
        # Calculate pagination
        total_count = len(instruments)
        start_index = (page - 1) * amount
        end_index = start_index + amount    
        
        # Get paginated results
        paginated_instruments = instruments[start_index:end_index]        
        
        # Build response with metadata
        response = {
            "page": page,
            "amount": amount,
            "total_count": total_count,
            "total_pages": (total_count + amount - 1) // amount,
            "instruments": paginated_instruments
        }
    
    return json.dumps(response, indent=2)

if __name__ == "__main__":
    # Initialize and run the server
    print("Starting eToro Finance MCP server...")
    eToro_server.run()