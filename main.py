import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any, Optional
import random
import time
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI(
    title="Swiggy Pizza API",
    description="API to fetch pizza data from Swiggy's search API for Ahmedabad",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Constants
SWIGGY_SEARCH_URL = "https://www.swiggy.com/dapi/restaurants/search/v3"
AHMEDABAD_LAT = 23.0225
AHMEDABAD_LNG = 72.5714
SEARCH_QUERY = "Pizza"

# User agents list for rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
]

# Define response model for filtered data
class PizzaItem(BaseModel):
    restaurant_name: str
    item_name: str
    price: float
    delivery_time: str

@app.get("/")
def read_root():
    return {"message": "Welcome to Swiggy Pizza API for Ahmedabad"}

@app.get("/search", response_model=Dict[str, Any])
async def search_pizza():
    """
    Fetch raw data from Swiggy's search API for pizzas in Ahmedabad
    """
    try:
        # Prepare headers to avoid blocks
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Referer": "https://www.swiggy.com/",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json",
            "Origin": "https://www.swiggy.com"
        }
        
        # Prepare parameters
        params = {
            "lat": AHMEDABAD_LAT,
            "lng": AHMEDABAD_LNG,
            "str": SEARCH_QUERY,
            "trackingId": None,
            "submitAction": "ENTER",
            "queryId": f"seo-data-{int(time.time() * 1000)}"
        }
        
        print("\n=== DEBUG: Making Request to Swiggy ===")
        print(f"URL: {SWIGGY_SEARCH_URL}")
        print(f"Headers: {headers}")
        print(f"Params: {params}")
        
        # Make request to Swiggy API
        response = requests.get(
            SWIGGY_SEARCH_URL,
            headers=headers,
            params=params
        )
        
        print(f"\n=== DEBUG: Response Status ===")
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        # Check response status
        if response.status_code != 200:
            print(f"Error response: {response.text}")
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch data from Swiggy")
        
        # Parse and print response
        response_data = response.json()
        print("\n=== DEBUG: Response Data ===")
        print(f"Response type: {type(response_data)}")
        print(f"Response keys: {response_data.keys() if isinstance(response_data, dict) else 'Not a dictionary'}")
        
        if isinstance(response_data, dict) and "data" in response_data:
            data = response_data["data"]
            print("\n=== DEBUG: Data Structure ===")
            print(f"Data type: {type(data)}")
            print(f"Data keys: {data.keys() if isinstance(data, dict) else 'Not a dictionary'}")
            
            if "cards" in data:
                print(f"\nNumber of cards: {len(data['cards'])}")
                for idx, card in enumerate(data["cards"]):
                    print(f"\nCard {idx} keys: {card.keys() if isinstance(card, dict) else 'Not a dictionary'}")
        
        return response_data
        
    except Exception as e:
        print(f"\n=== DEBUG: Error ===")
        print(f"Error in search_pizza: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")

@app.get("/search-filtered", response_model=List[PizzaItem])
async def search_pizza_filtered():
    """
    Fetch and filter pizza data from Swiggy's search API for Ahmedabad,
    returning only required attributes
    """
    try:
        # Get raw response from search endpoint
        raw_data = await search_pizza()
        print("\n=== DEBUG: Raw Data ===")
        print(f"Raw data type: {type(raw_data)}")
        print(f"Raw data keys: {raw_data.keys() if isinstance(raw_data, dict) else 'Not a dictionary'}")
        
        # Initialize filtered results list
        filtered_results = []
        
        if "data" in raw_data:
            data = raw_data["data"]
            print("\n=== DEBUG: Data Structure ===")
            print(f"Data type: {type(data)}")
            print(f"Data keys: {data.keys() if isinstance(data, dict) else 'Not a dictionary'}")
            
            # Try to find restaurants in different possible locations
            if "cards" in data:
                print("\n=== DEBUG: Processing Cards ===")
                print(f"Number of cards: {len(data['cards'])}")
                
                for card_idx, card in enumerate(data["cards"]):
                    print(f"\nProcessing card {card_idx}")
                    print(f"Card keys: {card.keys() if isinstance(card, dict) else 'Not a dictionary'}")
                    
                    # Check for groupedCard
                    if "groupedCard" in card:
                        grouped_card = card["groupedCard"]
                        print(f"Grouped card keys: {grouped_card.keys() if isinstance(grouped_card, dict) else 'Not a dictionary'}")
                        
                        # Process each card in the group
                        if "cardGroupMap" in grouped_card:
                            card_group_map = grouped_card["cardGroupMap"]
                            print(f"Card group map keys: {card_group_map.keys() if isinstance(card_group_map, dict) else 'Not a dictionary'}")
                            
                            # Process each group
                            for group_key, group_data in card_group_map.items():
                                print(f"\nProcessing group: {group_key}")
                                
                                if "cards" in group_data:
                                    for group_card in group_data["cards"]:
                                        print(f"Group card keys: {group_card.keys() if isinstance(group_card, dict) else 'Not a dictionary'}")
                                        
                                        if "card" in group_card:
                                            card_data = group_card["card"]
                                            print(f"Card data keys: {card_data.keys() if isinstance(card_data, dict) else 'Not a dictionary'}")
                                            
                                            if "card" in card_data:
                                                inner_card = card_data["card"]
                                                print(f"Inner card type: {inner_card.get('@type', 'Unknown')}")
                                                
                                                # Check for dish information
                                                if inner_card.get("@type") == "type.googleapis.com/swiggy.presentation.food.v2.Dish":
                                                    if "info" in inner_card:
                                                        info = inner_card["info"]
                                                        print(f"Processing dish: {info.get('name', 'Unknown')}")
                                                        
                                                        try:
                                                            # Get restaurant information
                                                            restaurant_info = inner_card.get("restaurant", {}).get("info", {})
                                                            restaurant_name = restaurant_info.get("name", "Unknown")
                                                            
                                                            # Get the price (convert from paise to rupees)
                                                            price = float(info.get("price", 0)) / 100
                                                            
                                                            # Get delivery time
                                                            delivery_time = "Unknown"
                                                            if "sla" in restaurant_info:
                                                                delivery_time = f"{restaurant_info['sla'].get('deliveryTime', 'Unknown')} mins"
                                                            
                                                            filtered_results.append(PizzaItem(
                                                                restaurant_name=restaurant_name,
                                                                item_name=info.get("name", "Unknown"),
                                                                price=price,
                                                                delivery_time=delivery_time
                                                            ))
                                                            print(f"Successfully added dish: {info.get('name', 'Unknown')} from {restaurant_name}")
                                                        except Exception as e:
                                                            print(f"Error processing dish: {str(e)}")
                                                            print(f"Dish info: {info}")
        
        print(f"\n=== DEBUG: Final Results ===")
        print(f"Total results found: {len(filtered_results)}")
        if filtered_results:
            print("Sample result:", filtered_results[0].dict())
        
        return filtered_results
    
    except Exception as e:
        print(f"\n=== DEBUG: Error ===")
        print(f"Error in search_pizza_filtered: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing data: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)