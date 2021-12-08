import os
import discord
from dotenv import load_dotenv
from utils import category, help

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

client = discord.Client()

user = category.User()
blog = category.Blog()
help_ = help.Help()

async def send_message(channel, content):
  embed = discord.Embed(description=f"{content}", color=discord.Color.red())
  await channel.send(embed=embed)

@client.event
async def on_ready():
  print(f'{client.user} has connected to discord!')

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  if not message.content.startswith("$"):
    return

  channel = message.channel
  user_message = message.content.lower().split()

  if user_message[0] == "$help":
    if len(user_message) == 1:
      await help_.all_help(channel)
    elif user_message[1] == "user":
      await help_.user_help(channel)
    elif user_message[1] == "blog":
      await help_.blog_help(channel)
    else:
      await help_.command_help(channel, user_message[1])
  
  elif user_message[0] == "$usernotify":
    if len(user_message) < 3:
      await send_message(channel, "Missing arguments!")
    else:
      if user_message[1] == "all":
        await user.notify_all_changes(channel, user_message[2])
      elif user_message[1] == "rating":
        await user.notify_rating_change(channel, user_message[2])
      else:
        await send_message(channel, "Wrong arguments!")
  
  elif user_message[0] == "$userstop":
    if len(user_message) < 3:
      await send_message(channel, "Missing arguments!")
    else:
      if user_message[1] == "all":
        await user.stop_all_changes(channel, user_message[2])
      elif user_message[1] == "rating":
        await user.stop_rating_change(channel, user_message[2])
      else:
        await send_message(channel, "Wrong arguments!")
  
  elif user_message[0] == "$userlist":
    if len(user_message) < 2:
      await send_message(channel, "Missing arguments!")
    else:
      if user_message[1] == "all":
        await user.list_all_changes(channel)
      elif user_message[1] == "rating":
        await user.list_rating_change(channel)
      else:
        await send_message(channel, "Wrong arguments!")
  
  elif user_message[0] == "$blognotify":
    if len(user_message) < 2:
      await send_message(channel, "Missing arguments!")
    else:
      await blog.notify_blog_changes(channel, user_message[1])
  
  elif user_message[0] == "$blogstop":
    if len(user_message) < 2:
      await send_message(channel, "Wrong arguments!")
    else:
      await blog.stop_blog_changes(channel, user_message[1])
  
  elif user_message[0] == "$bloglist":
    await blog.list_blog_changes(channel)

client.run(BOT_TOKEN)
