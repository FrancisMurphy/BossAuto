from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

from support.sale_word_bag import sale_position_words
from tool.common import down_page_single_load, ele_click

target_position_list = [
   ('销售经理', '南京', 100),
    ('大客户代表', '南京', 100),
    ('销售顾问', '南京', 100),
    # ('高薪销售岗', '淮安', 15),
    ('高薪销售岗', '滁州', 20),
    ('销售顾问', '宣城', 20),
    # ('医疗器械厂家', '驻马店', 25),
    # ('医疗器械厂家', '信阳', 25),
    ('医疗设备销售', '宿迁', 20),
    # ('销售助理', '南京', 50),
   # ('医疗器械厂家招', '六安', 10),
    # ('高薪销售岗', '宣城', 50),
    # ('销售顾问', '开封', 50),
    # ('销售顾问', '六安', 50),
    # ('销售顾问', '淮北', 50)
]


condition_keys = ['男', '大专', '本科', '今日活跃', '硕士']


def start_boss_graduate_recommend():
    driver = init_page()

    for target_position in target_position_list.__iter__():
        position = target_position[0:2]
        target_resume_num = target_position[2]
        print(" -----------------------开始------------------------")
        print(" ------------ 职位:{} 地区:{} 目标数量:{}沟通名单 -------------".format(position[0], position[1], target_resume_num))
        deal_position(driver, position, target_resume_num)
        print(" -----------------------结束------------------------")

    driver.quit()


def deal_position(driver, position_name, target_resume_num):
    result_seeker_name = set()
    select_position(driver, position_name)
    select_condition(driver, 22, 35, condition_keys)
    find_target(driver, target_resume_num, result_seeker_name)
    i = 1
    print(" ------------ 职位:{} 地区:{} 沟通名单 -------------".format(position_name[0], position_name[1]))
    for seeker_name in iter(result_seeker_name):
        print("第" + str(i) + "个，匹配人姓名：" + seeker_name)
        i = i + 1
    print(" -------------------------------------------------")
    sleep(1)


def find_target(driver, target_resume_num, result_seeker_name):
    old_resumes = []
    resume_num = 0
    while resume_num <= target_resume_num:
        new_resumes = driver.find_element(By.ID, 'recommend-list').find_elements(By.CLASS_NAME,
                                                                                 'candidate-list-content')
        target_resumes = new_resumes[len(old_resumes):]
        if len(target_resumes) == 0:
            print('无法获取更多简历，共打招呼{}次'.format(resume_num))
            break
        for resume in target_resumes:
            seeker_name = resume.find_element(By.CLASS_NAME, 'name').find_elements(By.TAG_NAME, 'span')[0].text

            try:
                activation = resume.find_element(By.CLASS_NAME, 'name').find_elements(By.TAG_NAME, 'span')[1].text
                if not '刚刚活跃今日活跃'.__contains__(activation):
                    print('[未匹配][{}][活跃度：{}]非今日活跃！'.format(seeker_name, activation))
                    continue
                if len(activation) == 0:
                    print('[未匹配][{}]未查到活跃度视为非今日活跃！'.format(seeker_name))
                    continue
            except NoSuchElementException:
                print('[未匹配][{}]未查到活跃度视为非今日活跃！'.format(seeker_name))
                continue

            # ele_click(driver, resume)
            # sleep(1.2)
            # try:
            #     ele_click(driver, driver.find_element(By.CLASS_NAME, 'resume-custom-close'))
            # except NoSuchElementException:
            #     sleep(2)
            #     ele_click(driver, driver.find_element(By.CLASS_NAME, 'resume-custom-close'))

            edu_exps = resume.find_element(By.CLASS_NAME, 'edu-exp-box').find_elements(By.TAG_NAME, 'li')
            if not check_graduation_date(edu_exps, seeker_name):
                continue

            try:
                work_exps = resume.find_element(By.CLASS_NAME, 'work-exp-box').find_elements(By.TAG_NAME, 'li')

            except NoSuchElementException:
                print('[未匹配][{}]未找到工作经验！'.format(seeker_name))
                continue

            if check_work_exp(work_exps, seeker_name):
                if resume_num >= target_resume_num:
                    break

                try:
                    greet_btn = resume.find_element(By.CLASS_NAME, 'btn-greet')
                    ele_click(driver, greet_btn)
                except NoSuchElementException:
                    print('[未匹配][{}]未找到打招呼按钮，跳过！'.format(seeker_name))
                    continue

                resume_num = resume_num + 1
                print('[最终匹配][{}][{}]！'.format(seeker_name, resume_num))
                result_seeker_name.add(seeker_name)
                sleep(0.2)
            else:
                print('[未匹配][{}]！'.format(seeker_name))

        if resume_num >= target_resume_num:
            break

        sleep(0.1)
        if down_page_single_load(driver):
            print("无法获取出新的简历，结束匹配！")
            break
        old_resumes = new_resumes.copy()
        new_resumes.clear()
        sleep(0.2)


def check_graduation_date(edu_exps, seeker_name):
    for edu_exp in edu_exps:
        graduation_date = edu_exp.find_element(By.CLASS_NAME, 'date').text.split('-')[1]
        if graduation_date >= "2022":
            print('[不匹配][{}]毕业年限检查不通过！'.format(seeker_name))
            return bool(0)
        exp_content = edu_exp.find_element(By.CLASS_NAME, 'exp-content').text
        if exp_content.__contains__('中专'):
            print('[不匹配][{}]学历包含中专检查不通过！'.format(seeker_name))
            return bool(0)
    return bool(1)


def check_work_exp(work_exps, seeker_name):
    for work_exp in work_exps:
        work_exp_content = work_exp.find_element(By.CLASS_NAME, 'exp-content').text
        for sale_key in sale_position_words:
            if work_exp_content.__contains__(sale_key):
                print('[匹配][{}] 工作经验[{}] 匹配关键字[{}]！'.format(seeker_name, work_exp_content, sale_key))
                return bool(1)
        return bool(0)


def init_page():
    edge_options = webdriver.EdgeOptions()
    # MAC
    # edge_options.add_argument('user-data-dir=/Users/frank/Library/Application Support/Microsoft Edge/Default')
    # PC
    edge_options.add_argument("user-data-dir=C:\\Users\\Zhumi\\AppData\\Local\\Microsoft\\Edge\\User Data1")
    driver = webdriver.Edge(options=edge_options)
    driver.get('https://www.zhipin.com/web/boss/recommend')
    sleep(0.5)
    switch_iframe(driver)
    return driver


def switch_iframe(driver):
    iframe = driver.find_element(By.TAG_NAME, 'iframe')
    driver.switch_to.frame(iframe)


def select_position(driver, position_name):
    driver.execute_script("arguments[0].click();",
                          driver.find_element(By.XPATH, '//*[@id="wrap"]/div/div/div[2]/div[1]'))
    driver.find_element(By.XPATH, '//*[@id="wrap"]/div/div/div[2]/div[2]/div/input').send_keys(position_name[0])
    position_ul = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[1]/div/div/div/div/div[2]/div[2]/ul')
    position_li_list = position_ul.find_elements(By.TAG_NAME, 'li')
    for position in position_li_list:
        position_item = position.find_element(By.TAG_NAME, 'span').text
        if position_item.__contains__(position_name[0]) & position_item.__contains__(position_name[1]):
            driver.execute_script("arguments[0].click();", position)
            sleep(1)


def select_condition(driver, target_min_age, target_max_age, conditions):
    condition = driver.find_element(By.CLASS_NAME, 'filter-btn')
    condition.click()
    sleep(0.1)
    condition_box = driver.find_element(By.CLASS_NAME, 'filter-container')
    select_condition_age(condition_box, driver, target_max_age, target_min_age)
    select_condition_item(condition_box, conditions)
    driver.find_element(By.CLASS_NAME, 'filter-dialog-footer').find_element(By.CLASS_NAME, 'btn-sure').click()
    sleep(4)


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
    age_rail = condition_box.find_element(By.CLASS_NAME, 'vue-slider-rail')
    age_dots = age_rail.find_elements(By.CLASS_NAME, 'vue-slider-dot')
    age_min_dot = age_dots[0]
    age_max_dot = age_dots[1]
    single_age_x_span = (age_max_dot.rect['x'] - age_min_dot.rect['x']) / 30
    if target_min_age > 16:
        ActionChains(driver).drag_and_drop_by_offset(age_min_dot, single_age_x_span * (target_min_age - 16),
                                                     0).perform()
        sleep(0.1)
    if target_max_age < 46:
        ActionChains(driver).drag_and_drop_by_offset(age_max_dot, - single_age_x_span * (46 - target_max_age),
                                                     0).perform()
        sleep(0.1)