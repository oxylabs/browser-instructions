import requests
from pprint import pprint

payload = {
    "source": "universal_ecommerce",
    "url": "https://www.aliexpress.us/",
    "geo_location": "United States",
    "render": "html",
    "browser_instructions": [
        {
            "type": "scroll",
            "x": 0,
            "y": 4115,
            "wait_time_s": 5
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
