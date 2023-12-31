# Telegram Bot

#### Video Demo: https://youtu.be/U1sVq_TBgNY

#### Description:

This Telegram bot is designed to run predefined macros, making it a tool for automating tasks. Built with aiogram 3 and FastAPI. The bot's functionality can be extended or customized.

## Technology Stack

- **Python 3.10+**: The primary programming language used for bot development.
- **aiogram 3.2**: An efficient framework for Telegram Bot API, facilitating asynchronous programming and offering a rich set of features for bot development.
- **FastAPI**: A high-performance web framework for building APIs, known for its speed and ease of use, serving the webhook endpoint for the bot.
- **APScheduler**: A task scheduler to run macros at predetermined intervals.
- **SQLite**

## Project Structure

- **`app.py`**: The main entry point of the bot. It initializes the bot, sets up the webhook, and starts the event loop.
- **`config/`**: Configuration directory containing all necessary tokens, database connection details, and other configurations.
- **`handlers/`**: This directory contains modules for different types of bot command handlers
- **`states/`**: Contains FSM states
- **`data/`**: Defines database models and structures, typically used for storing and retrieving macro and user data.
- **`keyboards/`**: Contains keyboards for InlineKeyboards
- **`requirements.txt`**: Lists all the Python dependencies required for the bot to run.
