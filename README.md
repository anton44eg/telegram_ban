# Налаштування (English version below)

Створити app в telegram https://my.telegram.org/apps

Заповнити всі поля. Будь який валідний URL має спрацювати.

Інколи telegram відповідає **ERROR**. Можна спробувати пізніше, або змінити _app name_, _short name_, _URL_.

# Запуск

Вказати API_ID і API_HASH змінні в команді нижче

> docker run -it -e API_ID= -e API_HASH= -v "state:/app/state" --pull=always -t anton44eg/telegram_ban python main.py

Залогінитись

# Setup

Create app in telegram https://my.telegram.org/apps

Fill all fields. Any valid URL should work.

Sometimes it responds with **ERROR** message - try different values for _app name_, _short name_ and _URL_ or try again a bit later.

# Run 

## Docker way

Set API_ID and API_HASH envs in command below

> docker run -it -e API_ID= -e API_HASH= -v "state:/app/state" --pull=always -t anton44eg/telegram_ban python main.py

Log in. Enjoy!
