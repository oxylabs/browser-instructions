import requests
from pprint import pprint

payload = {
    "source": "universal",
    "url": "https://sandbox.oxylabs.io/products",
    "render": "html",
    "browser_instructions": [
        {
            "type": "click",
            "selector": {
                "type": "xpath",
                "value": "//h4[@class='title css-7u5e79 eag3qlw7']"
            }
        },
        {
            "type": "wait",
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
