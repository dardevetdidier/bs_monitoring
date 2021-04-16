import csv
import pprint
from scraping_functions import get_urls_categories, get_category_list, get_soup, get_urls_prods, get_prod_infos, \
    get_image
import os

# TODO : Message de fin scrap OK et download images OK (indiquer nb)

url_home = "http://books.toscrape.com/"
# url_cat = "http://books.toscrape.com/catalogue/category/books/womens-fiction_9/index.html"

print()
print("All categories : \n")

# ================== DISPLAY ALL CATEGORIES ==========================

for index, value in enumerate(get_category_list(url_home)):
    print(f"{index+1} - {value}")

print()
print("Ready to scrap")
input("Press Enter to continue...")

url_cat = get_urls_categories(url_home)

# ================ LOOP TO SCRAP ALL CATEGORIES =======================

for url in url_cat:

    # ============= CREATE CATEGORY DIRECTORY ==========================
    # TODO : Créer dossier de la categorie
    path_cat_dir = get_category_list(url_home)

    # ===============  CREATE IMAGES DIR ===============================

    path_im_dir = 'images'
    if not os.path.exists(path_im_dir):
        os.makedirs(path_im_dir)

    # =============== SETTING UP CSV FILE =============================

    csv_file = open('info_product.csv', 'w', newline='')
    fieldnames = ['product_page_url', 'universal_product_code', 'title', 'price_including_tax', 'price_'
                                                                                                'excluding_tax',
                  'number_available', 'product_description', 'category', 'review_rating',
                  'image_url']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    # ============== NUMBER OF RESULTS IN THE CATEGORY ================

    results = int(get_soup(url).find('form', {'method': 'get'}).strong.text)
    pages = 1
    page_nb = 1

    # ============== COUNT NUMBER OF PAGES IN A CATEGORY ==============

    if not int(results) % 20 == 0:
        pages = ((int(results) / 20) + 1)
        pages = int(pages)

    # ====================== IF JUST 1 PAGE ==========================

    if results <= 20:  # no pagination
        for link in get_urls_prods(url):
            # writer.writerow(get_prod_infos(link))
            pprint.pprint(get_prod_infos(link), sort_dicts=False)
            get_image((get_prod_infos(link).get('image_url')), path_im_dir)
            print()

    # ======= IF MORE THAN ONE PAGE IN CATEGORY ==> PAGINATION =======

    else:
        while not page_nb > pages:
            next_page = "page-" + str(page_nb)
            url_pag = url.replace('index', next_page)
            get_soup(url_pag)
            for link in get_urls_prods(url_pag):
                # writer.writerow(get_prod_infos(link))
                pprint.pprint(get_prod_infos(link), sort_dicts=False)
                get_image((get_prod_infos(link).get('image_url')), path_im_dir)
                print()

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
