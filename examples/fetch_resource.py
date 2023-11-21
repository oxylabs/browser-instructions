import requests
from pprint import pprint

payload = {
    "source": "universal",
    "url": "https://www.zillow.com/ny/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22west%22%3A-106.09230612499996%2C%22east%22%3A-45.44777487499997%2C%22south%22%3A33.66133888602103%2C%22north%22%3A50.74415717706928%7D%2C%22mapZoom%22%3A4%2C%22usersSearchTerm%22%3A%22NY%22%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A43%2C%22regionType%22%3A2%7D%5D%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%7D",
    "render": "html",
    "browser_instructions": [
        {
            "type": "fetch_resource",
            "filter": "https://www.zillow.com/async-create-search-page-state"
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