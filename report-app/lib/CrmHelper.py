from lib.BitrixRequest import BitrixRequest
from lib.TimeHelper import TimeHelper
import os


class CrmHelper:
    """Класс для запросов в CRM bitrix24"""

    def __init__(self):
        self.users = []
        self.departament_id = os.getenv('DEPARTAMENT_ID')

        connect_to_orm = BitrixRequest()

        self.crmUrl = connect_to_orm.crm_adress
        self.crmRequest = connect_to_orm.connect
        self.__setUsers()

    def __setUsers(self):
        """Метод заполняет инфо о пользователях для экземпляра класса"""

        users_request_params = {
            'select': [
                "ID",
                "NAME",
                "LAST_NAME",
                "EMAIL"
            ],
            'filter': {
                "UF_DEPARTMENT": self.departament_id,
                "ACTIVE": True
            }
        }

        request_users = self.crmRequest.get_all('user.get', params=users_request_params)

        for user in request_users:
            user_info = {
                'id': user['ID'],
                'name': user['NAME'],
                'surname': user['LAST_NAME'],
                'email': user['EMAIL'],
            }

            self.users.append(user_info)

    def getUsers(self):
        """Метод возвращает список пользователей"""
        return self.users

    def getUsersTasksByDate(self, user_id, curr_date=False):
        """
        Метод заполняет инфо о пользователях для экземпляра класса
        по его id и дате формата dd-mm-yyyy
        """

        result = {}
        tasks_info_dict = {}

        current_date = curr_date if curr_date else TimeHelper.getDataObj().today()
        start_date = f"{current_date}T00:00:00+03:00"
        end_date = f"{current_date}T23:59:59+03:00"
        time_filter_param = {
            "order": {
                "ID": 'ASC'
            },
            "filter": {
                ">ID": 0,
                "USER_ID": user_id,
                ">=CREATED_DATE": start_date,
                "<=CREATED_DATE": end_date
            },
            "select": ["*"],
        }

        task_time = self.crmRequest.call('task.elapseditem.getlist', time_filter_param, raw=True)
        total_task_count = 0

        if 'result' in task_time:
            for task in task_time['result']:

                total_task_count += int(task['SECONDS'])

                if task['TASK_ID'] in result:
                    result[task['TASK_ID']]['SECONDS'] += int(task['SECONDS'])
                else:
                    result[task['TASK_ID']] = {
                        'USER_ID': task['USER_ID'],
                        'TASK_ID': task['TASK_ID'],
                        'SECONDS': int(task['SECONDS'])
                    }

        if len(result) > 0:
            # генерим формат времени, затраченного на задачу
            for task in result:
                seconds = result[task]['SECONDS']
                result[task]['TIME_TO_TASK'] = TimeHelper.leadToTimeFormat(seconds)

            # собираем пареметры для информации по задаче
            task_ids_keys_list = list(set([item for item in result]))
            tasks_params = {
                'select': [
                    "ID",
                    "TITLE",
                ],
                'filter': {
                    "ID": task_ids_keys_list,
                }
            }

            tasks_info = self.crmRequest.get_all('tasks.task.list', params=tasks_params)

            for task in result:
                task_title = [elem['title'] for elem in tasks_info if elem['id'] == result[task]['TASK_ID']][0]
                result[task]['TASK_TITLE'] = task_title
                result[task]['TASK_LINK'] = (f"https://{self.crmUrl}"
                                             f"/company/personal/user/{result[task]['USER_ID']}/"
                                             f"tasks/task/view/{result[task]['TASK_ID']}/")

            tasks_info_dict['TASKS'] = result
            tasks_info_dict['TASK_TOTAL_TIME'] = TimeHelper.leadToTimeFormat(total_task_count)
            tasks_info_dict['TASK_TOTAL_TIME_IN_SECONDS'] = total_task_count

        return tasks_info_dict

