import requests as r
import json
from pythonping import ping as P

"""
HTB API requests and handling. Maybe some other things too 😉, HTB API docs: 
https://documenter.getpostman.com/view/13129365/TVeqbmeq#auth-info-60b37e03-af60-45c1-ad84-fb879f80cc65
"""

# HTB URLs
team_url = 'https://www.hackthebox.com/api/v4/team/info/'
profile_overview = 'https://www.hackthebox.com/api/v4/profile/'
top_100_global = "https://www.hackthebox.com/api/v4/rankings/users"
# Misc urls
meme_url = 'https://meme-api.com/gimme'

# HTB API token
HTB_API = open('htb_token.txt', 'r').read()


def get_profile(profile):
        """ gets the HTB profile of a given user """
        pass

def ping():
        """ ping test"""
        response = P('google.com', size=10, count=10)
        return response.rtt_avg_ms

def meme():
        """
        obtains a meme from the url: https://meme-api.com/gimme
        """
        re = r.get(meme_url)
        re_dict = dict(re.json())
        preview = re_dict['url']
        op = re_dict['author']
        title = re_dict['title']
        votes = re_dict['ups']
        sub = re_dict['subreddit']
        return {'preview': preview, 'op': op, 'title': title, 'votes': votes, 'sub': sub}
        

def get_htb_profile_overview(profile):
        headers = {'Authorization': f'Bearer {HTB_API}'}
        