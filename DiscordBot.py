import discord
from discord.ext import commands
import requests

TOKEN = "token"
intents = discord.Intents.default()
intents.typing = True
intents.presences = True
intents.message_content = True
intents.guild_messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

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
    else:
        await ctx.send("User not found")

@bot.command(name="lun", description="Fetch Roblox user info from the username")
async def lun(ctx: commands.Context, *, username: str):
    await ctx.send("This command does not work right now")

@bot.command(name="echo", description="Repeats what the user said")
async def echo(ctx: commands.Context, *, message: str):
    await ctx.send(message)
    await ctx.send('Sucessfully echoed!')

@bot.command(name="announce", description="announcement go brr")
async def announce(ctx: commands.Context, *, message: str):
    await ctx.send(message+'\n||@everyone||')

@bot.command(name="rhelp", description="Roblox help")
async def rhelp(ctx: commands.Context):
    await ctx.send('```Commands:\n    !lid - Lookup Roblox users by name\n    !lun - In progress\n    !rhelp - Displays this message\n    !echo - Echos the users message.\n    !announce - Announces what you want to say\n    !rpurge - supposed to purge channels, but it sometimes breaks or gets rate limited\nMore commands coming soon!```')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Please enter a valid command or run `!help`.")

@bot.command(name="rpurge", description="Delete all messages in the current channel")
async def rpurge(ctx: commands.Context):
    await ctx.channel.purge(limit=None)
    await ctx.send(f"Purged {ctx.command.clean_params['ctx'].message_count} messages")

bot.run(TOKEN)
