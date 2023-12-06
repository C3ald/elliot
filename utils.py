import requests as r
import json
from pythonping import ping as P
from tinydb import TinyDB, Query
db = TinyDB('db.json')

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


def update_db(name, id):
        """ updates the database of ids and names. Returns 1 if user and id exists and will return 0 if database was updated properly"""
        data = {'name': name, 'id': id}
        if data not in db.all():
                db.insert(data)
                return 0
        else:
                return 1

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
        

def get_htb_top_100(limit):
        """ limit sets a limit for number of retrieved users, like top 30 if limit is set to 30 returns a list of dictionaries"""
        limit = int(limit)
        print(limit)
        headers = {'Authorization': f'Bearer {HTB_API}'}
        re = r.get(top_100_global, headers=headers)
        response = dict(re.json())
        response = response['data']
        response = response[:limit]
        print(response)
        formatted_data = []
        for data in response:
                rank = data['rank']
                points = data['points']
                user_id = data['id']
                name = data['name']
                country = 'country'
                total_owns = data['root_owns'] + data['user_owns'] + data['challenge_owns'] + data['fortress'] + data['endgames']
                bloods = data['root_bloods'] + data['user_bloods'] + data['challenge_bloods']
                fd = {'rank': rank, 'points': points, 'id': user_id, 'name': name, 'country': country, 'owns': total_owns, 'bloods': bloods}
                formatted_data.append(fd)
        return formatted_data