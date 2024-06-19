import json

from selenium import webdriver

from data import save_data
from passage import save_passage

key_word = '妙可蓝多'
href_num = 43

data_path = f'./data/{key_word}_{href_num}.json'
href_values = []
text_values = []


def load_data():
    # 加载数据
    with open(data_path, 'r', encoding='GBK') as f:
        dictionary = json.load(f)
        for key, value in dictionary.items():
            text_values.append(key)
            href_values.append(value)


if __name__ == '__main__':
    # 无头浏览器
    options = webdriver.EdgeOptions()
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = webdriver.Edge(options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
      """
    })

    save_data(driver=driver, key_word=key_word, href_num=href_num)
    load_data()
    index = 0
    for text, href in zip(text_values, href_values):
        try:
            print(index, text, href)
            save_passage(driver=driver, text=text, href=href)
            index += 1
        except Exception as e:
            print(e)
            continue
