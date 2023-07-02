from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

from support.sale_word_bag import sale_position_words
from tool.common import down_page_single_load, ele_click


def select_position(driver, position_name):
    driver.execute_script("arguments[0].click();",
                          driver.find_element(By.XPATH, '//*[@id="headerWrap"]/div/div/div[2]/div[1]'))
    driver.find_element(By.XPATH, '//*[@id="headerWrap"]/div/div/div[2]/div[2]/div[1]/input').send_keys(position_name[0])
    position_ul = driver.find_element(By.XPATH, '//*[@id="headerWrap"]/div/div/div[2]/div[2]/ul')
    position_li_list = position_ul.find_elements(By.TAG_NAME, 'li')
    for position in position_li_list:
        position_item = position.find_element(By.TAG_NAME, 'span').text
        if position_item.__contains__(position_name[0]) & position_item.__contains__(position_name[1]):
            driver.execute_script("arguments[0].click();", position)
            sleep(1)
            return bool(1)
    driver.execute_script("arguments[0].click();",
                          driver.find_element(By.XPATH, '//*[@id="headerWrap"]/div/div/div[2]/div[1]'))
    return bool(0)


def select_condition(driver, target_min_age, target_max_age, conditions):
    condition = driver.find_element(By.CLASS_NAME, 'filter-btn')
    condition.click()
    sleep(0.1)
    condition_box = driver.find_element(By.CLASS_NAME, 'filter-container')
    select_condition_age(condition_box, driver, target_max_age, target_min_age)
    select_condition_item(condition_box, conditions)
    driver.find_element(By.CLASS_NAME, 'filter-dialog-footer').find_element(By.CLASS_NAME, 'btn-sure').click()
    sleep(1)


def select_condition_item(condition_box, conditions):
    condition_item_all = condition_box.find_elements(By.CSS_SELECTOR, "a[ka*='recommend-']")

    def is_condition_item_effective(item):
        return not item.text.__contains__('不限')

    condition_item_effective_all = list(filter(is_condition_item_effective, condition_item_all))
    for condition in conditions:
        for condition_item in condition_item_effective_all:
            if condition_item.text == condition:
                condition_item.click()


def select_condition_age(condition_box, driver, target_max_age, target_min_age):
    sleep(1)
    age_rail = condition_box.find_element(By.CLASS_NAME, 'vue-slider-rail')
    age_dots = age_rail.find_elements(By.CLASS_NAME, 'vue-slider-dot')
    age_min_dot = age_dots[0]
    age_max_dot = age_dots[1]
    single_age_x_span = (age_max_dot.rect['x'] - age_min_dot.rect['x']) / 30
    if target_min_age > 16:
        ActionChains(driver).drag_and_drop_by_offset(age_min_dot, single_age_x_span * (target_min_age - 16),
                                                     0).perform()
    sleep(1)
    if target_max_age < 46:
        ActionChains(driver).drag_and_drop_by_offset(age_max_dot, - single_age_x_span * (46 - target_max_age),
                                                     0).perform()
    sleep(1)