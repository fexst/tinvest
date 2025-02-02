# Telegram Bot Project

## Overview
This project implements a Telegram bot that interacts with users to retrieve the latest price for financial instruments based on user-provided tickers. The bot uses an external SDK to fetch data about financial instruments, including their prices, and sends this information back to the user in a formatted message.

## Features
- **Start Command**: When users start the bot, they are prompted with a set of buttons to interact with it.  
- **Get Latest Price**: Users can request the latest price for a financial instrument by entering its ticker.  
- **Multiple Instruments**: If multiple instruments are found for a given ticker, users are given a choice to select the correct one.  
- **Error Handling**: The bot logs errors and sends notifications to the admin in case of critical issues.  

## Requirements
- Python 3.x  
- The following Python packages:  
  - `pyTelegramBotAPI` (for the Telegram Bot API)  
  - `logging` (for error logging)  
  - `configparser` (for reading configuration files)  
  - `time` (for retries in case of errors)  

You can install the required dependencies using pip:  

```bash
pip install pyTelegramBotAPI

Logs are generated for debugging and error tracking. The logs are stored in the console with the timestamp and log level. Critical errors, such as failures in sending admin notifications, will also be logged.

License
This project is open-source and available for use under the MIT License. Feel free to modify and distribute the code.
