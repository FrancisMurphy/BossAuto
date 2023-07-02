from datetime import datetime
from dateutil import rrule
from support.sale_word_bag import sale_position_words


def check_graduation_date(edu_exps, seeker_name):
    for edu_exp in edu_exps:
        graduation_date =edu_exp.text.split('\n')[0][4:]
        if graduation_date >= "2022":
            print('[不匹配][{}]毕业年限检查不通过！'.format(seeker_name))
            return bool(0)
    return bool(1)


def check_work_exp(work_exps, seeker_name):
    for work_exp in work_exps:
        work_exp_date = work_exp.text.split('\n')[0]
        if work_exp_date.__contains__('做过'):
            return bool(0)
        work_exp_content = work_exp.text.split('\n')[1]
        for sale_key in sale_position_words:
            if work_exp_content.__contains__(sale_key):
                print('[预匹配][{}] 工作经验[{}] 匹配关键字[{}] 工作时间[{}]！'.format(seeker_name, work_exp_content, sale_key, work_exp_date))
                #检查工作年限
                begin_date = work_exp_date[:7]
                if begin_date.__contains__('至今'):
                    return bool(0)
                end_date = work_exp_date[7:]
                if end_date.__contains__('至今'):
                    end_date = datetime.now().strftime("%Y.%m")
                begin_date_obj = datetime.strptime(begin_date, '%Y.%m')
                end_date_obj = datetime.strptime(end_date, '%Y.%m')
                year_sep = rrule.rrule(rrule.YEARLY, dtstart=begin_date_obj, until=end_date_obj).count()
                if year_sep >= 4:
                    return bool(1)
                else:
                    print('[不匹配][{}]一家公司下的销售年限未达到4年！'.format(seeker_name))
        return bool(0)