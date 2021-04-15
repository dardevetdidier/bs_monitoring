import csv
import pprint
from functions import *
import os


# SETTING UP CSV FILE
csv_file = open('info_product.csv', 'w', newline='')
fieldnames = ['product_page_url', 'universal_product_code', 'title', 'price_including_tax', 'price_'
              'excluding_tax', 'number_available', 'product_description', 'category', 'review_rating',
              'image_url']
writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
writer.writeheader()

# CREATE IMAGES DIR
path = 'images'
if not os.path.exists(path):
    os.makedirs(path)

# # CREATE CSV FILE FROM DICTIONARY
# def create_csv_file(infos_dict):
#     writer.writerow(infos_dict)
#
#
# # GET HTML PAGE
# def get_soup(url):
#     response_cat = requests.get(url)
#     soup = BeautifulSoup(response_cat.content, 'lxml')
#     return soup
#
#
# # GET URL OF 1 PRODUCT
# def get_url_prod(url):
#     url_prod = get_soup(url).find('h3').find('a')['href'].replace("../../..", "")
#     return f"http://books.toscrape.com/catalogue{url_prod}"
#
#
# # GET URLS OF ALL PRODUCTS FROM 1 CATEGORY PAGE ==> LIST
# def get_urls_prods(url):
#     urls_prod_list = []
#     for li in get_soup(url).find_all('li', {'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'}):
#         url_prod = li.find('h3').find('a')['href'].replace("../../..", "")
#         urls_prod_list.append(f"http://books.toscrape.com/catalogue{url_prod}")
#         # print(f"http://books.toscrape.com/catalogue{url_prod}")
#
#     return urls_prod_list
#
#
# # GET URLS OF ALL CATEGORIES FROM HOME PAGE --> LIST
# def get_urls_categories(url):
#     urls_all_cat_list = []
#     lis = get_soup(url).find('div', {'class': 'side_categories'}).findAll("li")
#     for li in lis[1:]:
#         a = li.find("a")
#         url_category = a["href"]
#         urls_all_cat_list.append(f"http://books.toscrape.com/{url_category}")
#
#     print(urls_all_cat_list)
#
#
# # GET INFOS OF 1 PRODUCT ==> DICT
# def get_prod_infos(url):
#     product_page_url = url
#     upc = get_soup(url).find('th', text='UPC').find_next_sibling('td').text
#     title = get_soup(url).find('h1').text
#     price_incl_tax = get_soup(url).find('th', text='Price (incl. tax)').find_next_sibling('td').text
#     price_excl_tax = get_soup(url).find('th', text='Price (excl. tax)').find_next_sibling('td').text
#     num_available = get_soup(url).find('p', {'class': 'instock availability'}).text.strip()
#     try:
#         prod_descript = get_soup(url).find('div', {'id': 'product_description'}).find_next_sibling('p').text
#     except AttributeError:
#         prod_descript = "No description"
#     category = get_soup(url).find('li', {'class': 'active'}).find_previous('a').text
#     review_rating = get_soup(url).find('th', text='Number of reviews').find_next_sibling('td').text
#     image_url = get_soup(url).find('div', {'class': 'item active'}).find_next('img')['src'].replace("../../", "")
#
#     infos_product = {
#         'product_page_url': product_page_url,
#         'universal_product_code': upc,
#         'title': title,
#         'price_including_tax': price_incl_tax,
#         'price_excluding_tax': price_excl_tax,
#         'number_available': num_available,
#         'product_description': prod_descript,
#         'category': category,
#         'review_rating': review_rating,
#         'image_url': 'http://books.toscrape.com/' + image_url
#     }
#     return infos_product
#     # print("product_page_url : " + product_page_url)
#     # print("universal_product_code : " + upc)
#     # print("title : " + title)
#     # print("price_including_tax : " + price_incl_tax)
#     # print("price_excluding_tax : " + price_excl_tax)
#     # print("number_available : " + num_available)
#     # print("product_description : " + prod_descript)
#     # print("category : " + category)
#     # print("review_rating = " + review_rating)
#     # print("image_url : " + "http://books.toscrape.com/" + image_url)

url_home = "http://books.toscrape.com/"
# url_cat = "http://books.toscrape.com/catalogue/category/books/womens-fiction_9/index.html"

# TODO : fonction liste des produits par catégorie
# DISPLAY ALL CATEGORIES TO CHOOSE
for i in get_category_list(url_home):
    print(i)

print()

# USER CATEGORY CHOICE
choice_cat = ''
while not (choice_cat.isdigit() and 1 <= int(choice_cat) <= len(get_category_list(url_home))):
    choice_cat = input("choisir une catégorie : ")

url_cat = get_urls_categories(url_home)[int(choice_cat)-1]


# GET NUMBER OF RESULTS IN A CATEGORY
results = int(get_soup(url_cat).find('form', {'method': 'get'}).strong.text)
pages = 1
page_nb = 1

print()
print(f"La catégorie contient {results} produit(s)\n")
print("Afficher tous les produits :  1  |  choisir un produit : 2 ")
choice_prod = input("Votre Choix ? ")
print()

# DISPLAY ALL PRODUCTS IN THIS CATEGORY
if choice_prod == '1':
    # COUNT NUMBER OF PAGES IN A CATEGORY
    if not int(results) % 20 == 0:
        pages = ((int(results) / 20) + 1)
        pages = int(pages)

    # IF JUST 1 PAGE
    if results <= 20:  # no pagination
        for link in get_urls_prods(url_cat):
            # writer.writerow(get_prod_infos(link))
            pprint.pprint(get_prod_infos(link), sort_dicts=False)
            get_image((get_prod_infos(link).get('image_url')))
            print()

    # IF MORE THAN ONE PAGE IN CATEGORY ==> PAGINATION
    else:
        while not page_nb > pages:
            next_page = "page-" + str(page_nb)
            url_cat_pag = url_cat.replace('index', next_page)
            get_soup(url_cat_pag)
            for link in get_urls_prods(url_cat_pag):
                # writer.writerow(get_prod_infos(link))
                pprint.pprint(get_prod_infos(link), sort_dicts=False)
                print()
            page_nb += 1
else:
    pass
csv_file.close()

# get product informations with BS
#     product_page_url = url_prod
#     upc = soup.find('th', text='UPC').find_next_sibling('td').text
#     title = soup.find('h1').text
#     price_incl_tax = soup.find('th', text='Price (incl. tax)').find_next_sibling('td').text
#     price_excl_tax = soup.find('th', text='Price (excl. tax)').find_next_sibling('td').text
#     num_available = soup.find('p', {'class': 'instock availability'}).text.strip()
#     prod_descript = soup.find('div', {'id': 'product_description'}).find_next_sibling('p').text
#     category = soup.find('li', {'class': 'active'}).find_previous('a').text
#     review_rating = soup.find('th', text='Number of reviews').find_next_sibling('td').text
#     image_url = soup.find('div', {'class': 'item active'}).find_next('img')['src'].replace("../../", "")


