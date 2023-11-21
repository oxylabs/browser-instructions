import requests
from pprint import pprint

payload = {
    "source": "universal",
    "url": "https://www.trivago.com/en-US/lm/hotels-los-angeles-california?search=200-14257",
    "render": "html",
    "browser_instructions": [
        {
            "type": "click",
            "selector": {
                "type": "xpath",
                "value": "(//button[@data-testid='item-name'])[2]"
            },
            "wait_time_s": 3
        },
        {
            "type": "click",
            "selector": {
                "type": "xpath",
                "value": "//button[@data-testid='show-more-deals-button']"
            },
            "wait_time_s": 3
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