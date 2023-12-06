import requests as r
import json
from pythonping import ping as P

"""
HTB API requests and handling. Maybe some other things too 😉, HTB API docs: 
https://documenter.getpostman.com/view/13129365/TVeqbmeq#auth-info-60b37e03-af60-45c1-ad84-fb879f80cc65
"""
team_url = 'https://www.hackthebox.com/api/v4/team/info/'



def get_profile(profile):
        """ gets the HTB profile of a given user """
        pass

def ping():
        """ ping test"""
        response = P('google.com', size=10, count=10)
        return response.rtt_avg_ms