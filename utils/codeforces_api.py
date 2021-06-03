import asyncio
import aiohttp

class CodeforcesAPI:
  def __init__(self):
    pass

  async def api_response(self, url, params=None):
    try:
      tries = 0
      async with aiohttp.ClientSession() as session:
        while tries < 5:
          tries += 1
          async with session.get(url, params=params) as resp:
            response = await resp.json()
            if response['status'] == 'FAILED' and 'limit exceeded' in response['comment'].lower():
              await asyncio.sleep(1)
            else:
              return response
        return response
    except Exception as e:
      return None

  async def user_info(self, handle):
    url = f"https://codeforces.com/api/user.info?handles={handle}"
    response = await self.api_response(url)
    if not response:
      return [False, "Codeforces API Error"]
    if response["status"] != "OK":
      return [False, response["comment"]]
    else:
      return [True, response["result"][0]]

  async def blog_info(self, blog_id):
    url = f"https://codeforces.com/api/blogEntry.comments?blogEntryId={blog_id}"
    response = await self.api_response(url)
    if not response:
      return [False, "Codeforces API Error"]
    if response["status"] != "OK":
      return [False, response["comment"]]
    else:
      return [True, response["result"]]