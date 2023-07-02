from selenium.common.exceptions import StaleElementReferenceException

from support.condition_selector import *
from support.exp_checker import *
from support.driver_init import *

target_position_list = [
     ('大客户销代表', '南京', 20),
     #('销售顾问', '南京', 20),
     ('高级销售', '南京', 20),
    #('医疗器械销售经理', '南京', 20),
     #('销售顾问', '宣城', 10),
    #('高级销售岗', '开封', 15),
    #('高级销售岗', '芜湖', 25),
    #('高薪销售岗', '平顶山', 15),
    # ('高级销售经理', '南京', 20),
    # ('高级销售岗', '郑州', 25),
    # ('高级销售岗', '武汉', 15),
    # ('销售岗位', '滁州', 10)
]


condition_keys = ['男',  '本科', '今日活跃', '硕士']

def start_boss_recommend():
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
    if not select_position(driver, position_name):
        return
    select_condition(driver, 27, 39, condition_keys)
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
        new_resumes = driver.find_element(By.CLASS_NAME, 'card-list').find_elements(By.CLASS_NAME,
                                                                                 'candidate-card-wrap')
        target_resumes = new_resumes[len(old_resumes):]
        if len(target_resumes) == 0:
            print('无法获取更多简历，共打招呼{}次'.format(resume_num))
            break
        for resume in target_resumes:
            try:
                resume_content = resume.find_element(By.CLASS_NAME, 'card-inner')
            except StaleElementReferenceException:
                continue
            resume_name_wrap = resume_content.find_element(By.CLASS_NAME, 'name-wrap')
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

            # ele_click(driver, resume)
            # sleep(1)
            # try:
            #     ele_click(driver, driver.find_element(By.CLASS_NAME, 'resume-custom-close'))
            # except NoSuchElementException:
            #     sleep(1)

            edu_exps = resume.find_element(By.CLASS_NAME, 'edu-exps').find_elements(By.CLASS_NAME, 'timeline-item')
            if not check_graduation_date(edu_exps, seeker_name):
                continue

            try:
                work_exps = resume.find_element(By.CLASS_NAME, 'work-exps').find_elements(By.CLASS_NAME,
                                                                                          'timeline-item')

            except NoSuchElementException:
                print('[未匹配][{}]未找到工作经验！'.format(seeker_name))
                continue

            if check_work_exp(work_exps, seeker_name):
                if resume_num >= target_resume_num:
                    break

                try:
                    greet_btn = resume.find_element(By.CLASS_NAME, 'btn-greet')
                    # ele_click(driver, greet_btn)
                    print('[已匹配][{}]点击打招呼按钮！'.format(seeker_name))
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


def init_page():
    driver = init_driver()
    driver.get('https://www.zhipin.com/web/chat/recommend')
    sleep(0.5)
    switch_iframe(driver)
    return driver


def switch_iframe(driver):
    iframe = driver.find_element(By.TAG_NAME, 'iframe')
    driver.switch_to.frame(iframe)

