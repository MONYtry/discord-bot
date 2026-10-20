# 🤖 Discord Bot

<p align="center">
  A powerful Discord management platform with moderation, support tickets, and a web dashboard.
</p>

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Discord.py](https://img.shields.io/badge/Discord.py-5865F2?style=for-the-badge&logo=discord&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![License](https://img.shields.io/badge/License-FREE-gray?style=for-the-badge)
---

## ✨ Overview

This project contains a **Python-based Discord bot** combined with a **FastAPI backend** and a web-based dashboard.

The platform allows server administrators to manage moderation, support tickets, community features, and guild-specific settings through Discord commands and a browser-based interface.

## 🚀 Features

- 🛡️ **Moderation** — Administrative tools and moderation commands.
- 🤖 **Automoderation** — Automated server management and moderation features.
- 🎫 **Ticket System** — Support tickets and application workflows.
- 👋 **Welcome & Leave** — Member join and leave handling.
- 🎭 **Reaction Roles** — Role assignment through reactions.
- 📋 **Logging** — Configurable server event and moderation logs.
- 📊 **Bot Statistics** — Status information and server statistics.
- 🌐 **Web Dashboard** — Manage server settings through a web interface.
- 🔐 **Discord OAuth2** — Secure Discord-based authentication flow.
- 💾 **Database** — Persistent guild settings and ticket-related data.

## 🏗️ Architecture

```text
Discord Management Platform
│
├── main.py              # Bot entry point and local API server
├── api/
│   ├── main.py           # FastAPI routes and OAuth integration
│   └── database.py       # Database operations
├── cogs/
│   ├── admin              # Administration commands
│   ├── moderation         # Moderation features
│   ├── automoderation     # Automated moderation
│   ├── support            # Support and ticket workflows
│   └── ...                # Additional bot modules
└── website/
    ├── HTML               # Website structure
    ├── CSS                # Styling
    └── JavaScript         # Dashboard and authentication UI
```

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| 🐍 Python | Core application and bot logic |
| 💬 Discord API | Server interaction and commands |
| ⚡ FastAPI | Backend API |
| 🗄️ SQLite | Persistent data storage |
| 🌐 HTML, CSS & JavaScript | Web dashboard and frontend |
| 🔐 Discord OAuth2 | User authentication |

## 📦 Installation

### 1. Clone the repository

```bash
git clone <discord-bot>
cd <discord-bot>
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows**
```bash
.venv\Scripts\activate
```

### 3. Install dependencies

Use the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

Otherwise, it wont work without a bunch of errors 

### 4. Configure environment variables

Create a `.env` file in the project root and configure the credentials required by your bot and web backend.

Example:

```env
DISCORD_TOKEN=your_discord_bot_token
DISCORD_CLIENT_ID=your_discord_client_id
DISCORD_CLIENT_SECRET=your_discord_client_secret
DISCORD_REDIRECT_URI=http://localhost:8000/auth/callback
```

> ⚠️ The variable names and redirect URI must match your actual implementation. Never commit your `.env` file or expose your bot token. (Consider using an .gitignore to prevent problems)

### 5. Start the application

```bash
python main.py
```

The bot and local FastAPI server are started through the main entry point.

> 💡 Check your configuration and project dependencies before launching the application.

## ⚙️ Configuration

The platform supports configurable guild settings, including:

- 🎫 Support and ticket channels
- 📢 Status channels
- 📝 Logging channels
- 🛠️ Ticket options
- 🏠 Guild-specific settings

OAuth credentials, API configuration, and Discord permissions must be configured correctly for all features to work.

## 🔐 Security

- 🔒 Keep bot tokens and OAuth secrets private.
- 🚫 Never commit `.env` files or other sensitive credentials.
- 🛡️ Validate permissions before allowing administrative actions.
- 🌐 Configure OAuth redirect URLs correctly.
- 📁 Exclude local databases and sensitive configuration files from version control when appropriate.

## 🗺️ Roadmap

- [ ] 📊 Expand dashboard statistics
- [ ] 🎨 Improve dashboard UI and user experience
- [ ] 🛡️ Extend moderation configuration
- [ ] 📋 Add more logging options
- [ ] ⚡ Improve API performance and reliability

## 🤝 Contributing

Contributions, bug reports, and feature suggestions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Open a pull request.


<p align="center">
  💜 Built with Python, Discord, FastAPI and alot of Hearth by <a href="https://github.com/Monytry"><b>MONYtry</b></a>
</p>
