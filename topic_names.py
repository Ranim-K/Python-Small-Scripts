from telethon.sync import TelegramClient
from telethon.tl.types import Channel, Chat

# Your API credentials
api_id = 29949213
api_hash = "cd78d1e37a6666756a5483ec22f6a84a"

client = TelegramClient('session_name', api_id, api_hash)
client.start()

# Step 1: List all groups you are in
dialogs = client.get_dialogs()
groups = []

print("Your groups:")
for i, d in enumerate(dialogs):
    if isinstance(d.entity, (Channel, Chat)) and d.is_group:
        print(f"{i}: {d.name}")
        groups.append(d.entity)

# Step 2: Pick a group by number
index = int(input("Enter the number of the group you want to fetch messages from: "))
group = groups[index]

# Step 3: Fetch and print recent messages (up to 100)
print(f"\nLast 100 messages in '{group.title if hasattr(group, 'title') else group.name}':")
for msg in client.iter_messages(group, limit=100):
    print(f"- {msg.text}")
