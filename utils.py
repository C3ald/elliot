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
base_HTB_url = 'https://www.hackthebox.com'
# Misc urls
meme_url = 'https://meme-api.com/gimme'
# HTB API token
HTB_API = open('htb_token.txt', 'r').read()
app_token = open('htb_app_token.txt', 'r').read()
#q = Query()
#a = db.search(q.name == 'Ceald')
#print(a)

headers = {'Authorization': f'Bearer {HTB_API}', 'Content-Type': 'wwwlication/json', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36'}
app_headers = {'Authorization': f'Bearer {app_token}', 'Content-Type': 'wwwlication/json', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36'}
def update_db(name, user_id, is_team=False):
        """ updates the database of ids and names. Returns 1 if user and id exists and will return 0 if database was updated properly teams can be used as well just put true if it is a team"""
        data = {'name': name, 'id': user_id, 'is_team': is_team}
        if data not in db.all():
                db.insert(data)
                return 0
        else:
                return 1


def get_user_info_username(user_name):
        Info = Query()
        user_id = db.search(Info.name == user_name)
        user_id = user_id[-1]
        user_id = user_id['id']
        url = profile_overview+str(user_id)
        print(url)
        re = r.get(url, headers=headers)
        response = dict(re.json())
        profile_info = response['profile']
        name = profile_info['name']
        rank = profile_info['rank']
        progress = profile_info['current_rank_progress']
        completion = profile_info['rank_ownership']
        points = profile_info['points']
        respects = profile_info['respects']
        bloods = profile_info['user_bloods'] + profile_info['system_bloods']
        global_ranking = profile_info['ranking']
        avatar = base_HTB_url + profile_info['avatar']
        print(profile_info)
        data = {'avatar':avatar,'name': name, 'rank': rank, 'completion': completion, 'rank progress': progress, 'points': points, 'respects': respects, 'bloods': bloods, 'global rank': global_ranking}
        return data



def get_user_info_id(user_id):
        """ gets user info based on id and updates the database """
        url = profile_overview+str(user_id)
        re = r.get(url, headers=headers)
        response = dict(re.json())
        profile_info = response['profile']
        name = profile_info['name']
        rank = profile_info['rank']
        progress = profile_info['current_rank_progress']
        completion = profile_info['rank_ownership']
        points = profile_info['points']
        respects = profile_info['respects']
        bloods = profile_info['user_bloods'] + profile_info['system_bloods']
        global_ranking = profile_info['ranking']
        avatar = base_HTB_url + profile_info['avatar']
        update_db(name, user_id)
        data = {'avatar':avatar,'name': name, 'rank': rank, 'completion': completion, 'rank progress': progress, 'points': points, 'respects': respects, 'bloods': bloods, 'global rank': global_ranking}
        return data


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
        
        re = r.get(top_100_global, headers=app_headers)
        #print(re.text)
        #print(re.status_code)
        response = dict(re.json())
        response = response['data']
        response = response[:limit]
        #print(response)
        formatted_data = []
        for data in response:
                rank = data['rank']
                points = data['points']
                user_id = data['id']
                name = data['name']
                country = data['country']
                print(country)
                total_owns = data['root_owns'] + data['user_owns'] + data['challenge_owns'] + data['fortress'] + data['endgame']
                bloods = data['root_bloods'] + data['user_bloods'] + data['challenge_bloods']
                avatar = base_HTB_url+data['avatar_thumb']
                fd = {'rank': rank, 'points': points, 'id': user_id, 'name': name, 'country': country, 'owns': total_owns, 'bloods': bloods, 'avatar': avatar}
                formatted_data.append(fd)
        return formatted_data