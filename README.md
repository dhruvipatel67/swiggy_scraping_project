# Swiggy Pizza API

A FastAPI-based service that fetches and filters pizza data from Swiggy's search API for Ahmedabad. This API provides information about pizzas available in Ahmedabad, including restaurant names, item names, prices, and delivery times.

## Features

- Fetches real-time pizza data from Swiggy
- Filters and structures the data for easy consumption
- Provides both raw and filtered endpoints
- Implements CORS for cross-origin requests
- Includes detailed error handling and logging

## Prerequisites

- Python 3.7+
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the FastAPI server:
```bash
python main.py
```

The server will start on `http://localhost:8080`

## API Endpoints

### 1. Root Endpoint
- **URL**: `/`
- **Method**: GET
- **Description**: Welcome message
- **Response**: 
```json
{
    "message": "Welcome to Swiggy Pizza API for Ahmedabad"
}
```

### 2. Raw Search Endpoint
- **URL**: `/search`
- **Method**: GET
- **Description**: Fetches raw data from Swiggy's search API
- **Response**: Raw JSON response from Swiggy's API

### 3. Filtered Search Endpoint
- **URL**: `/search-filtered`
- **Method**: GET
- **Description**: Returns filtered pizza data with specific attributes
- **Response**: List of pizza items with the following structure:
```json
[
    {
        "restaurant_name": "string",
        "item_name": "string",
        "price": "float",
        "delivery_time": "string"
    }
]
```

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8080/docs`