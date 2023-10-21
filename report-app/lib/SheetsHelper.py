import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from lib.TimeHelper import TimeHelper

class SheetsHelper:
    """
    Класс для работы с гугл таблицами
    """

    def __init__(self):
        CREDINTIALS_FILE = './creds.json'
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            CREDINTIALS_FILE,
            [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
        )

        self.spreadsheet_name = os.getenv('SHEETS_DOCUMENT_NAME')
        self.sheets_api = gspread.authorize(credentials)

    def setData(self, input_data):
        spreadsheet = self.sheets_api.open(self.spreadsheet_name)

        # Проверка наличия листа с названием месяца, если нет, то создаем его
        sheet_title = input_data['MONTH'].capitalize()
        sheet = None

        mount_time_plan = TimeHelper.getProdDateList()

        result = [
            ['', 'Детальный отчет по дням', '']
        ]
        users_report = [
            ['', 'Общее количество отработаных часов за месяц', ''],
            ['Сотрудник', 'Отработано часов', 'Отработано дней', 'Дней по плану', 'Часов по плану']
        ]

        result.append([('▴' * 300)])
        result.append([('▾' * 300)])

        if 'USERS' in input_data:
            for user in input_data['USERS']:
                result.append(['', ])
                user_full_info = [f"{user['NAME']} {user['SURNAME']}", user['TASKS_TOTAL_TIME_IN_MONTH']]
                result.append([f"{user['NAME']} {user['SURNAME']}"])
                report_day_count = 0

                if user['REPORTS_DAYS']:
                    for report in user['REPORTS_DAYS']:
                        report_day = ['', report['DATE'].replace("-", "."), '']
                        result.append(report_day)
                        result.append(['задача', 'ссылка на задачу', 'время'])

                        day_hours = '00:00:00'
                        day_hours_plan = '07:00:00'

                        if 'TASKS' in report:
                            report_day_count += 1

                            for task in report['TASKS']:
                                current_task = report['TASKS'][task]
                                task_result = [
                                    current_task["TASK_TITLE"],
                                    current_task["TASK_LINK"],
                                    current_task['TIME_TO_TASK']
                                ]
                                result.append(task_result)

                            if 'TASKS_TOTAL_TIME' in report:
                                day_hours = report['TASKS_TOTAL_TIME']

                        is_work_day = 'Да' if mount_time_plan['DATES'][report['DATE']] else 'Нет'
                        hours_in_plan = day_hours_plan if mount_time_plan['DATES'][report['DATE']] else '00:00:00'
                        day_result = ['', f'Рабочий день: {is_work_day}', f'Всего за день: {day_hours}', f'Плановое время: {hours_in_plan}', ]
                        result.append(day_result)

                        result.append([('-'*400)])

                result.append([('▴'*300)])
                result.append([('▾'*300)])

                user_full_info.append(report_day_count)
                user_full_info.append(mount_time_plan['WORKING_DAYS_COUNT'])
                user_full_info.append(mount_time_plan['WORKS_HOURS_COUNT'])
                users_report.append(user_full_info)

        try:
            sheet_is_exist = spreadsheet.worksheet(sheet_title)
            spreadsheet.del_worksheet(sheet_is_exist)
        except gspread.WorksheetNotFound:
            print(f'List {sheet_title} not found')

        insert_index = len(users_report) + 4
        report_size = insert_index + len(result)
        sheet = spreadsheet.add_worksheet(title=sheet_title, rows=report_size, cols=6)

        sheet.insert_rows(users_report, row=1)
        sheet.insert_rows(result, row=insert_index)