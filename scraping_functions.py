import requests
from bs4 import BeautifulSoup
import os


def get_soup(url):
    """
    Make a html request and get the html page.

            Parameter:
                url (str): An url string

            Returns:
                soup (bs4.BeautifulSoup) : html page
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def get_urls_prods(url_c):
    """
    Get all url of all produscts from one page of a category

            Parameter:
                url_c (str): An url of the first page of a category

            Returns:
                urls_prod_list (list): A list of all url products from a category
    """
    soup = get_soup(url_c)
    urls_prod_list = []
    for li in soup.find_all('li', {'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'}):
        url_prod = li.find('h3').find('a')['href'].replace("../../..", "")
        urls_prod_list.append(f"http://books.toscrape.com/catalogue{url_prod}")
    return urls_prod_list


def get_urls_categories(url_h):
    """
    Get all url of all category from home page

            Parameter:
                url_h (str): url of home page

            Returns:
                urls_all_cat_list (list): T list of all url of each category

    """
    soup = get_soup(url_h)
    urls_all_cat_list = []
    lis = soup.find('div', {'class': 'side_categories'}).findAll("li")
    for li in lis[1:]:
        url_category = li.find("a")["href"]
        urls_all_cat_list.append(f"http://books.toscrape.com/{url_category}")
    return urls_all_cat_list


# GET THE NAME OF ALL CATEGORIES  ==> LIST
def get_category_list(url_h):
    """
    Get the names of all categories

            Parameters:
                url_h (str): url of home page

            Returns:
                cat_list (list): The list of the name of each category
    """
    soup = get_soup(url_h)
    cat_list = []
    lis = soup.find('div', {'class': 'side_categories'}).findAll("li")
    for li in (lis[1:]):
        cat = li.find("a").text.strip()
        cat_list.append(cat)
    return cat_list


def get_prod_infos(url):
    """
    Get informations of one product

            Parameters:
                url (str): url of product page

            Returns:
                info_product (dict): A dictionary:
                                            keys: names of informations (str)
                                            values: datas (str)
    """
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
    """
    Make a get resquest and download image from the page of a product

            Parameters:
                url_image (str): url of the image
                path (str) : path where image is written

    """
    r = requests.get(url_image)
    image_name = "/" + os.path.basename(url_image)
    with open(path + image_name, 'wb') as f:
        f.write(r.content)


def loop_to_scrap_write_count(url_list, writer, path_im_dir):
    """
        1) Get informations for each product looping in each url of page product
        2) write informations in a csv file
        3) increment counter for counting number of products
        4) download image of the product

            Parameters:
                url_list (list): List of all product in a page of a category
                writer (_csv.writer): csv file that is created
                path_im_dir (str): path where image is downloaded

            Returns:
                cout (int): The number of products viewed
    """
    count = 0
    for link in url_list:
        infos = get_prod_infos(link)
        writer.writerow(infos)
        count += 1
        get_image(infos.get('image_url'), path_im_dir)

    return count
