# stayUp

A Discord bot designed to manage URLs associated with server users. It includes commands to add, remove, and list URLs, along with an automated task that checks the status of each URL every hour.

## Features

The bot provides three main commands:

### `/addurl`

**Description:**  
Registers a new URL associated with your user in the database. This is the first command you must use to be tracked by the bot.

**Usage:**  
```
/addurl url:<your_url>
```

**Example:**  
```
/addurl url:https://mywebsite.com/status
```

---

### `/removeurl`

**Description:**  
Removes your previously registered URL from the database.

**Usage:**  
```
/removeurl
```

---

### `/statusserv`

**Description:**  
Displays a list of all registered URLs along with their current status.

**Usage:**  
```
/statusserv
```

---

## Scheduled Task

The bot runs a scheduled task **every hour** that checks and updates the status of all stored URLs. This ensures that the information displayed with `/statusserv` is up-to-date.

---

## Database Structure

The bot uses two tables in its database:

### `subscriptions`

Stores the relationship between Discord users and the channel/message they are monitoring.

| Field       | Type       | Description             |
|-------------|------------|-------------------------|
| `id`        | bigint     | Primary key             |
| `channel_id`| bigint     | Discord channel ID      |
| `message_id`| bigint     | Discord message ID      |
| `userId`    | bigint     | Discord user ID         |

---

### `urls`

Stores URLs associated with a given server.

| Field      | Type        | Description                 |
|------------|-------------|-----------------------------|
| `id`       | int         | Primary key (auto increment)|
| `serverId` | bigint      | Discord server ID           |
| `url`      | varchar(100)| Monitored URL               |

---

## Requirements

- Node.js or Python (depending on the language used)
- Discord bot token
- A database (e.g. SQLite, PostgreSQL)

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/discord-url-manager-bot.git
cd discord-url-manager-bot
```

2. Install the dependencies:
```bash
npm install
# or
pip install -r requirements.txt
```

3. Create a configuration file with your bot token and database settings.

4. Run the bot:
```bash
npm start
# or
python main.py
```

---

## License

This project is licensed under the [MIT License](LICENSE).
