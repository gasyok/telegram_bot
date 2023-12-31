# Telegram Bot

https://github.com/Gasyok/final_project.git

#### Video Demo: https://youtu.be/U1sVq_TBgNY

### Description:

This Telegram bot is designed to run predefined macros, making it a powerful tool for automating tasks. Built with aiogram 3 and FastAPI, it leverages the best of asynchronous Python programming for efficient and scalable bot interactions. The bot's functionality can be extended or customized with various macros according to user needs.

**Technology Stack:**

- **Python 3.10+**: The primary programming language used for bot development.
- **aiogram 3.2**: An efficient framework for Telegram Bot API, facilitating asynchronous programming and offering a rich set of features for bot development.
- **FastAPI**: A high-performance web framework for building APIs, known for its speed and ease of use, serving the webhook endpoint for the bot.
- **APScheduler**: A task scheduler to run macros at predetermined intervals.
- **SQLite**: A simple file-based database used for storing user data and macros.

**Project Structure:**

- **`app.py`**: The main entry point of the bot. It initializes the bot, sets up the webhook, and starts the event loop.
- **`config/`**: Configuration directory containing all necessary tokens, database connection details, and other configurations.
- **`handlers/`**: This directory contains modules for different types of bot command handlers.
- **`states/`**: Contains FSM states for managing different stages of conversation or command execution.
- **`data/`**: Defines database models and structures, typically used for storing and retrieving macro and user data.
- **`keyboards/`**: Contains keyboards for InlineKeyboards, helping to structure interactive bot responses.
- **`requirements.txt`**: Lists all the Python dependencies required for the bot to run.
