# eToro MCP Server

This is a Model Context Protocol (MCP) server that interacts with eToro API providing list of available instruments.

## Requirements

- Python 3.11 or higher
- Dependencies as listed in `pyproject.toml`, including:
  - mcp

## Setup

1. Clone this repository:

   ```bash
   git clone https://github.com/p-karwowski-dev/mcp_etoro.git
   cd mcp_etoro
   ```

2. Create and activate a virtual environment and install dependencies:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -e .
   ```

## Usage

Run the server to allow host MCP server to interact with it.

```bash
uv run server.py
```

### Integration with host MCP server

Edit the host config file adding below settings.

- **Note**: You may need to put the full path to the uv executable in the command field. You can get this by running `which uv` on MacOS/Linux or `where uv` on Windows. Alternatively you can navigate to the project locations and run `pwd` command line.

- macOS:

  ```json
  {
    "mcpServers": {
      "etoro": {
        "command": "uv",
        "args": [
          "--directory",
          "/ABSOLUTE/PATH/TO/PARENT/FOLDER/mcp_etoro",
          "run",
          "server.py"
        ]
      }
    }
  }
  ```

- Windows:

  ```json
  {
    "mcpServers": {
      "yfinance": {
        "command": "uv",
        "args": [
          "--directory",
          "C:\\ABSOLUTE\\PATH\\TO\\PARENT\\FOLDER\\mcp_etoro",
          "run",
          "server.py"
        ]
      }
    }
  }
  ```
