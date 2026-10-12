# Just replace the values
# Otherwise your Bot wont work well 

# ----------- CHANNELS ----------- #
SERVER_ID = 1557487186016993363
WELCOME_CHANNEL_ID = 1557488303736094923
BOT_STATUS_CHANNEL_ID = 1558243145836269568
STATUS_CHANNEL_ID = 1558243145836269568
BAN_CHANNEL_ID = 1557488286161834034
SUPPORT_CHANNEL_ID = 1557488329279144096

# LOGGING - CHANNELS
TIMEOUT_LOG_CHANNEL = 1557488290511196211
MESSAGE_LOG_CHANNEL = 1557488278570270780
JOIN_LEAVE_LOG_CHANNEL = 1557488292193370213
SUPPORT_CHANNEL_LOG_ID = 1557488280512106536

# ----------- MESSAGES ----------- #
NO_RIGHTS_MESSAGE = "Du hast dazu keine Berechtigung!"
REMOVED_REACTION_ROLE_MESSAGE = "Du hattest die Rolle {role} bereits (Sie wurde entfernt!)"
ADDED_REACTION_ROLE_MESSAGE = "Du hattest die Rolle {role} erhalten"

# JOIN LEAVE LOG MESSSAGES
JOIN_TITEL_LOG_MESSAGE = "Member joined"
LEAVE_TITEL_LOG_MESSAGE = "Member leaved"
JOIN_LOG_MESSAGE = "{member} just joined the Discord"
LEAVE_LOG_MESSAGE = "{member} just leaved the Discord"

# WELCOME MESSAGE
WELCOME_MESSAGE = (
                "Hey {member}, welcome to our community💖\n\n"
                "We're happy to have you here! 🥳\n\n"
                "📜 **Before you get started, please read the server rules carefully.**\n"
                "They help keep our community friendly, safe, and fun for everyone.\n\n"
                "💬 Feel free to chat with other members, join the conversations, "
                "and have a great time!\n\n"
                "✨ **Make yourself at home and enjoy your stay!**"
                )
WELCOME_FOOTER = "Developer Academy Bot • Made with Love ❤️ • #{member_count}"

# SUPPORT MESSAGE
SUPPORT_EMBED_MESSAGE = ("Hey {member},\n" 
            "unser Team wird sich zeitnah melden, bitte habe Geduld!\n"
            "Wir wünschen dir eine angenehme Zeit und weiterhin viel Spaß!")
SUPPORT_EMBED_TITEL = "Hilfe ist unterwegs!"

TICKET_EMBED_TITEL =  "GETTING HELP - TUTORIAL"
TICKET_EMBED_MESSAGE =  (
            "Need help? Follow these simple steps!\n\n"
            "1. **Select a Category** – Choose the category that best describes your issue.\n"
            "2. **Create a Ticket** – A private ticket channel will be created for you.\n"
            "3. **Describe Your Issue** – Explain your problem in detail.\n"
            "4. **Wait for Support** – Our team will respond as soon as possible.\n"
            "5. **Close Your Ticket** – Click the 🔒 button when your issue is resolved.\n\n"
            "⚠️ Please do not create multiple tickets for the same issue. Thank you!")

# ----------- ROLE-IDS ----------- #
EMBED_ALLOWED_ROLE_IDS = [
    1558241441929760889  # Owner
]

TIMEOUT_ALLOWED_ROLE_IDS = [
    1558241441929760889  # Owner
]

SEND_DROPDOWN_ROLE_IDS = [
    1558241441929760889 # Owner
]

REACTION_ROLES_IDS = {
    "html": 1557488216351969350,
    "css": 1557488220948799488,
    "kotlin": 1557488209481433118,
    "lua": 1557488210437996584,
    "rust": 1557488211318673639,
    "go": 1557488212488884255,
    "c++": 1557488214103560292,
    "c#": 1557488215211114516,
    "react": 1557488221871546481,
    "node.js": 1557488223389753385
}

# Dictionary
REACTION_ROLE_OPTIONS = {
    "html": {"label": "HTML", "emoji": "🌐"},
    "css": {"label": "CSS", "emoji": "🎨"},
    "js": {"label": "JavaScript", "emoji": "💛"},
    "kotlin": {"label": "Kotlin", "emoji": "🟣"},
    "lua": {"label": "Lua", "emoji": "🌙"},
    "rust": {"label": "Rust", "emoji": "🦀"},
    "go": {"label": "Go", "emoji": "🐹"},
    "c++": {"label": "C++", "emoji": "⚙️"},
    "c#": {"label": "C#", "emoji": "💜"},
    "react": {"label": "React", "emoji": "⚛️"},
    "node.js": {"label": "Node.js", "emoji": "💚"},
}


# Dictionary
SUPPORT_CATEGORIES_OPTIONS = {
    "bug": {"label": "BUG", "emoji": "🌐"},
    "help": {"label": "HELP", "emoji": "🎨"},
    "other": {"label": "OTHER", "emoji": "💛"}
}




