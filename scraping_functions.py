import requests
from bs4 import BeautifulSoup
import os


# GET HTML PAGE
def get_soup(url):
    response_cat = requests.get(url)
    soup = BeautifulSoup(response_cat.content, 'html.parser')   # features="lxml" -> to avoid error
    return soup


# GET URLS OF ALL PRODUCTS FROM 1 CATEGORY PAGE ==> LIST
def get_urls_prods(url_c):
    soup = get_soup(url_c)
    urls_prod_list = []
    for li in soup.find_all('li', {'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'}):
        url_prod = li.find('h3').find('a')['href'].replace("../../..", "")
        urls_prod_list.append(f"http://books.toscrape.com/catalogue{url_prod}")
        # print(f"http://books.toscrape.com/catalogue{url_prod}")
    return urls_prod_list


# GET URLS OF ALL CATEGORIES FROM HOME PAGE --> LIST
def get_urls_categories(url_h):
    soup = get_soup(url_h)
    urls_all_cat_list = []
    lis = soup.find('div', {'class': 'side_categories'}).findAll("li")
    for li in lis[1:]:
        url_category = li.find("a")["href"]
        urls_all_cat_list.append(f"http://books.toscrape.com/{url_category}")
    return urls_all_cat_list


# GET THE NAME OF ALL CATEGORIES  ==> LIST
def get_category_list(url_h):
    soup = get_soup(url_h)
    cat_list = []
    lis = soup.find('div', {'class': 'side_categories'}).findAll("li")
    for li in (lis[1:]):
        cat = li.find("a").text.strip()
        cat_list.append(cat)
    return cat_list


# GET INFOS OF 1 PRODUCT ==> DICT
def get_prod_infos(url):
    soup = get_soup(url)

    upc = soup.find('th', text='UPC').find_next_sibling('td').text
    title = soup.find('h1').text
    price_incl_tax = soup.find('th', text='Price (incl. tax)').find_next_sibling('td').text
    price_excl_tax = soup.find('th', text='Price (excl. tax)').find_next_sibling('td').text
    num_available = soup.find('p', {'class': 'instock availability'}).text.strip()
    try:
        prod_descript = soup.find('div', {'id': 'product_description'}).find_next_sibling('p').text
    except AttributeError:
        prod_descript = "No description"
    category = soup.find('li', {'class': 'active'}).find_previous('a').text
    review_rating = soup.find('th', text='Number of reviews').find_next_sibling('td').text
    image_url = soup.find('div', {'class': 'item active'}).find_next('img')['src'].replace("../../", "")

    infos_product = {
        'product_page_url': url,
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


def get_image(url_image, path):
    r = requests.get(url_image)
    image_name = "/" + os.path.basename(url_image)
    with open(path + image_name, 'wb') as f:
        f.write(r.content)
