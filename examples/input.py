import requests
from pprint import pprint

payload = {
    "source": "universal_ecommerce",
    "url": "https://www.bestbuy.com/site/searchpage.jsp?st=backpack",
    "geo_location": "United States",
    "render": "html",
    "browser_instructions": [
        {
            "type": "click",
            "selector": {
                "type": "xpath",
                "value": "//div[@style='text-align: left;']"
            },
            "wait_time_s": 1
        },
        {
            "type": "input",
            "value": "11238",
            "selector": {
                "type": "xpath",
                "value": "//input[@placeholder='ZIP or City, State']"
            }
        },
        {
            "type": "click",
            "selector": {
                "type": "xpath",
                "value": "//button[@data-track='Delivery Location Modal: Update Button']"
            },
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