import os

topics = [
    "Lesbian",
    "Sxe",
    "Sxy",
    "Nude",
    "Masturbation",
    "Black",
    "Dance",
    "Extreme",
    "CCTV",
    "Cum",
    "Gay",
    "Voyeur",
    "Arab Sxe",
    "دياثة",
    "Kids with man",
    "kids with women",
    "kids",
    "kids nude"
]

base_dir = "Telegram_Topics"

os.makedirs(base_dir, exist_ok=True)

for topic in topics:
    path = os.path.join(base_dir, topic)
    os.makedirs(path, exist_ok=True)
    print(f"Created: {path}")

    print("You succuded")