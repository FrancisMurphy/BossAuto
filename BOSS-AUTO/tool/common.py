from selenium import webdriver
from time import sleep


# 元素点击
def ele_click(driver, ele):
    webdriver.ActionChains(driver).move_to_element(ele).click(ele).perform()


# 页面下拉出所有页面进行加载
def down_page_all_load(driver):
    height = 0
    while True:
        new_height = driver.execute_script('return document.body.scrollHeight;')
        if new_height > height:
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            height = new_height
            sleep(1)
        else:
            print("滚动条已经处于页面最下方，已无更多内容!")
            driver.execute_script('window.scrollTo(0, 0)')  # 页面滚动到顶部
            break


# 页面下拉一页
def down_page_single_load(driver):
    height = 0
    every_fresh_page_num = 1
    fresh_page = 0
    # while fresh_page < every_fresh_page_num:
    new_height = driver.execute_script('return document.body.scrollHeight;')
    if new_height > height:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        height = new_height
        sleep(1)
        return bool(0)
    else:
        print("滚动条已经处于页面最下方!")
        driver.execute_script('window.scrollTo(0, 0)')  # 页面滚动到顶部
        return bool(1)
        # break
    fresh_page = fresh_page + 1