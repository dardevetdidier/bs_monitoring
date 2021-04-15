import requests
from bs4 import BeautifulSoup
import csv
import pprint


# SETTING UP CSV FILE
csv_file = open('info_product.csv', 'w', newline='')
fieldnames = ['product_page_url', 'universal_product_code', 'title', 'price_including_tax', 'price_'
              'excluding_tax', 'number_available', 'product_description', 'category', 'review_rating',
              'image_url']
writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
writer.writeheader()


# CREATE CSV FILE FROM DICTIONARY
def create_csv_file(infos_dict):
    writer.writerow(infos_dict)


# GET HTML PAGE
def get_soup(url):
    response_cat = requests.get(url)
    soup = BeautifulSoup(response_cat.content, 'html.parser')
    return soup


# GET URL OF 1 PRODUCT
def get_url_prod(url):
    url_prod = get_soup(url).find('h3').find('a')['href'].replace("../../..", "")
    return f"http://books.toscrape.com/catalogue{url_prod}"


# GET URL OF ALL PRODUCTS / 1 CATEGORY ==> LIST
def get_urls_prods(url):
    urls_prod_list = []
    for li in get_soup(url).find_all('li', {'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'}):
        url_prod = li.find('h3').find('a')['href'].replace("../../..", "")
        urls_prod_list.append(f"http://books.toscrape.com/catalogue{url_prod}")
        # print(f"http://books.toscrape.com/catalogue{url_prod}")

    return urls_prod_list


# GET INFOS OF 1 PRODUCT ==> DICT
def get_prod_infos(url):
    product_page_url = url
    upc = get_soup(url).find('th', text='UPC').find_next_sibling('td').text
    title = get_soup(url).find('h1').text
    price_incl_tax = get_soup(url).find('th', text='Price (incl. tax)').find_next_sibling('td').text
    price_excl_tax = get_soup(url).find('th', text='Price (excl. tax)').find_next_sibling('td').text
    num_available = get_soup(url).find('p', {'class': 'instock availability'}).text.strip()
    try:
        prod_descript = get_soup(url).find('div', {'id': 'product_description'}).find_next_sibling('p').text
    except AttributeError:
        prod_descript = "No description"
    category = get_soup(url).find('li', {'class': 'active'}).find_previous('a').text
    review_rating = get_soup(url).find('th', text='Number of reviews').find_next_sibling('td').text
    image_url = get_soup(url).find('div', {'class': 'item active'}).find_next('img')['src'].replace("../../", "")

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
    return infos_product
    # print("product_page_url : " + product_page_url)
    # print("universal_product_code : " + upc)
    # print("title : " + title)
    # print("price_including_tax : " + price_incl_tax)
    # print("price_excluding_tax : " + price_excl_tax)
    # print("number_available : " + num_available)
    # print("product_description : " + prod_descript)
    # print("category : " + category)
    # print("review_rating = " + review_rating)
    # print("image_url : " + "http://books.toscrape.com/" + image_url)


url_cat = "http://books.toscrape.com/catalogue/category/books/womens-fiction_9/index.html"

# GET NUMBER OF RESULTS IN A CATEGORY
results = int(get_soup(url_cat).find('form', {'method': 'get'}).strong.text)
pages = 1
page_nb = 1


# COUNT NUMBER OF PAGES IN A CATEGORY
if not int(results) % 20 == 0:
    pages = ((int(results) / 20) + 1)
    pages = int(pages)

# IF JUST 1 PAGE
if results <= 20:  # no pagination
    for link in get_urls_prods(url_cat):
        create_csv_file(get_prod_infos(link))
        pprint.pprint(get_prod_infos(link), sort_dicts=False)
        print()
