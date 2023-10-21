from dotenv import load_dotenv
from lib.CrmHelper import CrmHelper
from lib.TimeHelper import TimeHelper
from lib.SheetsHelper import SheetsHelper
import schedule
import time

# подгружаем виртуальное окружение
load_dotenv()


def getReportInCurrentMonth():
    """
    функция фозвращает отчеты по задачам за текущий месяц
    :return:
    {
        'MONTH': 'Август',
        'USERS': [
            {
                'ID': 321,
                'NAME': 'Иван'
                'SURNAME': 'Иванов'
                'REPORTS_DAYS': [
                    {
                        'DATE': dd-mm-yyyy,
                        'TASK_LIST': task_list,
                        'TASK_TOTAL_TIME':
                    }
                ],
                'TASKS_TOTAL_TIME_IN_MONTH': hhh:mm:ss
            }
        ]
    }
    """
    result_dict = {}
    crm_obj = CrmHelper()

    users_list = crm_obj.getUsers()
    result_dict['MONTH'] = TimeHelper.getMonthName()
    result_dict['USERS'] = []

    for user in users_list:
        total_time_in_month = 0
        user_obj = {
            'ID': user['id'],
            'NAME': user['name'],
        }

        if 'surname' in user:
            user_obj['SURNAME'] = user['surname']
        if 'email' in user:
            user_obj['EMAIL'] = user['email']

        user_obj['REPORTS_DAYS'] = []

        date_list = TimeHelper.getDateList()

        for day in date_list:
            report_obj = {}
            request_report = crm_obj.getUsersTasksByDate(user_obj['ID'], day)

            report_obj['DATE'] = day

            if 'TASKS' in request_report:
                report_obj['TASKS'] = request_report['TASKS']
                report_obj['TASKS_TOTAL_TIME'] = request_report['TASK_TOTAL_TIME']

                total_time_in_month += request_report['TASK_TOTAL_TIME_IN_SECONDS']

            user_obj['REPORTS_DAYS'].append(report_obj)

        user_obj['TASKS_TOTAL_TIME_IN_MONTH'] = TimeHelper.getTimeInMonthFormat(total_time_in_month).strip()
        result_dict['USERS'].append(user_obj)

    return result_dict


def createMonthReport():
    """
    функция записывает отчет за текущий месяц в google sheets

    """
    report = getReportInCurrentMonth()
    sheets = SheetsHelper()
    sheets.setData(report)

    import datetime
    import json

    now = datetime.datetime.now()
    formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
    with open("data1.json", "w", encoding='utf-8') as file:
        json.dump({"test": formatted_date}, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    schedule.every().hour.do(createMonthReport)

    while True:
        schedule.run_pending()
