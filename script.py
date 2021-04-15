import requests
from bs4 import BeautifulSoup
import csv

# product url
url = "http://books.toscrape.com/catalogue/the-origin-of-species_499/index.html"

# http request to get html page with BS
response = requests.get(url)

if response.ok:  # if code == 200
    soup = BeautifulSoup(response.content, 'html.parser')
# get product informations with BS
    product_page_url = response.url
    upc = soup.find('th', text='UPC').find_next_sibling('td').text
    title = soup.find('h1').text
    price_incl_tax = soup.find('th', text='Price (incl. tax)').find_next_sibling('td').text
    price_excl_tax = soup.find('th', text='Price (excl. tax)').find_next_sibling('td').text
    num_available = soup.find('p', {'class': 'instock availability'}).text.strip()
    prod_descript = soup.find('div', {'id': 'product_description'}).find_next_sibling('p').text
    category = soup.find('li', {'class': 'active'}).find_previous('a').text
    review_rating = soup.find('th', text='Number of reviews').find_next_sibling('td').text
    image_url = soup.find('div', {'class': 'item active'}).find_next('img')['src'].replace("../../", "")

    print("product_page_url : " + product_page_url)
    print("universal_product_code : " + upc)
    print("title : " + title)
    print("price_including_tax : " + price_incl_tax)
    print("price_excluding_tax : " + price_excl_tax)
    print("number_available : " + num_available)
    print("product_description : " + prod_descript)
    print("category : " + category)
    print("review_rating = " + review_rating)
    print("image_url : " + "http://books.toscrape.com/" + image_url)

    infos_product = {
        'product_page_url': product_page_url,
        'universal_product_code': upc,
        'title': title,
        'price_including_tax': price_incl_tax,
        'price_excluding_tax': price_excl_tax,
        'number_available': num_available,
        'product_description': prod_descript,
        'category': category,
        'review_rating': review_rating,
        'image_url': 'http://books.toscrape.com/' + image_url
    }

    # create csv file from dictionary
    with open('info_product.csv', 'w', newline='') as csvfile:
        fieldnames = ['product_page_url', 'universal_product_code', 'title', 'price_including_tax', 'price_'
                      'excluding_tax', 'number_available', 'product_description', 'category', 'review_rating',
                      'image_url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(infos_product)
