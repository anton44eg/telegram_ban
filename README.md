# Setup

Create app in telegram https://my.telegram.org/apps

Fill any valid URL there.

Sometimes it responds with **ERROR** message - try different values for app name, short name and URL or try again a bit later.

# Run 

## Docker way

Set API_ID and API_HASH envs in command below

> docker run -it -e API_ID= -e API_HASH= -v "state:/app/state" --pull=always -t anton44eg/telegram_ban python main.py

Log in. Enjoy!
