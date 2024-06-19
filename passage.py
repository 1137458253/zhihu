import csv

from selenium.webdriver.common.by import By


def save_passage(driver, text, href):
    driver.get(href)
    passage1_values = []
    passage2_values = []
    try:
        xpath_expression = '//*[@class="RichText ztext Post-RichText css-1ygg4xu"]'
        elements = driver.find_elements(By.XPATH, xpath_expression)
        passage1_values = [elem.text for elem in elements]
    except:
        xpath_expression = '//*[@class="RichText ztext CopyrightRichText-richText css-1ygg4xu"]'
        elements = driver.find_elements(By.XPATH, xpath_expression)
        passage2_values = [elem.text for elem in elements]
    finally:
        passage_values = passage1_values + passage2_values
    if len(passage_values) != 0:
        with open('./data/data.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([f'{text}', f'{href}', f'{passage_values}'])
        print(f"{len(passage_values)}条数据写入完成")
    else:
        print("内容为空")
