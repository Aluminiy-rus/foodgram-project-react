# praktikum_new_diplom
# yamdb_final

![example workflow](https://github.com/Aluminiy-rus/foodgram-project-react/actions/workflows/yamdb_workflow.yml/badge.svg)


На данный момент(5.09.2022) посмотреть доступные эндпойнты проекта можно по адресу http://84.201.159.93/redoc/

---

#### **Об авторе:**


* Имя: Иннокентий.
* Род деятельности: Работаю. Учусь на курсах по программированию от Яндекса. Помогаю чем могу сокурсникам в Discord'e и Slack
* Интересы: Технологии, программирование, наука, DataScience, автоматизация, Машинное обучение, Нейросети, видеоигры, manga/anime.
* Контакты: https://github.com/Aluminiy-rus

---

#### **Описание:**
Проект FOODGRAM-PROJECT-REACT - сайт Foodgram, «Продуктовый помощник» онлайн-сервис и API для него. На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

---

#### **Подготовка сервера**

1. Войдите на свой удаленный сервер в облаке.
2. Остановите службу nginx:

```
sudo systemctl stop nginx 
```

3. Установите docker:

```
sudo apt install docker.io 
```

4. Установите docker-compose, с этим вам поможет официальная документация https://docs.docker.com/compose/install/

5. Скопируйте файлы docker-compose.yaml и nginx/default.conf из проекта на сервер в home/<ваш_username>/docker-compose.yaml и home/<ваш_username>/nginx/default.conf соответственно.

6. Добавьте в GitHub Actions Secrets переменные для подключения к серверу:
```
HOST                # IP-адрес вашего сервера
USER                # Имя пользователя для подключения к серверу
SSH_KEY             # Ключ с компьютера, имеющего доступ к боевому серверу
PASSPHRASE          # Если при создании ssh-ключа вы использовали фразу-пароль
```

7. Добавьте в GitHub Actions Secrets переменные окружения для работы базы данных:
```
DB_ENGINE           # Движок БД(базы данных)
DB_NAME             # Имя БД
POSTGRES_USER       # Пользовтаель БД
POSTGRES_PASSWORD   # Пароль БД
DB_HOST             # IP-адрес БД
DB_PORT             # Порт БД
SECRET_KEY          # Django SECRET_KEY
```

8. Для отслеживания выполнения workflow с помощью телеграм-аккаунта добавьте в GitHub Actions Secrets переменные окружения указанные ниже:
```
TELEGRAM_TO         # ID своего телеграм-аккаунта. Узнать свой ID можно у бота @userinfobot
TELEGRAM_TOKEN      # Токен вашего бота. Получить этот токен можно у бота @BotFather
```