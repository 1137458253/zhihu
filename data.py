import json
import pathlib
import time

from selenium.webdriver.common.by import By

data_path = pathlib.Path('./data/')
data_path.mkdir(exist_ok=True)


def save_data(driver, key_word='妙可蓝多', href_num=50):
    driver.get('https://www.zhihu.com/signin?next=%2F')
    while True:
        if driver.current_url == 'https://www.zhihu.com/':
            break

    cookies = driver.get_cookies()
    with open(data_path / f'cookies.json', 'w') as f:
        json.dump(cookies, f, ensure_ascii=False)
    print("Cookies保存成功")
    driver.get(f'https://www.zhihu.com/search?type=content&q={key_word}')

    time.sleep(2)

    href_values = []
    text_values = []
    number = -1
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # 滑动到底部
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # 等待新内容加载
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        # 获取标题和链接
        xpath_expression = '//*[@class="ContentItem-title"]/span/div/a'
        elements = driver.find_elements(By.XPATH, xpath_expression)
        href_values = [elem.get_attribute('href') for elem in elements]
        text_values = [elem.text for elem in elements]
        if len(href_values) != number:
            number = len(href_values)
            print(f'当前数量：{number},目标数量：{href_num},请继续下滑')
        if len(href_values) >= href_num:
            break
    print("标题长度", len(text_values))
    print(text_values)

    print("链接长度", len(href_values))
    print(href_values)

    dictionary = {}

    for href, text in zip(href_values, text_values):
        dictionary.update({text: href})
    with open(data_path / f'{key_word}_{href_num}.json', 'w') as f:
        json.dump(dictionary, f, ensure_ascii=False)
