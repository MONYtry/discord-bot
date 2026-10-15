# Just replace the values
# Otherwise your Bot wont work well 

# ----------- CHANNELS ----------- #
SERVER_ID = 1503032377822417016
WELCOME_CHANNEL_ID = 1557488303736094923
BOT_STATUS_CHANNEL_ID = 1558243145836269568
STATUS_CHANNEL_ID = 1558243145836269568
BAN_CHANNEL_ID = 1557488286161834034
SUPPORT_CHANNEL_ID = 1557488329279144096
APPLY_CHANNEL_ID = 1559641553373372527

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

# BOT MESSAGES
BOT_HAS_NO_RIGHTS = "Bot hat dazu keine Rechte!"

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

TICKET_PREWVIEW_EMBED_TITEL = "HOW TO APPLY - TUTORIAL"

TICKET_PREVIEW_MESSAGE = (
    "Want to join our team? 🚀 Follow these steps!\n\n"
    "1. **Choose a Category** – Select the team you want to join.\n"
    "2. **Fill Out the Form** – Answer all questions honestly.\n"
    "3. **Submit Your Application** – A private ticket will be created.\n"
    "4. **Wait for a Response** – Our team will review your application.\n"
    "5. **Be Patient** – Please avoid duplicate applications.\n\n"
    "❤️ Good luck with your application!"
)
TICKET_EMBED_DESCRIPTION = (
                        "Hey {member},\n"
                        "vielen Dank für deine Bewerbung, wir bitten um Gedult,\n"
                        "unser Team wird sich Zeitnah melden!")

SUPPORT_PREVIEW_EMBED_TITEL =  "GETTING HELP - TUTORIAL"
SUPPORT_PREVIEW_EMBED_MESSAGE =  (
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

APPLY_ALLOWED_ROLE_IDS = [
    1558241441929760889,  # Owner
    1559679252503470160
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
    "bug": {
        "label": "BUG", 
        "emoji": "🌐"
    },
    
    "help": {
        "label": "HELP", 
        "emoji": "🎨"
    },
    
    "other": {
        "label": "OTHER", 
        "emoji": "💛"
    }
}

APPLY_CATEGORIES_OPTIONS = {
    "developer": {
        "label": "DEVELOPER",
        "emoji": "🧑‍💻"
    },
    
    "supporter": {
            "label": "SUPPORTER",
            "emoji": "📨"
    },

    "builder": {
        "label": "BUILDER",
        "emoji": "⛏️"
    },
    
    "designer": {
        "label": "DESIGNER",
        "emoji": "🧊"
    },
    
    "creator": {
        "label": "CREATOR",
        "emoji": "🎥"
    },
    
    "content": {
        "label": "CONTENT",
        "emoji": "💡"
    }
}


TRUSTED_URL = [
    "youtube.com"
    ]
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


APPLY_QUESTIONS = {
    "developer": [
        ("Name & Alter", "Wie heißt du und wie alt bist du?"),
        ("Stärken & Schwächen", "Was sind deine Stärken und Schwächen?"),
        ("Programmiererfahrung", "Welche Sprachen nutzt du?"),
        ("Projekte", "An welchen Projekten hast du gearbeitet?"),
        ("Referenzen", "GitHub oder andere Projekte?")
    ],

    "supporter": [
            ("Name & Alter", "Wie heißt du und wie alt bist du?"),
            ("Stärken & Schwächen", "Was sind deine Stärken und Schwächen?"),
            ("Verhalten", "Wie verhältst du dich bei Fehlverhalten?"),
            ("Erfahrung", "Hast du bereits Erfahrungen als Supporter?")
        ],

    "content": [
            ("Name & Alter", "Wie heißt du und wie alt bist du?"),
            ("Stärken & Schwächen", "Was sind deine Stärken und Schwächen?"),
            ("Features", "Feature Ideen..."),
            ("Wieso du", "Wieso sollten wir uns für dich Entscheiden?")
        ],

    "builder": [
        ("Name & Alter", "Wie heißt du und wie alt bist du?"),
        ("Stärken & Schwächen", "Was sind deine Stärken und Schwächen?"),
        ("Referenzen", "Bilder, Screenshots oder Maps?")
    ],

    "creator": [
        ("Name & Alter", "Wie heißt du und wie alt bist du?"),
        ("Stärken & Schwächen", "Was sind deine Stärken und Schwächen?"),
        ("Plattform", "Welche Plattform nutzt du?"),
        ("Aktivität", "Wie aktiv bist du?"),
        ("Sonstige Informationen", "Was sollten wir noch wissen?")
    ]
}