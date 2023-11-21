import requests
from pprint import pprint

payload = {
    "source": "universal_ecommerce",
    "url": "https://www.aliexpress.us/item/3256805956826539.html",
    "geo_location": "United States",
    "render": "html",
    "browser_instructions": [
        {
            "type": "scroll_to_bottom",
            "wait_time_s": 2
        }
    ]
}

response = requests.request(
    "POST",
    "https://realtime.oxylabs.io/v1/queries",
    auth=("USERNAME", "PASSWORD"),
    json=payload
)

pprint(response.json())