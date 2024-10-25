import requests
from bs4 import BeautifulSoup
import csv
# from urllib.request import Request, urlopen


# support data structures to implement the crawling logic
visited_pages = []
pages_to_scrape = ['https://www.yelp.com/search?find_desc=Local+Restaurants&find_loc=Brisbane%2C+Queensland&attrs=RestaurantsDelivery']

#to recitfy Response 403 error
request_headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
} 
 
# to store the scraped data
items = []

# to avoid overwhelming Yelp's servers with requests
limit = 5
i = 0

# until all pagination pages have been visited or the page limit is hit
while len(pages_to_scrape) != 0 and i < limit:
    # extract the first page from the array
    url = pages_to_scrape.pop(0)

    # mark it as "visited"
    visited_pages.append(url)

    # download and parse the page
        # Initiate HTTP request
    page = requests.get(url, headers=request_headers)
    # page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    # select all item card
    html_item_cards = soup.select('[data-testid="serp-ia-card"]')

    for html_item_card in html_item_cards:
        # print("HTML ITEM CARD: ", html_item_card)
        # scraping logic
        item = {}
        image = html_item_card.select_one('[data-lcp-target-id="SCROLLABLE_PHOTO_BOX"] img').attrs['src']
        name = html_item_card.select_one('h3 a').text
        url = 'https://www.yelp.com' + html_item_card.select_one('h3 a').attrs['href']
        # html_stars_element = html_item_card.select_one('[class^="yelp-emotion"]')
        # print("HTML STARS ELEMENT", html_stars_element.attrs)
        # stars = html_stars_element.attrs['aria-label'].replace(' star rating', '')
        # reviews = html_stars_element.parent.parent.next_sibling.text
        tags = []
        html_tag_elements = html_item_card.select('[class^="priceCategory"] button')
        for html_tag_element in html_tag_elements:
            tag = html_tag_element.text
            tags.append(tag)
        price_range_html = html_item_card.select_one('[class^="priceRange"]')

        # this HTML element is optional
        price_range = ""
        if price_range_html is not None:
            price_range = price_range_html.text
            # item['price_range'] = price_range

        services = []
        html_service_elements = html_item_card.select('[data-testid="services-actions-component"] p[class^="tagText"]')
        for html_service_element in html_service_elements:
            service = html_service_element.text
            services.append(service)

        # add the scraped data to the object and then the object to the array
        item['name'] = name
        item['image'] = image
        item['url'] = url
        # item['stars'] = stars
        # item['reviews'] = reviews
        item['tags'] = tags
        item['price_range'] = price_range
        item['services'] = services
        # print("ITEM: ", item)
        items.append(item)

    # discover new pagination pages and add them to the queue
    pagination_link_elements = soup.select('[class^="pagination-links"] a')
    for pagination_link_element in pagination_link_elements:
        pagination_url = pagination_link_element.attrs['href']
        # if the discovered URL is new
        if pagination_url not in visited_pages and pagination_url not in pages_to_scrape:
            pages_to_scrape.append(pagination_url)
    # increment the page counter
    i += 1

# extract the keys from the first object in the array to use them as headers of the CSV
# print("iTEMS: ")
# print(items)
headers = items[0].keys()

# initialize the .csv output file
with open('restaurants3.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=headers, quoting=csv.QUOTE_ALL)
    writer.writeheader()
    # populate the CSV file
    for item in items:
        # transform array fields from "['element1', 'element2', ...]" to "element1; element2; ..."
        csv_item = {}
        for key, value in item.items():
            if isinstance(value, list):
                csv_item[key] = '; '.join(str(e) for e in value)
            else:
                csv_item[key] = value
        # add a new record
        writer.writerow(csv_item)