import os
import re
import json
from langchain_community.document_loaders import RecursiveUrlLoader, WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
from crawl4ai import *
import asyncio
load_dotenv()


def bs4_extractor(html: str) -> str:
    """
    Hàm trích xuất và làm sạch nội dung từ HTML
    Args:
        html: Chuỗi HTML cần xử lý
    Returns:
        str: Văn bản đã được làm sạch, loại bỏ các thẻ HTML và khoảng trắng thừa
    """
    soup = BeautifulSoup(html, "html.parser")  # Phân tích cú pháp HTML
    return re.sub(r"\n\n+", "\n\n", soup.text).strip()  # Xóa khoảng trắng và dòng trống thừa


async def crawl_data_using_crawl4AI(url):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=url,
        )
        return result.markdown



def craw_icd_web_light(url_data = "https://icd.who.int/browse/2025-01/mms/en"):
    data = ""
    driver = webdriver.Chrome()
    try:
        driver.get(url_data)
        menu_toggle = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "collapsed"))
        )
        menu_toggle.click()
        print("Đã mở menu trái thành công")
    except:
        print("Menu đã mở sẵn hoặc không có nút toggle")
    categories = driver.find_elements(By.CLASS_NAME, "titleinh")
    category_data = []
    for category in categories:
        category_name = category.text.strip()
        print(f"Đang xử lý danh mục: {category_name}")
        category.click()
        right_panel = WebDriverWait(driver , 10).until(
            EC.text_to_be_present_in_element((By.CLASS_NAME , "browserBodyRightContent") , category_name)
        )
        right_panel_contents = driver.find_elements(By.CLASS_NAME , "browserBodyRightContent")
        for right_panel_content in right_panel_contents:
            right_panel_content_text = right_panel_content.text
            data += "\n" + right_panel_content_text
    return data

def crawl_icd_web(url_data="https://icd.who.int/browse/2025-01/mms/en"):
    # Khởi tạo Chrome WebDriver
    driver = webdriver.Chrome()
    driver.get(url_data)

    # Danh sách để lưu dữ liệu menu
    menu_data = []
    right_panel_data = ""
    try:
        # Xử lý nút toggle menu trái nếu có
        try:
            pass
            menu_toggle = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "collapsed"))
            )
        #     # menu_toggle.click()
        #     # print("Đã mở menu trái thành công")
        except:
            print("Menu đã mở sẵn hoặc không có nút toggle")

        # Hàm đệ quy để crawl menu đa cấp
        def crawl_menu_level(parent_element=None, level=0):
            # Nếu không có parent_element, lấy các mục cấp cao nhất
            if(len(menu_data) <= 1) :
                if parent_element is None:
                    left_panel = driver.find_element(By.CLASS_NAME, "browserBodyLeftContent")
                else:
                    # Tìm các mục con trong parent_element
                    left_panel = parent_element.find_element(By.CSS_SELECTOR, "ul")
                categories = left_panel.find_elements(By.CSS_SELECTOR , "li")
                for category in categories:
                    try:
                        # Lấy tên danh mục
                        category_name = category.find_element(By.CLASS_NAME , "labelinh").text.strip()
                        print(f"{'  ' * level}Đang xử lý danh mục cấp {level}: {category_name}")

                        # Tạo dict để lưu thông tin danh mục
                        category_info = {
                            "name": category_name,
                            "level": level,
                            "children": [],
                            "content": ""
                        }
                        # Click vào danh mục
                        driver.execute_script("arguments[0].scrollIntoView();", category)
                        # print("sap click")
                        category.click()
                        time.sleep(1)  # Đợi load nội dung
                        has_sub_menu = False
                        try :
                            collapsed_icon = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.CLASS_NAME, f"collapsed"))
                            )
                            # collapsed_icon = category.find_element(By.CLASS_NAME, "collapsed")
                            print("Mo tab con")
                            collapsed_icon.click()
                            has_sub_menu = True
                        except Exception as e:
                            print(f"Khong co tab con")

                        time.sleep(1)
                        # Kiểm tra xem có submenu không
                        if has_sub_menu:
                            # Nếu có submenu, crawl đệ quy cấp tiếp theo
                            print(f"{'  ' * level}Tìm thấy submenu cho {category}")
                            category_info["children"] = crawl_menu_level(category, level + 1)
                            # lấy nội dung bên phải
                            right_panel = WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located((By.CLASS_NAME, "browserBodyRightContent"))
                            )

                            content_text = right_panel.text.strip()
                            right_panel_data = right_panel_data + "\n" + content_text
                            print(right_panel_data)
                        # Thêm danh mục vào danh sách kết quả
                        menu_data.append(category_info)

                    except Exception as e:
                        print(e)
                        print(f"k crawl")

                return menu_data

        # Bắt đầu crawl từ cấp cao nhất
        crawl_menu_level()

    finally:
        driver.quit()  # Đóng trình duyệt khi hoàn tất

    return right_panel_data


def crawl_web(url_data):
    session = requests.Session()
    session.verify = False
    """
    Hàm crawl dữ liệu từ URL với chế độ đệ quy
    Args:
        url_data (str): URL gốc để bắt đầu crawl
    Returns:
        list: Danh sách các Document object, mỗi object chứa nội dung đã được chia nhỏ
              và metadata tương ứng
    """
    # Tạo loader với độ sâu tối đa là 4 cấp
    loader = RecursiveUrlLoader(url=url_data, extractor=bs4_extractor, max_depth=4)
    docs = loader.load()  # Tải nội dung
    print('length: ', len(docs))  # In số lượng tài liệu đã tải

    # Chia nhỏ văn bản thành các đoạn 10000 ký tự, với 500 ký tự chồng lấp
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=500)
    all_splits = text_splitter.split_documents(docs)
    print('length_all_splits: ', len(all_splits))  # In số lượng đoạn văn bản sau khi chia
    return all_splits


def web_base_loader(url_data):
    session = requests.Session()
    session.verify = False  # Tắt xác thực SSL (không dùng cho production!)
    """
    Hàm tải dữ liệu từ một URL đơn (không đệ quy)
    Args:
        url_data (str): URL cần tải dữ liệu
    Returns:
        list: Danh sách các Document object đã được chia nhỏ
    """
    loader = WebBaseLoader(url_data)  # Tạo loader cơ bản
    docs = loader.load()  # Tải nội dung
    print('length: ', len(docs))  # In số lượng tài liệu

    # Chia nhỏ văn bản tương tự như trên
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
    all_splits = text_splitter.split_documents(docs)
    print(f"all_splits {all_splits} \ndocs : {docs}")
    return all_splits


def save_data_locally(documents, filename, directory):
    """
    Lưu danh sách documents vào file JSON
    Args:
        documents (list): Danh sách các Document object cần lưu
        filename (str): Tên file JSON (ví dụ: 'data.json')
        directory (str): Đường dẫn thư mục lưu file
    Returns:
        None: Hàm không trả về giá trị, chỉ lưu file và in thông báo
    """
    # Tạo thư mục nếu chưa tồn tại
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, filename)  # Tạo đường dẫn đầy đủ

    # Chuyển đổi documents thành định dạng có thể serialize
    data_to_save = [{'page_content': doc, 'metadata': {}} if isinstance(doc, str) else {'page_content': doc.page_content, 'metadata': doc.metadata} for doc in documents]
    # Lưu vào file JSON
    with open(file_path, 'w') as file:
        json.dump(data_to_save, file, indent=4)
    print(f'Data saved to {file_path}')  # In thông báo lưu thành công


async def main():
    """
    Hàm chính điều khiển luồng chương trình:
    1. Crawl dữ liệu từ trang web stack-ai
    2. Lưu dữ liệu đã crawl vào file JSON
    3. In kết quả crawl để kiểm tra
    """
    # Crawl dữ liệu từ trang docs của stack-ai
    # data = craw_icd_web_light('https://icd.who.int/browse/2025-01/mms/en')
    # print(f"right panel : {data}")
    # text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=500)
    # all_splits = text_splitter.split_text(data)
    # Lưu dữ liệu vào thư mục data_v2
    # save_data_locally(all_splits, 'dataICD.json', 'data')
    # print('data: ', data)  # In dữ liệu đã crawl
    # crawl_icd_web("https://icd.who.int/browse/2025-01/mms/en")

    #test crawl data from crawl4AI
    url = "https://icd.who.int/browse/2025-01/mms/en"
    data = crawl_icd_web(url_data=url)
    print(data)

# Kiểm tra nếu file được chạy trực tiếp
if __name__ == "__main__":
    asyncio.run(main())
