import discord
from discord.ext import commands
import requests
import concurrent.futures
import json
import random
import string
from typing import Dict

TOKEN = "ur-tbot-token"
intents = discord.Intents()
intents.dm_messages = True
intents.bans = True
intents.emojis = True
intents.typing = True
intents.presences = True
intents.message_content = True
intents.guild_messages = True

bot = commands.Bot(command_prefix='!', intents=intents)
url = "https://auth.roblox.com/v1/usernames/validate"
params = {"context": "Signup", "Birthday": "1931-01-01T06:00:00.000Z"}
def generate_random_username(length: int = random.randint(5, 20)) -> str:
    """
    This function generates a random string of the specified length.
    """
    return "".join(random.choices(string.ascii_letters, k=length))

def check_username_availability(username: str) -> Dict[str, str]:
    """
    This function checks the availability of a given name on the specified URL.
    """
    params["username"] = username
    response = requests.get(url, params=params)
    rData = json.loads(response.text)
    return rData

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    await bot.change_presence(activity=discord.Game(name="Checking Roblox usernames"))

@bot.command(name="RNG", description="Check the availability of Roblox usernames")
async def RNG(ctx: commands.Context, count: int = 100):
    async with ctx.typing():
        available_usernames = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_name = {
                executor.submit(check_username_availability, generate_random_username()): generate_random_username()
                for _ in range(count)
            }
            for future in concurrent.futures.as_completed(future_to_name):
                name = future_to_name[future]
                try:
                    data = future.result()
                    if not data['message'] or not data['code']:
                        print(f"[{name}] No message or code. Can't tell if claimed or not.")
                    if data["code"] != 0:
                        print(f"[{name}] {data['message']}")
                    else:
                        available_usernames.append(name)
                except (requests.RequestException, requests.ConnectionError,
                        ConnectionResetError, ConnectionError,
                        ConnectionRefusedError, ConnectionAbortedError):
                    continue
    if available_usernames:
        await ctx.send(f"Available usernames:\n ```{', '.join(available_usernames)}```")
    else:
        await ctx.send("No available usernames found.")

def fetch_user_data(user_id):
    response = requests.get(f'https://users.roblox.com/v1/users/{user_id}')
    if response.status_code != 200:
        return None
    user_data = response.json()
    username = user_data['name']
    bio = user_data.get('description', '')
    is_banned = user_data.get('isBanned', False)
    is_verified = user_data.get('hasVerifiedBadge', False)
    display_name = user_data.get('displayName', '')
    created = user_data['created']
    external_app_display_name = user_data.get('externalAppDisplayName', '')
    data = f"```Username: {username}\nDisplay Name: {display_name}\nBio: {bio}\nBanned: {is_banned}\nVerified Badge: {is_verified}\nCreated: {created}\nExternal App Display Name: {external_app_display_name}\nUserID: {user_id}```"
    return data


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    await bot.change_presence(activity=discord.Game(name='with my balls'))


@bot.command(name="lid", description="Fetch Roblox user info from the user's ID")
async def lid(ctx: commands.Context, *, user_id: str):
    data = fetch_user_data(user_id)
    if data:
        await ctx.send(data)
        await ctx.message.delete()
    else:
        await ctx.send("User not found")
        await ctx.message.delete()


@bot.command(name="checkname", description="Check if a Roblox username is available")
async def checkname(ctx: commands.Context, *, username: str):
    validate_url = f'https://auth.roblox.com/v1/usernames/validate?username={username}'
    response = requests.get(validate_url)
    
    if response.status_code == 200 and response.json()["message"] == "Username is valid":
        check_user_url = f'https://api.roblox.com/users/get-by-username?username={username}'
        user_response = requests.get(check_user_url)
        
        if user_response.status_code == 200:
            user_data = user_response.json()
            user_id = user_data["Id"]
            await ctx.send(f'Username "{username}" is available!')
            await ctx.message.delete()
        else:
            await ctx.send(f'An error occurred while retrieving user ID for username "{username}".')
    else:
        await ctx.send(f'Username "{username}" is taken. User ID: {user_id}')
        await ctx.message.delete()


@bot.command(name="recho", description="Repeats what the user said")
async def recho(ctx: commands.Context, *, message: str):
    await ctx.send(message)
    await ctx.message.delete()


@bot.command(name="announce", description="announcement go brr")
async def announce(ctx: commands.Context, *, message: str):
    await ctx.send(message + '\n||@everyone||')
    await ctx.message.delete()


@bot.command(name="rhelp", description="Roblox help")
async def rhelp(ctx: commands.Context):
    await ctx.send('```Commands:\n    !lid - Lookup Roblox users by ID\n    !lun - In progress\n    !rhelp - Displays this message\n    !recho - Echos the users message.\n    !announce - Announces what you want to say\n    !fuckyoumouwy - trolls mouwy\n    !rpurge - supposed to purge channels, but it sometimes breaks or gets rate limited\nMore commands coming soon!```')
    await ctx.message.delete()


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Please enter a valid command or run `!help`.")
        await ctx.message.delete()


@bot.command(name="rpurge", description="Delete all messages in the current channel")
async def rpurge(ctx: commands.Context):
    await ctx.channel.purge(limit=None)
    await ctx.send(f"Purged {ctx.command.clean_params['ctx'].message_count} messages")
    await ctx.message.delete()


@bot.command(name="fuckyoumouwy", description="lmaoo")
async def fuckyoumouwy(ctx: commands.Context):
    while True:
        await ctx.send("fuck you <@822158222118223922>")

bot.run(TOKEN)
