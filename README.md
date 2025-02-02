Telegram Bot Project
This project implements a Telegram bot that interacts with users to retrieve the latest price for financial instruments based on user-provided tickers. The bot uses an external SDK to fetch data about financial instruments, including their prices, and sends this information back to the user in a formatted message.

Features
Start Command: When users start the bot, they are prompted with a set of buttons to interact with the bot.
Get Latest Price: Users can request the latest price for a financial instrument by entering its ticker.
Multiple Instruments: If multiple instruments are found for a given ticker, users are given a choice to select the correct one.
Error Handling: The bot logs errors and sends notifications to the admin in case of critical issues.
Requirements
Python 3.x
The following Python packages:
pyTelegramBotAPI (for the Telegram Bot API)
logging (for logging errors)
configparser (for reading configuration from a file)
time (for retries in case of errors)
You can install the required dependencies using pip:

bash
Копировать
Редактировать
pip install pyTelegramBotAPI
Configuration
This project requires a configuration file setting.ini with the following structure:

ini
Копировать
Редактировать
[TOKEN]
TOKEN_TG = your_telegram_bot_token_here

[ADMIN]
CHAT_ID = your_admin_chat_id_here
TOKEN_TG: Your Telegram bot token obtained from BotFather.
CHAT_ID: The chat ID of the admin to send error notifications to.
Functions
start(message):

Displays the start menu with buttons.
handle_button1(message):

Prompts the user to enter a ticker to retrieve the latest price.
process_parameter(message):

Handles the ticker input, fetches the relevant instrument data, and displays it to the user.
If multiple instruments are found, prompts the user to choose one.
handle_callback_query(call):

Handles user selection from multiple instruments and returns detailed information about the selected instrument.
notify_admin(error_message):

Notifies the admin in case of a critical error after retrying up to 5 times with a delay of 5 seconds.
Running the Bot
To run the bot, ensure that you have set up the configuration file (setting.ini) with the correct bot token and admin chat ID.

Then, simply run the script:

bash
Копировать
Редактировать
python bot_script.py
The bot will start, and you can interact with it in your Telegram app. If any errors occur, they will be logged, and the bot will try to restart automatically.

Logging
Logs are generated for debugging and error tracking. The logs are stored in the console with the timestamp and log level. Critical errors, such as failures in sending admin notifications, will also be logged.

License
This project is open-source and available for use under the MIT License. Feel free to modify and distribute the code.
