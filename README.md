# Setup

Create app in telegram https://my.telegram.org/apps

Fill any valid URL there.

# Run 

Set API_ID and API_HASH envs in command below

> docker run -it -e API_ID= -e API_HASH= -v "state:/app/state" -t anton44eg/telegram_ban python main.py

Log in. Enjoy!
