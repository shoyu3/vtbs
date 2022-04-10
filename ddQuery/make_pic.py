import os
import time
import json
from .dd_account import *
from .api import *
from pathlib import Path
from PIL import Image, ImageFont, ImageDraw 

spath = os.path.split(__file__)[0]

font = []
font_size = [30, 25, 20, 10]
for i in font_size:
    font.append(ImageFont.truetype(f"{spath}/data/font/msyh.ttf", size = i))

class Pic():
    def __init__(self, ddAccount):
        self.dd = ddAccount
        self.line = int(self.dd.attention_vtb_nums / 500)
        if self.dd.attention_vtb_nums % 500 != 0:
            self.line += 1
        if self.dd.attention_vtb_nums < 500:
            self.height = 320 + len(self.dd.followed_vtbs) * 30
        else:
            self.height = 320 + 500 * 30
        self.img = Image.new(mode = "RGB", color = (255, 255, 255),
                             size = (100 + 500 * self.line, self.height))
        with open(f'{spath}/data/vtb_data_simple.json', 'r', encoding = 'utf8') as fp:
            vtbs_data = json.load(fp)
        self.vtbs = {}
        for i in vtbs_data:
            self.vtbs[i['mid']] = i
        self.draw_info()
        self.draw_vtbs()
        self.img.save(f"{spath}/cache/ddPic/" + str(self.dd.mid) + ".png")
    
    def draw_vtbs(self):
        for i in range(0, self.line):
            now_place = 230
            for j in range(0, 500):
                if (i)* 500 + j >= self.dd.attention_vtb_nums:
                    return
                now = self.dd.followed_vtbs[(i)* 500 + j]
                data = self.vtbs[now]['uname'] + " (" + str(now) + ") "
                if now in self.dd.medal.keys():
                    data = data + "  【" + self.dd.medal[now]['medal_info']['medal_name'] + "】 " + str(self.dd.medal[now]['medal_info']['level']) + " 级"
                self.draw.text((50 + i * 500, now_place), data, fill = "black", font = font[2])
                now_place += 30
            
    
    def draw_face(self):
        path = f"{spath}/cache/pic/" + str(self.dd.mid) + ".png"
        if not api.download_img(self.dd.user_info['face'], path):
            path = f"{spath}/cache/pic/Akkarin.jpg"
        face = Image.open(path)
        face = face.resize((100, 100))
        self.img.paste(face, (50, 40))
    
    def draw_level(self, width):
        path = f"{spath}/data/pic/level/" + str(self.dd.user_info['level_info']['current_level']) + ".png"
        level = Image.open(path)
        level = level.resize((30, 15))
        self. img.paste(level, (width, 55))
    
    def draw_info(self):
        self.draw_face()
        self.draw = ImageDraw.Draw(self.img)
        self.draw.text((160, 40), self.dd.name, fill = "black", font = font[1])
        width, h = font[1].getsize(self.dd.name)
        self.draw_level(162 + width)
        
        self.draw.text((160, 70), "MID: " + str(self.dd.mid), fill = "black", font = font[2])
        follow_radio = str(round(self.dd.ratio, 2)) + "% (" + str(self.dd.attention_vtb_nums) + "/" + str(self.dd.attention_nums) + ") "
        self.draw.text((160, 110), follow_radio, fill = "black", font = font[0])
        reg_time_array = time.localtime(int(self.dd.user_info['regtime']))
        reg_time = time.strftime("%Y-%m-%d %H:%M:%S", reg_time_array)
        self.draw.text((50, 160), "注册时间: " + reg_time, fill = "black", font = font[2])
        attentions = "粉丝: " + str(self.dd.user_info['fans']) + "    关注: " + str(self.dd.attention_nums)
        self.draw.text((50, 185), attentions, fill = "black", font = font[2])
        
        now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.draw.text((20, self.height - 50), 
                        "数据生成时间: " + now_time , fill = "black", font = font[3])
        
        vtb_time = os.stat(f'{spath}/data/vtb_data_simple.json').st_mtime
        vtb_modify_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(vtb_time))
        self.draw.text((20, self.height - 35), 
                        "vtbs数据更新时间: " + vtb_modify_time , fill = "black", font = font[3])
                        
        self.draw.text((20, self.height - 20), 
                        "create by ZBot, forbidden to republish without authorization!", fill = "black", font = font[3])
    
    def get_path(self): 
        return f"{spath}/cache/ddPic/" + str(self.dd.mid) + ".png"
        
