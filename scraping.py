import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv
import os


product_page_url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'

product_page = requests.get(product_page_url)
soup = BeautifulSoup(product_page.content, 'html.parser')
tables = soup.find(class_='table table-striped')
items = tables.find_all('td')
universal_product_code = items[0].get_text()
price_including_tax = items[3].get_text()
price_excluding_tax = items[2].get_text()
quantity_available = items[-2].get_text()
quantities_available = int(quantity_available[10:12])
titles = soup.find(class_='col-sm-6 product_main')
title = titles.find_all('h1')
book_title = title[0].get_text()
lists = soup.find(class_='breadcrumb')
list = lists.find_all('li')
category = list[2].get_text()
rating = titles.find_all('p')
review = rating[2].get('class')
review_rating = review[1]
content_inner = soup.find(class_='product_page')
content_ = content_inner.find_all('p')
product_description = content_[3].get_text()
images = soup.find_all('img')
for image in images:
    image_src = image['src']
    image_url = f"http://books.toscrape.com/{image_src.replace('../', '')}"
    book = pd.DataFrame(
          {
               'product_page_url': [product_page_url],
               'universal_product_code': [universal_product_code],
               'price_including_tax': [price_including_tax],
               'price_excluding_tax': [price_excluding_tax],
               'quantity_available': [quantities_available],
               'book_title': [book_title],
               'category': [category],
               'review_rating': [review_rating],
               'product_description': [product_description],
               'image_url': [image_url],
       })
# One book
    book.to_csv('book1.csv')



poetry_page_url = 'http://books.toscrape.com/catalogue/category/books/poetry_23/index.html'
poetry_page = requests.get(poetry_page_url)
s = BeautifulSoup(poetry_page.content, 'html.parser')
poetry_search = s.find('ol')
poetry_books = poetry_search.find_all('div', class_='image_container')
# scrape all links for poetry
poetry_book_urls = []
for poetry_book in poetry_books:
    poetry_book_src = poetry_book.find('a', href=True)
    poetry_book_src_1 = poetry_book_src.attrs['href']
    poetry_book_url = f"http://books.toscrape.com/catalogue/{poetry_book_src_1.replace('../', '')}"
    poetry_book_urls.append(poetry_book_url)
n = len(poetry_book_urls)

poetry_universal_products_code = []
poetry_price_including_taxes = []
poetry_price_excluding_taxes = []
poetry_quantities_1_available = []
poetry_books_title = []
poetry_categories = []
poetry_review_ratings = []
poetry_product_descriptions = []
poetry_images_url = []

# scrape all required information from list of poetry links
for i in range(0, n):
    url_poetry = poetry_book_urls[i]
    req_poetry = requests.get(url_poetry)
    soup_poetry = BeautifulSoup(req_poetry.content, 'html.parser')
    tables_poetry = soup_poetry.find(class_='table table-striped')
    items_poetry_s = tables_poetry.find_all('td')
    poetry_universal_product_code = items_poetry_s[0].get_text()
    poetry_universal_products_code.append(poetry_universal_product_code)
    poetry_price_including_tax = items_poetry_s[3].get_text()
    poetry_price_including_taxes.append(poetry_price_including_tax)
    poetry_price_excluding_tax = items_poetry_s[2].get_text()
    poetry_price_excluding_taxes.append(poetry_price_excluding_tax)
    poetry_quantity_available = items_poetry_s[-2].get_text()
    poetry_quantities_available = int(poetry_quantity_available[10:12])
    poetry_quantities_1_available.append(poetry_quantities_available)
    poetry_titles = soup_poetry.find(class_='col-sm-6 product_main')
    poetry_title = poetry_titles.find_all('h1')
    poetry_book_title = poetry_title[0].get_text()
    poetry_books_title.append(poetry_book_title)
    poetry_lists = soup_poetry.find(class_='breadcrumb')
    poetry_list = poetry_lists.find_all('li')
    poetry_category = poetry_list[2].get_text()
    poetry_categories.append(poetry_category)
    poetry_rating = poetry_titles.find_all('p')
    poetry_review = poetry_rating[2].get('class')
    poetry_review_rating = poetry_review[1]
    poetry_review_ratings.append(poetry_review_rating)
    poetry_content_inner = soup_poetry.find(class_='product_page')
    poetry_content_ = poetry_content_inner.find_all('p')
    poetry_product_description = poetry_content_[3].get_text()
    poetry_product_descriptions.append(poetry_product_description)
    poetry_images = soup_poetry.find_all('img', class_='')
    for poetry_image in poetry_images:
        poetry_image_src = poetry_image['src']
        poetry_image_url = f"http://books.toscrape.com/{poetry_image_src.replace('../', '')}"
        poetry_images_url.append(poetry_image_url)

poetry_book = pd.DataFrame(
      {
           'product_page_url': poetry_book_urls,
           'universal_product_code': poetry_universal_products_code,
           'price_including_tax': poetry_price_including_taxes,
           'price_excluding_tax': poetry_price_excluding_taxes,
           'quantity_available': poetry_quantities_1_available,
           'book_title': poetry_books_title,
           'category': poetry_categories,
           'review_rating': poetry_review_ratings,
           'product_description': poetry_product_descriptions,
           'image_url': poetry_images_url,
    })
# One category
poetry_book.to_csv('poetry_book1.csv')



all_category_page_url = 'http://books.toscrape.com/index.html'
all_category_page = requests.get(all_category_page_url)
all_s = BeautifulSoup(all_category_page.content, 'html.parser')
all_category_search = all_s.find('ul', class_='')
all_category_book_urls = []
all_category_books_urls = []
# scrape links of all categories from the sidebar
all_category_books = all_category_search.find_all('li')
for all_category_book in all_category_books:
    all_category_book_src = all_category_book.find('a', href=True)
    all_category_book_src_1 = all_category_book_src.attrs['href']
    all_category_book_url = 'http://books.toscrape.com/'+all_category_book_src_1.replace('../', '')
    all_category_book_urls.append(all_category_book_url)
    all_n = len(all_category_book_urls)
# scrape all categories links from all pages
category_new_list = []
category_universal_product_code = []
category_new_page_url = []
for j in range(0, 50):
    r_category = requests.get(all_category_book_urls[j])
    soup_category = BeautifulSoup(r_category.content, 'html.parser')
    # condition for the button "next" with use of a number of the last page
    if soup_category('li', class_='next'):
        number = soup_category.find('li', class_='current').get_text()
        total_number = int(number[40:42])
        for page in range(1, total_number + 1):
            category_new_page_url = f"{all_category_book_urls[j].replace('index.html', '')}page-{page}.html"
            category_next_page = requests.get(category_new_page_url)
            soup_category = BeautifulSoup(category_next_page.content, 'html.parser')
            category_new_list.append(category_new_page_url)

    else:

        category_new_page_url = all_category_book_urls[j]
        category_new_list.append(category_new_page_url)

all_urls = []
all_universal_product_code = []
all_price_including_tax = []
all_price_excluding_tax = []
all_quantities_available = []
all_book_title = []
all_category = []
all_review_rating = []
all_product_description = []
all_image_url = []
# scrape all books links from all pages
for k in range(0, 80):
    category_page = requests.get(category_new_list[k])
    soup = BeautifulSoup(category_page.content, 'html.parser')
    books_search = soup.find('section')
    all_books = books_search.find_all('div', class_='image_container')
    for all_book in all_books:
        all_book_src = all_book.find('a', href=True)
        all_books_src = all_book_src.attrs['href']
        book_url = f"http://books.toscrape.com/catalogue/{all_books_src.replace('../', '')}"
        all_urls.append(book_url)
# scrape all required information from all books
for h in range(0, 1000):
    all_books_url = all_urls[h]
    all_req = requests.get(all_books_url)
    all_s = BeautifulSoup(all_req.content, 'html.parser')
    tables = all_s.find(class_='table table-striped')
    items = tables.find_all('td')
    universal_product_code = items[0].get_text()
    all_universal_product_code.append(universal_product_code)
    price_including_tax = items[3].get_text()
    all_price_including_tax.append(price_including_tax)
    price_excluding_tax = items[2].get_text()
    all_price_excluding_tax.append(price_excluding_tax)
    quantity_available = items[-2].get_text()
    quantities_available = int(quantity_available[10:12])
    all_quantities_available.append(quantities_available)
    titles = all_s.find(class_='col-sm-6 product_main')
    title = titles.find_all('h1')
    book_title = title[0].get_text()
    all_book_title.append(book_title)
    lists = all_s.find(class_='breadcrumb')
    list = lists.find_all('li')
    category = list[2].get_text().replace('\n', '')
    all_category.append(category)
    rating = titles.find_all('p')
    review = rating[2].get('class')
    review_rating = review[1]
    all_review_rating.append(review_rating)
    content_inner = all_s.find(class_='product_page')
    content_ = content_inner.find_all('p')
    product_description = content_[3].get_text()
    all_product_description.append(product_description)
    images = all_s.find_all('img', class_='')

    for image in images:
        image_src = image['src']
        image_url = f"http://books.toscrape.com/{image_src.replace('../', '')}"
        all_image_url.append(image_url)

list_of_books = pd.DataFrame(
    {
        'product_page_url': all_urls,
        'universal_product_code': all_universal_product_code,
        'price_including_tax': all_price_including_tax,
        'price_excluding_tax': all_price_excluding_tax,
        'quantity_available': all_quantities_available,
        'book_title': all_book_title,
        'category': all_category,
        'review_rating': all_review_rating,
        'product_description': all_product_description,
        'image_url': all_image_url,
    })

# All books from bookscraper
list_of_books.to_csv('all_books.csv')

# split document on many csv regarding their categories
df = pd.read_csv('all_books.csv')
column_values = df['category'].unique()
for value in column_values:
    category_df = df[df['category'] == value]
    category_df.to_csv(f'category_{value}.csv', index = False)
# create a folder for images and download them in
if not os.path.isdir('images'):
    os.makedirs('images')
    for image in all_image_url:
        response = requests.get(image)
        open('images/' + image.split('/')[-1], 'wb').write(response.content)






