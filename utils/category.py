import discord
from discord.ext import tasks
from utils import codeforces_api

cf = codeforces_api.CodeforcesAPI()

class User:
  def __init__(self):
    self.rating_change_dict = {}
    self.all_changes_dict = {}
    self.user_link = "https://codeforces.com/profile/"

  async def send_message(self, channel, content, title=""):
    embed = discord.Embed(
      title=title,
      description=content, 
      color=discord.Color.blue())
    await channel.send(embed=embed)
  
  async def notify_rating_change(self, channel, username):
    if username not in self.rating_change_dict:
      response = await cf.user_info(username)

      if not response[0]:
        print(f"Error : {response[1]}")
        await self.send_message(channel, "Some error occured!!!")
      else:
        rating = response[1]['rating']

        @tasks.loop(minutes=10)
        async def is_rating_changed():
          print(f"{username} - {is_rating_changed.current_loop}")
          response = await cf.user_info(username)
          if not response[0]:
            print(f"Error : {response[1]}")
          else:
            nonlocal rating
            if response[1]['rating'] != rating:
              title = f"Rating change for user {username}"
              message = f"[{username}]({self.user_link}{username}): {rating} ― {'+' if rating > response[1]['rating'] else '-'} ⟶ {response[1]['rating']}"
              rating = response[1]['rating']
              await self.send_message(channel, message, title)

        @is_rating_changed.after_loop
        async def after_complete():
          print(f"done user {username}.")

        title = f"Started notifications(rating change) for user {username}"
        message = f"[{username}]({self.user_link}{username})\n - Rating: {rating}"
        await self.send_message(channel, message, title)
        self.rating_change_dict[username] = is_rating_changed.start()
    else:
      await self.send_message(channel, f"Notification for user [{username}]({self.user_link}{username}) is already active.")

  async def notify_all_changes(self, channel, username):
    if username not in self.all_changes_dict:
      response = await cf.user_info(username)

      if not response[0]:
        print(f"Error : {response[1]}")
        await self.send_message(channel, "Some error occured!!!")
      else:
        rating = response[1]['rating']
        contribution = response[1]['contribution']
        friend_count = response[1]['friendOfCount']

        @tasks.loop(minutes=10)
        async def any_changes():
          print(f"{username} - {any_changes.current_loop}")
          response = await cf.user_info(username)
          if not response[0]:
            print(f"Error : {response[1]}")
          else:
            nonlocal rating
            nonlocal contribution
            nonlocal friend_count
            if response[1]['rating'] != rating:
              title = f"Rating change for user {username}"
              change = f"{'-' if rating > response[1]['rating'] else '+'}{abs(rating-response[1]['rating'])}"
              message = f"[{username}]({self.user_link}{username}): {rating} ― **{change}** ⟶ {response[1]['rating']}"
              rating = response[1]['rating']
              await self.send_message(channel, message, title)
            if response[1]['contribution'] != contribution:
              title = f"Contribution change for user {username}"
              change = f"{'-' if contribution > response[1]['contribution'] else '+'}{abs(contribution-response[1]['contribution'])}"
              message = f"[{username}]({self.user_link}{username}): {contribution} ― **{change}** ⟶ {response[1]['contribution']}"
              contribution = response[1]['contribution']
              await self.send_message(channel, message, title)
            if response[1]['friendOfCount'] != friend_count:
              title = f"Friend-count change for user {username}"
              change = f"{'-' if friend_count > response[1]['friendOfCount'] else '+'}{abs(friend_count-response[1]['friendOfCount'])}"
              message = f"[{username}]({self.user_link}{username}): {friend_count} ― **{change}** ⟶ {response[1]['friendOfCount']}"
              friend_count = response[1]['friendOfCount']
              await self.send_message(channel, message, title)

        @any_changes.after_loop
        async def after_complete():
          print(f"done user {username}")

        title = f"Started notifications(all) for user {username}"
        message = f"[{username}]({self.user_link}{username})\n - Rating: {rating}\n - Contribution: {contribution}\n - Friend-count: {friend_count}"
        await self.send_message(channel, message, title)
        self.all_changes_dict[username] = any_changes.start()
    else:
      await self.send_message(channel, f"Notification for user [{username}]({self.user_link}{username}) is already active.")

  async def stop_rating_change(self, channel, username):
    if username in self.rating_change_dict:
      if self.rating_change_dict[username].cancel():
        self.rating_change_dict.pop(username)
        await self.send_message(channel, f"Stopped notification(rating change) for user [{username}]({self.user_link}{username}).")
      else:
        await self.send_message(channel, "Something is wrong.")
    else:
      await self.send_message(channel, f"User **{username}** is not present.")

  async def stop_all_changes(self, channel, username):
    if username in self.all_changes_dict:
      if self.all_changes_dict[username].cancel():
        self.all_changes_dict.pop(username)
        await self.send_message(channel, f"Stopped notifications(all) for user [{username}]({self.user_link}{username}).")
      else:
        await self.send_message(channel, "Something is wrong.")
    else:
      await self.send_message(channel, f"User **{username}** is not present.")

  async def list_rating_change(self, channel):
    if len(self.rating_change_dict) != 0:
      title = "Active notification(rating change) for user :"
      message = ""
      for username in self.rating_change_dict:
        message += f"\n - [{username}]({self.user_link}{username})"
    else:
      title = ""
      message = f"There is no active notification(rating change)."
    await self.send_message(channel, message, title)

  async def list_all_changes(self, channel):
    if len(self.all_changes_dict) != 0:
      title = "Active notifications(all) for user :"
      message = ""
      for username in self.all_changes_dict:
        message += f"\n - [{username}]({self.user_link}{username})"
    else:
      title = ""
      message = f"There is no active notifications(all)."
    await self.send_message(channel, message, title)

class Blog:
  def __init__(self):
    self.blog_changes_dict = {}
    self.blog_link = "https://codeforces.com/blog/entry/"

  async def send_message(self, channel, content, title=""):
    embed = discord.Embed(
      title=title,
      description=content,
      color=discord.Color.purple())
    await channel.send(embed=embed) 

  async def notify_blog_changes(self, channel, blog_id):
    if blog_id not in self.blog_changes_dict:
      response = await cf.blog_info(blog_id)
      if not response[0]:
        print(f"Error : {response[1]}")
        await self.send_message(channel, "Some error occured!!!")
      else:
        blog = [comment['id'] for comment in response[1]]

        @tasks.loop(minutes=10)
        async def any_changes():
          print(f"{blog_id} - {any_changes.current_loop}")
          response = await cf.blog_info(blog_id)

          if not response[0]:
            print(f"Error : {response[1]}")
          else:
            if len(response[1]) != len(blog):
              for comment in response[1]:
                if comment['id'] not in blog:
                  blog.append(comment['id'])
                  message = f"There is [new comment]({self.blog_link}{blog_id}?#comment-{comment['id']}) in blog [{blog_id}]({self.blog_link}{blog_id})."
                  await self.send_message(channel, message)

        @any_changes.after_loop
        async def after_complete():
          print(f"done blog {blog_id}.")

        await self.send_message(channel, f"Started notification for blog [{blog_id}]({self.blog_link}{blog_id}).")
        self.blog_changes_dict[blog_id] = any_changes.start()
    else:
      await self.send_message(channel, f"Notification for blog [{blog_id}]({self.blog_link}) is already active.")

  async def stop_blog_changes(self, channel, blog_id):
    if blog_id in self.blog_changes_dict:
      if self.blog_changes_dict[blog_id].cancel():
        self.blog_changes_dict.pop(blog_id)
        await self.send_message(channel, f"Stopped notification for blog [{blog_id}]({self.blog_link}{blog_id}).")
      else:
        await self.send_message(channel, "Something is wrong.")

  async def list_blog_changes(self, channel):
    if len(self.blog_changes_dict) != 0:
      title = "Active notifications for blog :"
      message = ""
      for blog_id in self.blog_changes_dict:
        message += f"\n - [{blog_id}]({self.blog_link}{blog_id})"
    else:
      title = ""
      message = "There is no active notification."
    await self.send_message(channel, message, title)