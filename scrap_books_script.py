import csv
from scraping_functions import get_urls_categories, get_category_list, get_soup, get_urls_prods, get_prod_infos, \
     get_image
import os


url_home = "http://books.toscrape.com/"

counter = 0

# ================= CREATE DIRECTORY FOR SCRAPING ===================

path_dir = 'scrap_dir'
os.makedirs(path_dir, exist_ok=True)

print()
print("All categories : \n")

# ================== DISPLAY ALL CATEGORIES ==========================

for index, value in enumerate(get_category_list(url_home)):
    print(f"{index+1} - {value}")

print()
print("Ready to scrap")
input("Press Enter to continue...")
print()
print("scrap in progress...")

url_cat = get_urls_categories(url_home)

# ================ LOOP TO SCRAP ALL CATEGORIES =======================

for index, url in enumerate(url_cat):

    # ============= CREATE CATEGORY DIRECTORY ==========================

    path_cat_dir = os.path.join(path_dir, get_category_list(url_home)[index].lower(), '')
    os.makedirs(path_cat_dir, exist_ok=True)

    # ===============  CREATE IMAGES DIR ===============================

    path_im_dir = os.path.join(path_cat_dir, 'images', '')
    os.makedirs(path_im_dir, exist_ok=True)

    # =============== SETTING UP CSV FILE =============================

    path_csv = os.path.join(path_cat_dir, 'info_product.csv')
    csv_file = open(path_csv, 'w', newline='', encoding='utf-8')
    fieldnames = ['product_page_url', 'universal_product_code', 'title', 'price_including_tax', 'price_'
                  'excluding_tax', 'number_available', 'product_description', 'category', 'review_rating',
                  'image_url']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    # ============== NUMBER OF RESULTS IN THE CATEGORY ================

    results = int(get_soup(url).find('form', {'method': 'get'}).strong.text)
    pages = 1
    page_nb = 1

    # ================== NUMBER OF PAGES IN A CATEGORY =================

    if not int(results) % 20 == 0:
        pages = ((int(results) / 20) + 1)
        pages = int(pages)

    # ================== IF JUST 1 PAGE TO SCRAP =======================
    url_prod_list = get_urls_prods(url)
    if results <= 20:  # no pagination
        for link in url_prod_list:
            infos = get_prod_infos(link)
            writer.writerow(infos)
            counter += 1
            get_image(infos.get('image_url'), path_im_dir)
            # REMOVE # BELOW TO DISPLAY INFOS OF PRODUCTS (!! SLOWER !!)
            # pprint.pprint(get_prod_infos(link), sort_dicts=False)
            # print()
            # print("=" * 50)
            # print()

    # ======= IF MORE THAN ONE PAGE IN CATEGORY TO SCRAP ==> PAGINATION ========

    elif results > 20:
        while not page_nb > pages:
            next_page = "page-" + str(page_nb)
            url_pag = url.replace('index', next_page)
            get_soup(url_pag)
            url_pag_list = get_urls_prods(url_pag)
            for link in url_pag_list:
                infos = get_prod_infos(link)
                writer.writerow(infos)
                counter += 1
                get_image(infos.get('image_url'), path_im_dir)
                # REMOVE # BELOW TO DISPLAY INFOS OF PRODUCTS (!! SLOWER !!)
                # pprint.pprint(get_prod_infos(link), sort_dicts=False)
                # print()
                # print("=" * 50)
                # print()
            page_nb += 1

    csv_file.close()
print("Scrap completed")
print(f"Number of products  : {counter} ")
