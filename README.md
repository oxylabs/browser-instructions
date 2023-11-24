# How to Use Browser Instructions for Web Scraping

- [General tips](#general-tips)
- [Structuring instructions for Scraper APIs and Web Unblocker](#structuring-instructions-for-scraper-apis-and-web-unblocker)
  * [Web Unblocker](#web-unblocker)
  * [Scraper APIs](#scraper-apis)
- [Postpone execution or wait for elements](#postpone-execution-or-wait-for-elements)
  * [Wait for an element to load](#wait-for-an-element-to-load)
  * [Wait](#wait)
- [Click on elements](#click-on-elements)
- [Fill in text in fields](#fill-in-text-in-fields)
- [Scroll pages](#scroll-pages)
  * [Scroll by pixel](#scroll-by-pixel)
  * [Scroll to the bottom](#scroll-to-the-bottom)
- [Fetch browser resources](#fetch-browser-resources)

Browser instructions are a feature of Oxylabs’ [<u>Scraper
API</u>](https://oxylabs.io/products/scraper-api) solutions and [<u>Web
Unblocker</u>](https://oxylabs.io/products/web-unblocker), enabling
users to interact with a web page when using a headless browser. For
instance, you can tell the headless browser to scroll down to the bottom
of the page, click on a specific element, enter text into a specific
field, and much more. As a result, your scraping operations will be
better equipped to handle various page interactions without using
third-party tools like Selenium or Puppeteer.

Follow this guide to learn how to form browser instructions and see them
applied when scraping popular e-commerce and travel aggregation
websites.

## General tips

Before writing custom browser instructions, you should explore your
target web page and navigate through each step you want the browser to
make. Take notice of any peculiarities, like longer loading times or
unexpected page refreshes, that may affect how the headless browser sees
the page and, thus, its ability to interact with desired elements.

After sending a request to the Scraper APIs or Web Unblocker, it’s best
to check the output for any interaction errors to make sure that every
browser instruction was completed successfully. In cases where
instructions fail, you may find it helpful to retrieve a [<u>PNG
screenshot</u>](https://developers.oxylabs.io/scraper-apis/getting-started/global-parameter-values#render)
of the result, which will let you see what the headless browser is
dealing with. For better control when handling failures, you can use the
[<u>on_error</u>](https://developers.oxylabs.io/scraper-apis/headless-browser/browser-instructions-beta/list-of-instructions#on_error)
parameter to specify whether browser instructions should be stopped
entirely or continue with the next instruction on error.

You can use XPath and CSS selectors to select elements or use text to
easily target elements with a certain text value. If you need a
refresher on how to form selectors, see this blog post on [<u>XPath vs.
CSS</u>](https://oxylabs.io/blog/xpath-vs-css). To quickly test out your
XPath and CSS selectors, you can use the **Developer Tools** \>
**Elements** tab, open the search bar, and paste your selector:

![](/images/dev_tools.png)

Oxylabs
documentation for [<u>Web Unblocker</u>](https://developers.oxylabs.io/advanced-proxy-solutions/web-unblocker/headless-browser) and [<u>Scraper APIs</u>](https://developers.oxylabs.io/scraper-apis/headless-browser)
is the go-to resource for all the available parameters, so keep it open
for a quick reference.

## Structuring instructions for Scraper APIs and Web Unblocker

The process of creating browser instructions for Scraper APIs and Web
Unblocker differs slightly, and we'll explore these variances below to
make it clearer for you. So, using this [<u>Oxylabs’
Sandbox</u>](https://sandbox.oxylabs.io/products) page, let’s instruct
the browser to click the first product listing and scrape it:

![](/images/sandbox.png)

### Web Unblocker

When using Web Unblocker, you must define browser instructions as a
value of the `X-Oxylabs-Browser-Instructions` header after providing the
`"X-Oxylabs-Render": "html"` header.

There are several ways you can form your instructions, the first one
being a single JSON line:

```python
import requests

proxies = {
  "http": "http://USERNAME:PASSWORD@unblock.oxylabs.io:60000",
  "https": "http://USERNAME:PASSWORD@unblock.oxylabs.io:60000"
}


headers = {
    "X-Oxylabs-Render": "html",
    "X-Oxylabs-Browser-Instructions": '''[{"type":"click","selector":{"type":"xpath","value":"//h4[@class='title css-7u5e79 eag3qlw7']"}},{"type":"wait","wait_time_s":3}]'''
}

response = requests.get(
    "https://sandbox.oxylabs.io/products",
    verify=False,  # It's required to ignore the certificate
    proxies=proxies,
    headers=headers
)

print(response.text)
```

We recommend providing instructions in **escaped JSON** format and without
empty spaces to ensure proper parsing and interpretation by our API. For
manual testing, you can escape a JSON string manually or by using
[<u>online tools</u>](https://www.freeformatter.com/json-escape.html)
and then provide the headers like so:

```python
headers = {
    "X-Oxylabs-Render": "html",
    "X-Oxylabs-Browser-Instructions": '''[{\"type\":\"click\",\"selector\":{\"type\":\"xpath\",\"value\":\"\/\/h4[@class='title css-7u5e79 eag3qlw7']\"}},{\"type\":\"wait\",\"wait_time_s\":3}]'''
}
```

Another way, which is the only approach that’ll work in the full
implementation stage, is to import the `json` module and use the
`json.dumps()` function to automatically escape JSON. This way, you can
also structure your instructions in a more readable way:

```python
headers = {
    "X-Oxylabs-Render": "html",
    "X-Oxylabs-Browser-Instructions": json.dumps(
        [
            {
                "type":"click",
                "selector":{
                    "type":"xpath",
                    "value":"//h4[@class='title css-7u5e79 eag3qlw7']"
                }
            },
            {
                "type":"wait",
                "wait_time_s":3
            }
        ]
    )
}
```

### Scraper APIs

For all Scraper APIs, browser instructions must be paired with the
`browser_instructions` key and included in the payload. These instructions
can be provided as a single line or spread out for improved readability:

```python
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
```

As these differences are out of the way, let’s overview some real-life
scraping scenarios where browser instructions can be used.

## Postpone execution or wait for elements

<sub>*All information herein is provided on an “as is” basis and for
informational purposes only. We make no representation and disclaim all
liability with respect to your use of any information contained on this
page. Before engaging in scraping activities of any kind you should
consult your legal advisors and carefully read the particular website’s
terms of service or receive a scraping license.*</sub>

As the heading suggests, you can instruct the browser to wait a set
count of seconds explicitly. This is helpful in cases where you need to:

- Handle lazy loading pages and elements;

- Wait for a page to load fully;

- Wait for elements or pop ups to load;

- Imitate organic user behavior.

Consider this [<u>Wayfair product
page</u>](https://www.wayfair.com/furniture/pdp/ebern-designs-cidalino-83-upholstered-sleeper-sofa-chaise-with-storage-2-cup-holders-w100038905.html?piid=122444084)
as an example. When you visit this page, the full price, the discounted
price, and the shipping information take quite a while to load:

![](/images/wayfair.png)

### Wait for an element to load

Use the `wait_for_element` parameter when you only need to wait for a
specific element to load, as is the case with this Wayfair page. As a
result, you’ll save time by making your scraping process as short as it
can be.

You can specify the element by providing its **XPath** or **CSS** selector or
its **textual** value. See this snippet below, where the `timeout_s` parameter
instructs the browser to terminate the action if the element doesn’t
load after 5 seconds:

```python
payload = {
    "source": "universal_ecommerce",
    "url": "https://www.wayfair.com/furniture/pdp/ebern-designs-cidalino-83-upholstered-sleeper-sofa-chaise-with-storage-2-cup-holders-w100038905.html",
    "render": "html",
    "browser_instructions": [
        {
            "type": "wait_for_element",
            "selector": {
                "type": "xpath",
                "value": "//div[@data-enzyme-id='PriceBlock']"
            },
            "timeout_s": 7
        }
    ]
}
```

Note how, in this example, the `timeout_s` parameter goes after the
selector parameter. You may also combine the `wait_time_s` and `on_error`
parameters in the same manner if you want to include them.

### Wait

The `wait` command directs the browser to pause the execution of further
instructions until the specified duration has passed. This parameter has
many uses, one of which can be to simply wait for a page to load
completely. Let’s use the previous Wayfair page as an example:

```python
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
```

## Click on elements

Simply put, by clicking on specific elements, you can access the data
you need that’s not visible in the initial HTML. There are countless
ways you can use the `click` instruction, primarily enabling you to:

- Load dynamic content;

- Handle various pop-ups and alerts;

- Navigate websites like a real user.

Let’s use this [<u>Trivago search
page</u>](https://www.trivago.com/en-US/lm/hotels-los-angeles-california?search=200-14257)
as an example. When you scrape this page without browser instructions,
you aren’t able to retrieve all available deals for a listing without
clicking the hotel name and then clicking “Show all prices”:

![](/images/trivago.png)

![](/images/trivago_show_prices.png)

In this scenario, you can tell the browser to click the hotel name and
the button and wait a few seconds to load the data:

```python
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
```

## Fill in text in fields

The `input` parameter is handy in situations where you need to enter
specific information into a field. With it, you can perform various
input actions, like:

- Access content that requires you to enter a text;

- Navigate websites;

- Fill in forms.

Below, you can see a [<u>Best Buy listing
page</u>](https://www.bestbuy.com/site/searchpage.jsp?st=backpack),
where you can enter a ZIP code to see customized delivery information.
Hence, you can instruct the browser to:

1.  **Click** the delivery ZIP code;

    - Wait for the element to load;

2.  **Enter** “11238” into the input field;

3.  **Click** “Update”;

    - Wait for the page to reload.

![](/images/best_buy.png)

```python
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
```

## Scroll pages

You can scroll pages by using two different parameters, in the end
giving you the ability to:

- Load all content by overcoming lazy loading elements;

- Mimic organic user interaction.

### Scroll by pixel

The `scroll` instruction grants you complete control over the browser's
scrolling ability, enabling precise navigation in all directions
(left-right and up-down) pixel by pixel.

> [!NOTE]
> To scroll up, use a negative value, for instance `-100`.

For this example, let’s use the [<u>Aliexpress
homepage</u>](https://www.aliexpress.us/), as it has several sections
that load only when you scroll to them.

To estimate how many pixels it would take to scroll the page to a
certain section, you can use your browser’s Developer Tools and run a
JavaScript code. Open the **Dev Tools**, head to the **Console** tab,
and execute this line, which will scroll down by `500` pixels:

```javascript
window.scrollBy(0, 500)
```

Alternatively, you can simply scroll the page manually to the desired
section and then run the below code to output the amount of pixels
you’ve scrolled from the top:

```javascript
var scrollTop = window.pageYOffset || document.documentElement.scrollTop;
console.log(scrollTop)
```

As the Aliexpress homepage has lazy loading sections, you’ll only be
able to scrape a total of 30 products under the _“More to love”_ section
without using browser instructions. After scrolling down and triggering
the first lazy loading section – there will be a total of 60 products
available. So, using this logic, you can control how many listings
you’ll scrape.

Say you want to retrieve 60 products in total. You can instruct the
browser to scroll down a number of pixels, in this case, `4115` pixels, to
trigger the first lazy loading section and load 30 more items:

```python
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
```

### Scroll to the bottom

When you use the `scroll_to_bottom` instruction, the browser will scroll
down to the bottom of the page. We can target this [<u>Aliexpress
product page</u>](https://www.aliexpress.us/item/3256805956826539.html)
as it has related products at the bottom that load only when you scroll
to this section:

![](/images/aliexpress.png)

Let’s say your goal is to scrape these related products. You can
instruct the browser to scroll to the bottom and give it some time to
load these elements:

```python
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
```

## Fetch browser resources

With the `fetch_browser` parameter, you can retrieve the first occurrence
of a Fetch/XHR resource that matches a specified pattern. In essence, it
enables you to:

- Fetch data straight from a resource;

- Get structured data if the resource has it structured;

- Get only the data you need instead of dealing with the entire HTML document.

Let’s illustrate this functionality by using this [<u>Zillow search
page</u>](https://www.zillow.com/ny/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22west%22%3A-106.09230612499996%2C%22east%22%3A-45.44777487499997%2C%22south%22%3A33.66133888602103%2C%22north%22%3A50.74415717706928%7D%2C%22mapZoom%22%3A4%2C%22usersSearchTerm%22%3A%22NY%22%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A43%2C%22regionType%22%3A2%7D%5D%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%7D).
Looking at the **Dev** **Tools** \> **Network** \> **Response** tab, you
can see that the `async-create-search-page-state` resource has all the
listings neatly structured in JSON format:

![](/images/fetch_zillow.png)

![](/images/fetch_json.png)

You can extract the full JSON file by specifying the URL of this
resource in browser instructions. Note, that the `filter` parameter values
must be formatted as regular expressions (regex). Furthermore, you may
want to transform the URL into a regular expression that matches
different URL variations and doesn’t break with minor changes of the API
endpoint.

```python
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
```

This article focuses on the basics of forming and using browser
instructions with our Scraper APIs and Web Unblocker. So, take your time
to play around and see what works best for your target websites. As
always, if you have any questions, don’t hesitate to contact our 24/7
support team via [<u>live chat</u>](https://oxylabs.io/) or
[<u>email</u>](mailto:support@oxylabs.io).
