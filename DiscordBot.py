import discord
from discord.ext import commands
import requests
TOKEN = "OTk0NjU4ODY5MDUxNjU0MTQ3.GorFHv.AAsoHsCaoMINP7uVSFoAd7I8M8AnSCNq9A7u2I"
intents = discord.Intents.default()
intents.typing = True
intents.presences = True
intents.message_content = True
intents.guild_messages = True
bot = commands.Bot(command_prefix='!', intents=intents)
def fetch_user_data(user_id):
    response = requests.get(f'https://users.roblox.com/v1/users/{user_id}')
    if response.status_code != 200:
        balls = f"No used found with ID '{user_id}'"
        return balls
    user_data = response.json()
    username = user_data['name']
    bio = user_data.get('description', '')
    is_banned = user_data.get('isBanned', False)
    is_verified = user_data.get('hasVerifiedBadge', False)
    display_name = user_data.get('displayName', '')
    created = user_data['created']
    external_app_display_name = user_data.get('externalAppDisplayName', '')
    data = f"```Username: {username}\nDisplay Name: {display_name}\nBio: {bio}\nBanned: {is_banned}\nVerified Badge: {is_verified}\nCreated: {created}\nExternal App Display Name: {external_app_display_name}```"
    return data
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    await bot.change_presence(activity=discord.Game(name='with my balls'))
@bot.command(name="lid", description="Fetch roblox user info from the user's ID")
async def lid(ctx: commands.Context, *, user_id: str):
    data = fetch_user_data(user_id)
    if data:
        await ctx.send(data)
    else:
        await ctx.send("User not found")
bot.run(TOKEN)
