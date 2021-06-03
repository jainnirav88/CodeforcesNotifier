async def send_message(channel, content):
  await channel.send(f"```{content}```")

class Help:
  def __init__(self):
    pass

  async def all_help(self, channel):
    response = "CodeforcesNotifier\n\nUser:\n  usernotify Start [rating/contribution/friends] notification for user\n  userstop   Stop [rating/contribution/friends] notification for user\n  userlist   List the users whose notification is on\nBlog:\n  blognotify Start notification for given blog id\n  blogstop   Stop notification for given blog id\n  bloglist   List the blog id whose notification is on\nNo Category:\n  help       Shows this message\n\nType $help command for more info on a command.\nYou can also type $help category for more info on a category."
    await send_message(channel, response)

  async def user_help(self, channel):
    response = "Commands:\n  usernotify   Start [rating/contribution/friends] notification for user\n  userstop     Stop [rating/contribution/friends] notification for user\n  userlist     List the users whose notification is on\n\nUsage Ex:\n  $usernotify [rating/all] [username]\n  $userstop [rating/all] [username]\n  $userlist [rating/all]\n\n  - all: for rating, contribution and friends\n  - rating: only for rating"
    await send_message(channel, response)

  async def blog_help(self, channel):
    response = "Commands:\n  blognotify   Start notification for blog\n  blogstop     Stop notification for blog\n  bloglist     List the blogs whose notification is on\n\nUsage Ex:\n  $blognotify [blog id]\n  $blogstop [blog id]\n  $bloglist"
    await send_message(channel, response)

  async def command_help(self, channel, command):
    if command == "usernotify":
      response = "$usernotify [rating/all] [username]\n\nStart notification for user.\nrating - Notification for rating changes\nall - Notification for rating, friends, contribution changes"
      await send_message(channel, response)
    elif command == "userstop":
      response = "$userstop [rating/all] [username]\n\nStop notification for user.\nrating - Notification for rating changes\nall - Notification for rating, friends, contribution changes"
      await send_message(channel, response)
    elif command == "userlist":
      response = "$userlist [rating/all]\n\nList all username whose notifcation is on.\nrating - Notification for rating changes\nall - Notification for rating, friends, contribution changes"
      await send_message(channel, response)
    elif command == "blognotify":
      response = "$blognotify [blog id]\n\nStart notification for given blog id."
      await send_message(channel, response)
    elif command == "blogstop":
      response = "$blogstop [blog id]\n\nStop notification for given blog id."
      await send_message(channel, response)
    elif command == "bloglist":
      response = "$bloglist [blog id]\n\nList the blog id whose notification is on."
      await send_message(channel, response)
    else:
      await send_message(channel, "Wrong command")

""" 

CodeforcesNotifier
\n
\nUser:
\n  usernotify Start [rating/contribution/friends] notification for user
\n  userstop   Stop [rating/contribution/friends] notification for user
\n  userlist   List the users whose notification is on
\nBlog:
\n  blognotify Start notification for given blog id
\n  blogstop   Stop notification for given blog id
\n  bloglist   List the blog id whose notification is on
\nNo Category:
\n  help       Shows this message
\n
\nType $help command for more info on a command.
\nYou can also type $help category for more info on a category.

**********************************************************************

Catagory User

Commands:
\n  usernotify   Start [rating/contribution/friends] notification for user
\n  userstop     Stop [rating/contribution/friends] notification for user
\n  userlist     List the users whose notification is on
\n
\nUsage Ex:
\n  $usernotify [rating/all] [username]
\n  $userstop [rating/all] [username]
\n  $userlist [rating/all]
\n
\n  - all: for rating, contribution and friends
\n  - rating: only for rating

**********************************************************************

Category Blog:

Commands:
\n  blognotify   Start notification for blog
\n  blogstop     Stop notification for blog
\n  bloglist     List the blogs whose notification is on
\n
\nUsage Ex:
\n  $blognotify [blog id]
\n  $blogstop [blog id]
\n  $bloglist

**********************************************************************

$usernotify [rating/all] [username]
\n
\nStart notification for user.
\nrating - Notification for rating changes
\nall - Notification for rating, friends, contribution changes

$userstop [rating/all] [username]
\n
\nStop notification for user.
\nrating - Notification for rating changes
\nall - Notification for rating, friends, contribution changes

$userlist [rating/all]
\n
\nList all username whose notifcation is on.
\nrating - Notification for rating changes
\nall - Notification for rating, friends, contribution changes

$blognotify [blog id]\n\nStart notification for given blog id.

$bloglist [blog id]\n\nList the blog id whose notification is on.

$blogstop [blog id]\n\nStop notification for given blog id.

"""
