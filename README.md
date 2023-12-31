# Telegram Bot

https://github.com/Gasyok/final_project.git

#### Video Demo: https://youtu.be/U1sVq_TBgNY

### Description:

This Telegram bot is an innovative solution designed to streamline and automate tasks by executing predefined macros. As a versatile tool, it finds utility in various domains, enhancing productivity and interaction. Leveraging the asynchronous capabilities of aiogram 3 and the robustness of FastAPI, this bot stands out for its efficiency and scalability, catering to the modern needs of automation and bot interaction.

**Purpose:**
The bot's primary purpose is to provide users with a seamless interface to automate repetitive tasks, schedule activities, and manage workflows through Telegram. Whether it's sending out reminders, compiling reports, or even interacting with other APIs, this bot is equipped to handle a multitude of tasks, making it an invaluable asset for personal productivity or organizational management.

**Features:**

- **Macro Execution**: Users can define, execute, and manage custom macros, allowing for tailored automation solutions.
- **Scheduling**: Integrate time-based task execution, enabling users to run tasks at specific times or intervals.
- **Security**: Implementing memory and time limitations.

**Technology Stack:**

- **Python 3.10+**: A high-level programming language known for its readability and broad ecosystem.
- **aiogram 3.2**: A modern Telegram Bot API framework, utilizing Python’s asyncio for concurrent operations, making the bot highly responsive.
- **FastAPI**: Known for its performance and ease of use, FastAPI is a modern web framework that allows us to expose a webhook endpoint securely for Telegram to communicate with the bot.
- **APScheduler**: This tool is used for scheduling jobs, making it possible to run macros at specific times or intervals.
- **SQLite**: Provides a lightweight database solution for storing user data, macro configurations, and other relevant information.

**Project Structure:**

- **`app.py`**: The central script where the bot instance is created, webhook is set up, and the application starts listening for incoming updates.
- **`config/`**: Contains configuration files and environment variables crucial for the bot's operation, ensuring modularity and ease of maintenance.
- **`handlers/`**: Modules within this directory define how the bot reacts to various commands and messages, structuring the interaction flow.
- **`states/`**: Manages different stages of conversation or command execution, providing a way to maintain context and manage complex user interactions.
- **`data/`**: Responsible for data handling, including storing and retrieving macro and user data, leveraging SQLite for database interactions.
- **`keyboards/`**: Defines the structure and layout of inline keyboards, enhancing user interaction with custom buttons and commands.
- **`requirements.txt`**: A comprehensive list detailing every package and dependency needed to run the bot, ensuring quick and consistent setup across environments.

### Getting Started

`python3 -m venv venv`
`source venv/bin/activate`
`pip install -r requirements.txt`

### Usage

`python app.py`

### License

MIT License
