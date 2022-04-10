import os
import json
from ddQuery import api

spath = os.path.split(__file__)[0]

class ddAccount():
    def __init__(self, name = None, mid = None):
        if name == None and mid == None:
            return False
        if mid == None:
            self.mid = api.search_user(name)['mid']
        else:
            self.mid = mid
        self.user_info = api.get_info(self.mid)
        self.name = self.user_info['name']
        self.attentions = self.user_info['attentions']
        self.followed_vtbs = self.get_followed_vtbs()
        self.get_medal_wall()
        self.attention_nums = len(self.attentions)
        self.attention_vtb_nums = len(self.followed_vtbs)
        self.ratio = self.attention_vtb_nums / self.attention_nums * 100
    
    def get_followed_vtbs(self):
        if self.user_info == None:
            self.user_info = api.get_info(self.mid)
        with open(f'{spath}/data/vtb_data_simple.json', 'r', encoding = 'utf8') as fp:
            vtb_data = json.load(fp)
        vtbs = []
        for i in vtb_data:
            if i['mid'] in self.attentions:
                vtbs.append(i['mid'])
        return vtbs
        
    def get_medal_wall(self):
        raw_data = api.get_medal(self.mid)
        self.medal = {}
        if raw_data == None:
            return
        for i in raw_data['list']:
            self.medal[i['medal_info']['target_id']] = i