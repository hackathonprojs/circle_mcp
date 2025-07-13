# Weather MCP Server

A Model Context Protocol (MCP) server that provides weather information and alerts using the National Weather Service (NWS) API. This server offers tools for retrieving weather forecasts and active weather alerts for locations in the United States.

## About This Project

This project is based on the [Model Context Protocol (MCP) Getting Started Tutorial](https://modelcontextprotocol.io/quickstart/server) for server developers. The tutorial provides a comprehensive guide for building MCP servers and integrating them with clients like Claude for Desktop.

The original code sample for this weather server can be found in the [MCP Quickstart Resources repository](https://github.com/modelcontextprotocol/quickstart-resources/tree/main/weather-server-python).

## Features

- **Weather Alerts**: Get active weather alerts for any US state using two-letter state codes
- **Weather Forecasts**: Retrieve detailed weather forecasts for specific coordinates
- **Real-time Data**: Uses the official National Weather Service API for accurate, up-to-date information
- **Easy Integration**: Simple MCP server that can be integrated with any MCP-compatible client

## Installation

### Prerequisites

- Python 3.8 or higher
- `uv` package manager (recommended) or `pip`

### Setup

1. Clone the repository:
```bash
git clone https://github.com/agentventure/mcp_server_python_getting_started.git
cd mcp_server_python_getting_started
```

2. Install dependencies using `uv`:
```bash
uv sync
```

Or using `pip`:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Server

Start the MCP server:

```bash
uv run weather.py
```

The server will start and communicate via stdio, ready to handle requests from MCP clients.

### Available Tools

#### 1. Get Weather Alerts (`get_alerts`)

Retrieve active weather alerts for a US state.

**Parameters:**
- `state` (string): Two-letter US state code (e.g., "CA", "NY", "TX")

**Example:**
```python
# Get alerts for California
alerts = await get_alerts("CA")
```

**Response Format:**
```
Event: Severe Thunderstorm Warning
Area: Northern California
Severity: Severe
Description: Severe thunderstorm warning in effect...
Instructions: Take shelter immediately...

---

Event: Flood Watch
Area: Central Valley
Severity: Moderate
Description: Flood watch in effect...
Instructions: Monitor weather conditions...
```

#### 2. Get Weather Forecast (`get_forecast`)

Get detailed weather forecast for a specific location.

**Parameters:**
- `latitude` (float): Latitude coordinate of the location
- `longitude` (float): Longitude coordinate of the location

**Example:**
```python
# Get forecast for San Francisco (37.7749, -122.4194)
forecast = await get_forecast(37.7749, -122.4194)
```

**Response Format:**
```
Tonight:
Temperature: 55°F
Wind: 10 mph NW
Forecast: Clear skies with light winds. Low around 55.

---

Tomorrow:
Temperature: 68°F
Wind: 15 mph W
Forecast: Sunny with increasing clouds in the afternoon. High near 68.

---

Tomorrow Night:
Temperature: 52°F
Wind: 8 mph NW
Forecast: Partly cloudy with light winds. Low around 52.
```

## API Information

This server uses the [National Weather Service API](https://www.weather.gov/documentation/services-web-api), which provides:

- **No API Key Required**: Free access to weather data
- **Real-time Updates**: Data is updated frequently throughout the day
- **Comprehensive Coverage**: Covers all US states and territories
- **Reliable Service**: Official government weather service

### Data Sources

- **Alerts**: Active weather alerts from the NWS
- **Forecasts**: Detailed weather forecasts including temperature, wind, and conditions
- **Geographic Data**: Point-based weather information for any US location

## Error Handling

The server includes robust error handling for:

- Network connectivity issues
- Invalid coordinates or state codes
- API service unavailability
- Timeout conditions

When errors occur, the server returns informative error messages to help with debugging.

## Development

### Project Structure

```
weather/
├── weather.py          # Main MCP server implementation
├── main.py            # Entry point for running the server
├── pyproject.toml     # Project configuration and dependencies
├── README.md          # This file
└── .gitignore         # Git ignore rules
```

### Dependencies

- `mcp`: Model Context Protocol server framework
- `httpx`: Async HTTP client for API requests
- `fastmcp`: FastMCP server implementation

### Adding New Features

To add new weather-related tools:

1. Create a new async function in `weather.py`
2. Decorate it with `@mcp.tool()`
3. Add proper type hints and docstrings
4. Implement error handling using the existing `make_nws_request` helper

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Support

For issues or questions:

1. Check the [National Weather Service API documentation](https://www.weather.gov/documentation/services-web-api)
2. Review the MCP documentation at [modelcontextprotocol.io](https://modelcontextprotocol.io)
3. Open an issue in this repository

---

**Note**: This server is designed for educational and development purposes. For production use, consider implementing rate limiting and additional error handling based on your specific requirements.
