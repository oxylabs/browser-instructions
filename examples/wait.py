import requests
from pprint import pprint

payload = {
    "source": "universal_ecommerce",
    "url": "https://www.wayfair.com/furniture/pdp/ebern-designs-cidalino-83-upholstered-sleeper-sofa-chaise-with-storage-2-cup-holders-w100038905.html",
    "render": "html",
    "browser_instructions": [
        {
            "type": "wait",
            "wait_time_s": 7
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