from datetime import date, timedelta, datetime
import requests


class TimeHelper:
    @staticmethod
    def getDataObj():
        return date

    @staticmethod
    def leadToTimeFormat(input_seconds):
        """Метод преобразует секунды в формат чч:мм:сс"""
        delta = timedelta(seconds=input_seconds)
        time_obj = datetime(1, 1, 1) + delta

        return time_obj.strftime('%H:%M:%S')

    @staticmethod
    def getTimeInMonthFormat(input_seconds):
        """Метод преобразует секунды в формат ччч:мм:сс"""
        hours = input_seconds // 3600  # количество часов
        minutes = (input_seconds % 3600) // 60  # количество минут
        seconds = input_seconds % 60  # количество секунд

        return f"{hours:3}:{minutes:02}:{seconds:02}"


    @staticmethod
    def getDateList():
        """Метод возвращает список дат с первого дня месяца по текущий день"""
        dates = []
        start_date = datetime.today().replace(day=1)
        end_date = datetime.today()

        current_date = start_date

        while current_date <= end_date:
            formatted_date = current_date.strftime('%d-%m-%Y')
            dates.append(formatted_date)
            current_date += timedelta(days=1)

        return dates

    @staticmethod
    def getProdDateList():
        """Метод возвращает список дат с первого дня месяца по текущий день по производственному календарю"""
        dates = {}
        current_date = datetime.now()
        year = current_date.year
        month = f"{current_date.month:02}"
        working_days_count = 0

        requestUrl = 'https://isdayoff.ru/api/getdata'
        requestParams = {
            'year': year,
            'month': month
        }

        with requests.get(requestUrl, params=requestParams) as response:
            days_to_work_list = list(response.text)

            for index, value in enumerate(days_to_work_list, start=1):
                dataKey = current_date.replace(day=int(index)).strftime('%d-%m-%Y')
                dayValue = True if int(value) < 1 else False

                if dayValue:
                    working_days_count += 1

                dates[dataKey] = dayValue

        works_hour_count = (working_days_count * 7) * 3600

        return {
            'WORKING_DAYS_COUNT': working_days_count,
            'WORKS_HOURS_COUNT': TimeHelper.getTimeInMonthFormat(works_hour_count),
            'DATES': dates
        }


    @staticmethod
    def getMonthName():
        """Метод возвращает название текущего месяца"""

        current_month = datetime.now().month
        month_list = [
            'Январь',
            'Февраль',
            'Март',
            'Апрель',
            'Май',
            'Июнь',
            'Июль',
            'Август',
            'Сентябрь',
            'Октябрь',
            'Ноябрь',
            'Декабрь'
        ]

        return month_list[current_month - 1]
