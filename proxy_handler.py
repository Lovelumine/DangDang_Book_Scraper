# proxy_handler.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_proxy_settings():
    print("\n请选择代理设置:")
    print("1. 不使用代理")
    print("2. 使用HTTP代理")
    print("3. 使用HTTPS代理")
    print("4. 使用SOCKS代理")
    choice = input("请输入选择（1/2/3/4）: ")

    if choice == "1":
        return None
    elif choice in ["2", "3", "4"]:
        proxy_address = input("请输入代理地址（如 127.0.0.1:8080）: ")
        if choice == "2":
            return {"http": f"http://{proxy_address}"}
        elif choice == "3":
            return {"https": f"https://{proxy_address}"}
        elif choice == "4":
            return {"http": f"socks5://{proxy_address}", "https": f"socks5://{proxy_address}"}
    else:
        print("无效的选择。")
        return None

def get_chrome_proxy_options(proxies):
    chrome_options = Options()
    if proxies:
        if "http" in proxies:
            chrome_options.add_argument("--proxy-server=" + proxies["http"])
        elif "https" in proxies:
            chrome_options.add_argument("--proxy-server=" + proxies["https"])
        elif "socks5" in proxies:
            chrome_options.add_argument("--proxy-server=" + proxies["socks5"])
    return chrome_options

def init_browser_with_proxies():
    proxies = get_proxy_settings()
    chrome_options = get_chrome_proxy_options(proxies)
    browser = webdriver.Chrome(options=chrome_options)
    return browser, proxies
