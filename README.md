# Собираем часы из bx24 в google sheets

порядок действий:
1) создаем вебхук и заполняем файл ./report-app/.env
2) создаем технический аккаунт в google sheets и заполняем файлик ./report-app/creds.json
3) запускаем 
```bash
docker-compose -up -d
```
4) заходим в контейнер 
```bash
docker exec -it report-app /bin/bash
```
5) выполняем внутри контейнера** 
```bash
python3 main.py
```
** - хотел потестить работу с библиотекой schedule, поэтому сделал так, а не на cron` 

не забываем проверить доступы внутри вэбхука bx24 и настройки gs