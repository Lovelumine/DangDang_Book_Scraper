from httpcore import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.common.exceptions import WebDriverException
import re



def get_book_info_from_url(browser, session, url, headers, books_info):
    max_retries = 2  # 设置最大重试次数
    retries = 0

    while retries < max_retries:
        try:
            # Use the same selenium browser to get dynamic content
            browser.get(url)

            # Wait until the dynamic content is loaded
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'descrip')))
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1')))
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.t1 a')))
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.pro_content li')))

            # Now we have the dynamically loaded content, let's parse it with BeautifulSoup
            soup = BeautifulSoup(browser.page_source, 'html.parser')

            # Find and print book title
            title = soup.find('h1').text.strip()

            print("书名: ", title)

            # Find and print author and publisher
            author = soup.find('span', attrs={'class': 't1'}).find_all('a')
            print("作者: ", author[0].text if author else 'N/A')

            publisher = soup.find('span', attrs={'dd_name': '出版社'})
            print("出版社: ", publisher.text.replace('出版社:', '').strip() if publisher else 'N/A')

            # Find and print book price, ISBN, and publication date
            # Find and print book price
            price = soup.find('div', attrs={'id': 'original-price'})
            if price:
                print("定价: ", price.text.replace('¥', '').strip())
            else:
                print("定价: ", 'N/A')

            product_info = soup.find('div', attrs={'class': 'pro_content'}).find_all('li')
            for info in product_info:
                text = info.text
                if "ISBN" in text:
                    print("ISBN: ", text.split('：')[-1])

            # 查找并打印出版时间
            pub_time = soup.find('span', string=re.compile('出版时间'))
            if pub_time:
                print("出版时间: ", pub_time.text.replace('出版时间:', '').strip())
            else:
                print("出版时间: ", 'N/A')
            # 内容简介
            content_container = soup.find('div', attrs={'id': 'content'})
            if content_container is not None:
                content_div = content_container.find('div', attrs={'class': 'descrip'})
            else:
                content_div = None
            content_str = ""  # 初始化一个空字符串来存储所有的内容
            if content_div:
                content_paragraphs = content_div.find_all('p')
                for paragraph in content_paragraphs:
                    if paragraph.text.strip():  # Ignore empty paragraphs
                        content_str += paragraph.text.strip()+"\n"  # 将每个段落的文本添加到字符串中
                print("内容: ", content_str)  # 打印整个内容
            else:
                print("内容: ", 'N/A')

            book_info = {
                    '书名': title,
                    '作者': author[0].text if author else 'N/A',
                    '出版社': publisher.text.replace('出版社:', '').strip() if publisher else 'N/A',
                    '定价': price.text.replace('¥', '').strip() if price else 'N/A',
                    'ISBN': '',
                    '出版时间': pub_time.text.replace('出版时间:', '').strip() if pub_time else 'N/A',
                    '内容': content_str
                }
            for info in product_info:
                text = info.text
                if "ISBN" in text:
                    book_info['ISBN'] = text.split('：')[-1]

            # 将这本书的信息添加到列表中
            books_info.append(book_info)
            break

        except TimeoutException:
            retries += 1  # 增加重试次数
            print(f"书籍的详情页面加载超时。正在尝试重新加载...({retries}/{max_retries})")
            browser.refresh()  # 刷新页面

        except WebDriverException:
            retries += 1
            print(f"Selenium WebDriver 出现问题。正在尝试重新加载...({retries}/{max_retries})")
            browser.refresh()  # 刷新页面

        except Exception as e:
            print(f"处理书籍时发生错误: {e}")
            break

    if retries == max_retries:
        print(f"无法加载书籍的详情页面。请检查网络连接或稍后再试。")

def get_book_info(browser, session, book_title, headers, books_info):
    try:
        search_url = 'http://search.dangdang.com/?key={}&act=input'.format(book_title)
        response = session.get(search_url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the book detail URL and add 'http:' if necessary
        book_detail_a_tag = soup.find('a', attrs={'name': 'itemlist-title'})
        if not book_detail_a_tag:
            print(f"未找到与'{book_title}'相关的书籍。")
            return

        book_detail_url = book_detail_a_tag['href']
        if book_detail_url.startswith('//'):
            book_detail_url = 'http:' + book_detail_url
        print(book_detail_url)

        get_book_info_from_url(browser, session, book_detail_url, headers, books_info)
    except Exception as e:
        print(f"处理书籍'{book_title}'时发生错误: {e}")

