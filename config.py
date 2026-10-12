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


# ----------- IMAGES-URL ----------- #
SUPPORT_THUMBNAIL_URL = "https://cdn.discordapp.com/attachments/1534607507023069346/1559308964691181678/Festliches_SUPPORT-Logo_mit_Schneefall.png?ex=6ace9b23&is=6acd49a3&hm=966782c303b2587718e428254ce4924bdaad70a8df1377ad43aa94e538472bfe&"
WELCOME_THUMBNAIL_URL = "https://cdn.discordapp.com/attachments/1534607507023069346/1559312111908167790/Winterliches_Willkommen_im_Voxel-Dorf.png?ex=6ace9e12&is=6acd4c92&hm=99c5bf9c7c3a086e708327f5661f7e7db8300e9e1fb3a1c5d61e04ecc959e866&"


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




# Inhalt KI genererriert!
FORBIDDEN_WORDS = [
    # Beleidigungen
    "idiot", "dummkopf", "depp", "trottel", "vollidiot",
    "hurensohn", "hs", "huso", "missgeburt", "opfer",
    "wixxer", "wichser", "arschloch", "arsch", "bastard",
    "spast", "spasti", "mongo", "penner", "schwuchtel",
    "fotze", "fick dich", "fickfehler", "drecksau",
    "scheißkerl", "dreckskerl", "mistkerl", "pisskopf",
    "nutte", 

    # Englische Beleidigungen
    "idiot", "moron", "dumbass", "jackass", "asshole",
    "bastard", "motherfucker", "son of a bitch",
    "fuck you", "fuck off", "piece of shit", "dickhead",
    "dipshit", "shithead", "scumbag", "prick", "twat",

    # Rassistische / diskriminierende Begriffe
    "nigger", "negro", "coon", "kike", "chink",
    "wetback", "spic", "raghead", "tranny",

    # Deutsche vulgäre Ausdrücke
    "scheiße", "scheisse", "scheiß", "scheiss",
    "fick", "ficken", "gefickt", "verfickt",
    "verpiss dich", "leck mich", "leck mich am arsch",
    "halt die fresse", "maul halten", "fotzenkopf",
    "schwanzlutscher", "arschgeburt", "drecksack",

    # Englische vulgäre Ausdrücke
    "fuck", "fucking", "fucked", "shit", "bullshit",
    "bitch", "bitches", "whore", "slut", "cunt",
    "dick", "cock", "pussy", "dick sucker",
    "go to hell", "eat shit",

    # Bedrohungen
    "ich bring dich um", "ich töte dich",
    "i will kill you", "kill yourself", "kys",
    "bring dich um"

    # Sonstige
    "nude","nudes","sex","psy","pssy","ayri","dih",
    "hitler", "hitla", "adolf", "88", "1945", "1933",
    "911","9/11"
]
