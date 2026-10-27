# Discordbot

![Discord](https://img.shields.io/badge/Discord-5865F2?style=flat&logo=discord&logoColor=white) 
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS-563d7c?&style=flat&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)


# Overview
I've spent the last 3 Weeks to learn how to create a Discord bot. 
Only because i am sick of being restricted or having to pay just to use some small features and thats why I share it here!

# Project
This project is based on Python3. It has an Python3 based Backend (Database, API) other then the front end because it is written in Vanilla Web-Languages (HTML, CSS and JS)
For security reasons I'v had to learn OAUTH and I integrated it in this project.
You can take a look at it in /api/main.py

# ℹ️ Built-in Features:
```
- 👋 Welcome-Messages
- ✅ Reactionroles
- 🎫 Ticket-System
- ♨️ Apply-Ticket-System
- 💥 Timeout-Command
- 🍻 Unban-All-Command
- ℹ️ Ban-List-Command
- 🌐 Custom-Embed-Command
- 🧹 Clear-Messages-Command
- 🛡️ Automoderation
- 📝 Clean Logging
- 🔧 Join-roles

```
# ⚙️ Configuration
You can change the settings of the bot through the Frontend.
But you can only do that if you'r the owner of the Server.

For example you could change:
- Welcome Channel
- Join-Roles
- Support-Roles
- Enable / Disable Ticketsystem
- and so much more!


# 🖼️ Showcase

<div align="center">
  <img src="/website/Images/Dashboard1" width="49%" alt="Landing Page">
  <img src="https://via.placeholder.com/900x500?text=Dashboard" width="49%" alt="Dashboard">
  <br><br>
  <img src="https://via.placeholder.com/1200x600?text=Ticket+System" width="80%" alt="Ticket System">
</div>


# 📖Libraries
The Project uses Libraries as:
- ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white) | Database 
- **CHART.JS** | The Graph (Chart) in the Dashboard
- ![Discord](https://img.shields.io/badge/Discord-5865F2?style=flat&logo=discord&logoColor=white)  | The main functions (Discordbot)
- **FASTAPI** | API that gets used across Backend & Frontend

# 📘Techstack

Stack | Usage 
--- | --- |
`FASTAPI` | API
`SQLITE` | Database
`CHART.JS` | Chart in Dashboard
`DISCORD` | Discord Function
`JS` | Frontend
`PYTHON3`  | Backend

> [!NOTE]
> I went with this specific Tech-Stack because i already had some experience with Python3 and Vanilla-Web (HTML, CSS and JS)

# Setup
It isn't complicated to setup the Discordbot and it only takes 3 steps!

⏬ 1.Clone the Repository
```
git clone https://github.com/MONYtry/discord-bot.git
```

🏗️ 2. Create an .env File
```
Create an file (.env) and paste in placeholder variables after that change the Values to your needs!
```
🛜 3. Download the requirements
```
pip install -r requirements.txt
```

🍻 Have fun!
```
🚩 If you run into any bugs consider creating an issue so i can fix them 
```

# 🏗️ Structure
```
├──  website
│   ├── admin
│   ├── dashboard
│   ├── landingPage
│   └── userServer
├──  cogs
│   ├── support.py
│   ├── automoderation.py
│   ├── join.py
│   └── and more..
├──  api
│  ├── database.py
│  ├── main.py
│  └── tracking.py
├──  config.py
├──  main.py
└──  requirements.txt
```

# 👨‍💻 About-me
As I'm writing this I'm 15 yrs old and this is my first time building an project with an Frontend and Backend.
I know some parts of the Code aren't perfect to the last bit, but I think it is good to make mistakes because it is an part of learning and growing.
I did spent 3 Weeks learning all of this (API, SQLLITE3 Databases and so much more) and I'm pretty proud.
If you run into any bugs or you just have an oppinion what to add, i would be happy to help :)


---

<p align="center">
  Made with ❤️ by <a href="https://github.com/MONYtry">MONY</a>
</p>
