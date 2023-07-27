import requests
from scraper import get_book_info
from csv_handler import save_to_csv
from selenium import webdriver

books_info = []


# Use selenium to login and get cookies
browser = webdriver.Chrome()  # Specify the path to the webdriver if it is not in your PATH
browser.get('https://login.dangdang.com/?returnurl=http%3A%2F%2Fproduct.dangdang.com%2F22732944.html')

print("Please login in the browser and then press enter here.")
input()

# Get cookies and make them into the format that requests accepts
cookies = browser.get_cookies()
cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}

# Pass cookies to requests
session = requests.Session()
session.cookies.update(cookies_dict)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Referer': 'http://www.dangdang.com/'
}

while True:
    book_name = input("请输入书名，或输入'退出并导出'结束程序: ")
    if book_name == '退出并导出':
        save_to_csv(books_info)  # 当用户输入'退出并导出'时，调用save_to_csv函数
        break
    else:
        get_book_info(browser, session, book_name, headers,books_info)
