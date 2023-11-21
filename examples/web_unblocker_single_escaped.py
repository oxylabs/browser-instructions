import requests

proxies = {
  "http": "http://USERNAME:PASSWORD@unblock.oxylabs.io:60000",
  "https": "http://USERNAME:PASSWORD@unblock.oxylabs.io:60000"
}


headers = {
    "X-Oxylabs-Render": "html",
    "X-Oxylabs-Browser-Instructions": '''[{\"type\":\"click\",\"selector\":{\"type\":\"xpath\",\"value\":\"\/\/h4[@class='title css-7u5e79 eag3qlw7']\"}},{\"type\":\"wait\",\"wait_time_s\":3}]'''
}

response = requests.get(
    "https://sandbox.oxylabs.io/products",
    verify=False,  # It's required to ignore the certificate
    proxies=proxies,
    headers=headers
)

print(response.text)