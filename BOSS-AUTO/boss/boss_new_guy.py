from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

from support.sale_word_bag import sale_position_words
from support.condition_selector import *
from support.exp_checker import *
from support.driver_init import *
from tool.common import down_page_single_load, ele_click

condition_keys = ['男',  '本科', '今日活跃', '硕士']
target_resume_num = 10
result_seeker_name = set()


def start_boss_new_guy():
    driver = init_edge()
    select_condition(driver, 27, 44, condition_keys)
    find_nb_target(driver)
    i = 1
    for seeker_name in iter(result_seeker_name):
        print("第" + str(i) + "个，匹配人姓名：" + seeker_name)
        i = i + 1
    driver.quit()


def find_nb_target(driver):
    old_resumes = []
    resume_num = 0
    while resume_num <= target_resume_num:
        new_resumes = driver.find_element(By.CLASS_NAME, 'recommend-card-list').find_elements(By.CLASS_NAME,
                                                                                 'candidate-card-wrap')
        target_resumes = new_resumes[len(old_resumes):]
        if len(target_resumes) == 0:
            print('无法获取更多简历，共打招呼{}次'.format(resume_num))
            break
        for resume in target_resumes:
            resume_content = resume.find_element(By.CLASS_NAME,'card-inner')
            resume_name_wrap = resume_content.find_element(By.CLASS_NAME,'name-wrap')
            seeker_name = resume_name_wrap.find_element(By.CLASS_NAME, 'name').text
            try:
                activation = resume_name_wrap.find_element(By.CLASS_NAME, 'active-text').text
                if not '刚刚活跃今日活跃'.__contains__(activation):
                    print('[未匹配][{}][活跃度：{}]非今日活跃！'.format(seeker_name, activation))
                    continue
                if len(activation) == 0:
                    print('[未匹配][{}]未查到活跃度视为非今日活跃！'.format(seeker_name))
                    continue
            except NoSuchElementException:
                print('[未匹配][{}]未查到活跃度视为非今日活跃！'.format(seeker_name))
                continue

            ele_click(driver, resume)
            sleep(1)
            try:
                ele_click(driver, driver.find_element(By.CLASS_NAME, 'resume-custom-close'))
            except NoSuchElementException:
                sleep(1)

            edu_exps = resume.find_element(By.CLASS_NAME, 'edu-exps').find_elements(By.CLASS_NAME, 'timeline-item')
            if not check_graduation_date(edu_exps, seeker_name):
                continue

            try:
                work_exps = resume.find_element(By.CLASS_NAME, 'work-exps').find_elements(By.CLASS_NAME, 'timeline-item')

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

        sleep(1)
        if down_page_single_load(driver):
            print("无法获取出新的简历，结束匹配！")
            break
        old_resumes = new_resumes.copy()
        new_resumes.clear()
        sleep(1)


def init_edge():
    driver = init_driver()
    driver.get('https://www.zhipin.com/web/boss/recommend')
    sleep(1)
    switch_iframe(driver)
    driver.find_element(By.XPATH, '//*[@id="headerWrap"]/div/div/div[1]/ul/li[2]').click()
    return driver


def switch_iframe(driver):
    iframe = driver.find_element(By.TAG_NAME, 'iframe')
    driver.switch_to.frame(iframe)


