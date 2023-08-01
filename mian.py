import requests
from scraper import get_book_info
from csv_handler import save_to_csv
from selenium import webdriver
import pickle
import os
from selenium.webdriver.chrome.options import Options
from proxy_handler import init_browser_with_proxies

books_info = []
COOKIES_PATH = "dangdang_cookies.pkl"

from proxy_handler import init_browser_with_proxies

browser, proxies = init_browser_with_proxies()
session = requests.Session()
if proxies:
    session.proxies = proxies




def login_and_get_cookies():
     
    browser.get('https://login.dangdang.com/?returnurl=http%3A%2F%2Fproduct.dangdang.com%2F22732944.html')
    print("Please login in the browser and then press enter here.")
    input()

    cookies = browser.get_cookies()
    with open(COOKIES_PATH, "wb") as f:
        pickle.dump(cookies, f)
    return cookies

def test_cookies_validity():
    """Test if the cookies are still valid."""
    try:
        response = session.get('http://www.dangdang.com/')  # Change this URL if needed
        return response.status_code == 200
    except Exception as e:
        print(f"Error testing cookies: {e}")
        return False
    
# Check if cookies file exists and load cookies
cookies_loaded = False  # Flag to check if cookies were loaded
if os.path.exists(COOKIES_PATH):
    with open(COOKIES_PATH, "rb") as f:
        cookies = pickle.load(f)
    cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}
    session.cookies.update(cookies_dict)
    if proxies:
        session.proxies = proxies
    if test_cookies_validity():
        print("Cookies successfully loaded and are valid!")
        cookies_loaded = True
    else:
        print("The stored cookies are no longer valid.")

# If cookies were not loaded or are invalid, login and get new ones
if not cookies_loaded:
    print("Opening browser for user login...")
    cookies = login_and_get_cookies()
    cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}
    session.cookies.update(cookies_dict)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Referer': 'http://www.dangdang.com/'
}


def read_book_names_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        # 读取所有书名，并且过滤掉空行和只有空白字符的行
        book_names = [line.strip() for line in file if line.strip()]
    return book_names

def get_book_names_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        # 去除空行和可能的乱码
        book_names = [line.strip() for line in file if line.strip()]
    return book_names

while True:
    print("\n选择输入方式: ")
    print("1. 手动输入书名")
    print("2. 从txt文件读取书名")
    print("3. 保存并退出")
    choice = input("请输入选择（1/2/3）: ")

    if choice == "1":
        while True:
            book_name = input("请输入书名，或输入'返回'返回上级菜单, '退出并导出'结束程序: ")
            if book_name == '退出并导出':
                save_to_csv(books_info)
                browser.close()
                exit(0)  # 结束程序
            elif book_name == '返回':
                break
            else:
                get_book_info(browser, session, book_name, headers, books_info)

    elif choice == "2":
        filename = input("请输入txt文件的路径（每行一个书名），或输入'返回'返回上级菜单: ")
        if filename == '返回':
            continue
        try:
            book_names = get_book_names_from_file(filename)
            for book_name in book_names:
                get_book_info(browser, session, book_name, headers, books_info)
        except Exception as e:
            print(f"读取文件时出现错误: {e}")

    elif choice == "3":
        save_to_csv(books_info)
        print("数据已保存。")
        browser.close()
        exit(0)  # 结束程序

    else:
        print("无效的选择。")
