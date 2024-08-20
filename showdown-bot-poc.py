import discord
import BingoUtils
import configparser
import argparse
from discord.ext import commands
from discord import app_commands
from ApprovalRequest import ApprovalRequest

# Parse command-line args
parser = argparse.ArgumentParser(
  prog = 'Showdown Bot POC',
  description = 'POC for the UIM Showdown bot'
)
parser.add_argument('--test', action='store_true')
commandLineArgs = parser.parse_args()

# Set up bot object
intents = discord.Intents.default()
intents.message_content = True # Required for the commands extension to work
bot = commands.Bot(command_prefix='/', intents=intents)

# Register callback for all errors thrown out of command methods
@bot.tree.error
async def handleCommandErrors(ctx, error):
  await BingoUtils.handleCommandError(bot, ctx, error)

# Register commands
@bot.tree.command(name='submit_monster_killcount', description='Submit a monster killcount for the bingo!')
@app_commands.autocomplete(monster=BingoUtils.monster_autocomplete)
async def test_submit_kc(ctx: discord.Interaction, screenshot: discord.Attachment, monster: str, kc: int):
  if(kc < 0):
    raise BingoUtils.BingoUserError('KC cannot be negative')
  if(monster not in BingoUtils.monsters):
    raise BingoUtils.BingoUserError('Invalid monster name (make sure to click on the autocomplete option)')
  if(kc == 999):
    x = 1 / 0 # To demo an unexpected error
  request = ApprovalRequest(ctx, f'{kc} KC of {monster}')
  await BingoUtils.requestApproval(bot, request)
  responseText = 'Request received:\n'
  responseText += str(request)
  await ctx.response.send_message(responseText)

@bot.event
async def on_ready():
  print(f'Logged in as {bot.user.name}')
  await bot.tree.sync() # This sets up the app commands in the Discord server based on what we register here
  print(f'Command tree synced!')

bot.run(BingoUtils.token)