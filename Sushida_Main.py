import csv
import glob
import os
import random
import sys
import time

from Moduls_sushida import Button

import pygame
from pygame.locals import *


#最初に出る画面 コースの選択もできる
#Welcom.wel()  で eazy=0,nomal=1,hard=3 を返す
class Welcom():

    def __init__(self,screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
    def wel(self):
        self.screen.fill((0,0,0))

        button_width , button_height= 200, 50
        select_dif0_button = Button(self.screen,0,button_width,button_height)
        select_dif1_button = Button(self.screen,0,button_width,button_height)
        select_dif2_button = Button(self.screen,0,button_width,button_height)

        select_dif0_button.creat_button(160,120,(0,0,0))
        select_dif1_button.creat_button(160,215,(0,0,0))
        select_dif2_button.creat_button(160,310,(0,0,0))

        select_dif0_button.set_text('eazy',75,(0,255,0))
        select_dif1_button.set_text('nomal',75,(0,0,255))
        select_dif2_button.set_text('hard',75,(255,0,0))

        #eazy=0,nomal=1,hard=3を返す
        pygame.display.update()
        while(True):
            events = pygame.event.get()
            for event in events:
                if(event.type==MOUSEBUTTONDOWN):
                    if(select_dif0_button.is_clickd(event)):
                        return 0
                    if(select_dif1_button.is_clickd(event)):
                        return 1
                    if(select_dif2_button.is_clickd(event)):
                        return 2
                if(event.type == QUIT):
                    pygame.quit()
                    sys.exit(0)
                else : self.clock.tick(0)
'''
            if(select_dif0_button.is_selectred(events)):
                return 0
            if(select_dif1_button.is_selectred(events)):
                return 1
            if(select_dif2_button.is_selectred(events)):
                return 2

            for event in events:
                if(event.type == QUIT):
                    pygame.quit()
                    sys.exit(0)
            else : self.clock.tick(30)
'''
#メインクラス
class Main_game():

    #コンストラクタ
    def __init__(self,screen):
        self.screen = screen
        self.font_big = pygame.font.SysFont(None,128)
        self.font_smole = pygame.font.SysFont(None,48)
        self.total_time = 0
        self.scor=0
        self.clock = pygame.time.Clock()
        self.sushi_list = self.make_sushi_list()
        self.img_sushi=self.select_img()

        path = os.path.join(os.path.dirname(__file__),"words.csv")
        with open(path, 'r', encoding="utf-8", newline="\n") as file:
            csv_ob = csv.reader(file)
            self.words = []
            for row in csv_ob:
                self.words.append(row[0])

    def set_dif(self,dif):
        self.dif = dif

    def get_limit_time(self):
        return self.limit_time

    def set_limit_time(self,limit_time):
        self.limit_time = limit_time

    def get_score(self):
        return self.scor

    def get_total_time(self):
        return self.total_time
    #ゲームの進行を担当するメソッド
    def game_loop(self):
        self.init_game()
        self.main_game()
    #ゲームの初期化をするメソッド
    def init_game(self):
        self.scor=0
        self.word=self.select_word()
        limit_time_list = [30,45,60]
        self.limit_time=limit_time_list[self.dif]
        pygame.display.set_caption("scor="+str(self.scor))

    def main_game(self):
        count3_start = pygame.time.get_ticks()
        count3 = pygame.time.get_ticks()
        while(int((count3 - count3_start)/1000) < 3):
            self.screen.fill((0,0,0))
            count3 = pygame.time.get_ticks()
            count3_lb = self.font_big.render(str(round(3 - (count3 - count3_start)/1000,3)),True,(255,255,255))
            self.screen.blit(count3_lb,(100,200))
            pygame.display.update()
            self.clock.tick(0)

        self.start_time = pygame.time.get_ticks()
        self.finished_time = pygame.time.get_ticks()

        while(True):
            self.screen.fill((200,200,200))

            pr_word = self.font_big.render(self.word,True,((0,0,0)))
            self.screen.blit(pr_word,(50,200))

            self.total_time = (pygame.time.get_ticks() - self.start_time)/1000
            if(self.total_time>self.limit_time):
                break

            delta_time = (pygame.time.get_ticks()-self.finished_time)/1000
            if(delta_time>3 and delta_time<5) :
                count5s_lb = self.font_big.render(str(delta_time),True,(255,0,0))
            elif (delta_time>5) :
                break
            else :
                count5s_lb = self.font_big.render(str(delta_time),True,(0,0,0))
            self.screen.blit(count5s_lb,(280,10))

            self.screen.blit(self.img_sushi,(720*delta_time/5,300))

            limit_time=int(self.limit_time-self.total_time)
            limit_time_lb = self.font_smole.render('last '+str(limit_time)+" seconds",True,(0,0,0))
            self.screen.blit(limit_time_lb,(100,100))

            pygame.display.update()

            self.handle_key_event(pygame.event.get())

            self.clock.tick(20)


    def handle_key_event(self,events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if chr(event.key) == self.word[0]:
                    self.cut_head_chr()
                    self.scor+=1
                    pygame.display.set_caption("scor= "+str(self.scor))
                    if self.is_empty_word():
                        self.img_sushi=self.select_img()
                        self.word=self.select_word()
                        self.finished_time=pygame.time.get_ticks()

    def cut_head_chr(self):
        self.word=self.word[1:]

    def is_empty_word(self):
        return not self.word

    #word[]中の文字列をランダムで返すメソッド
    def select_word(self):

        leng = len(self.words)
        return self.words[random.randint(0,leng-1)]

    def select_img(self):
        leng = len(self.sushi_list)
        i = random.randint(0,leng-1)
        return pygame.transform.scale(self.sushi_list[i],(100,100))

    def make_sushi_list(self):
        path = os.path.dirname(__file__)
        sushi_list = []
        path_list = glob.glob(os.path.join(path,'img/*.gif'))
        for path in path_list:
            sushi_list.append(pygame.image.load(path))
        return sushi_list

class GameOver():
    def __init__(self,screen):
        self.score = 0
        self.time = 1
        self.screen = screen
        self.big_font = pygame.font.SysFont(None,128)
        self.small_font = pygame.font.SysFont(None,48)
        self.clock = pygame.time.Clock()
    def set_score(self,score):
        self.score = score

    def set_time(self,time):
        self.time = time

    def game_over(self):
        self.screen.fill((0,0,0))

        type_speed =  self.score / self.time
        type_speed_lb = self.big_font.render(str(round(type_speed,3)) + ' key/s',True,(255,255,255))
        self.screen.blit(type_speed_lb,(100,100))

        button_again = Button(self.screen,0,250,50)
        button_select = Button(self.screen,0,250,50)

        button_again.creat_button(110,260,(255,255,255))
        button_select.creat_button(420,260,(255,255,255))

        button_again.set_text("play-again",38,(0,0,0))
        button_select.set_text("select-difficulity",38,(0,0,0))

        pygame.display.update()

        while(True):
            events = pygame.event.get()
            if(button_again.is_selectred(events)):
                return 'again'
            if(button_select.is_selectred(events)):
                return 'select'
            for event in events:
                if(event.type == QUIT):
                    pygame.quit()
                    sys.exit(0)
            self.clock.tick(30)




class Sushida():
    def __init__(self):
        pygame.init()
        (WIDTH,HEIGHT) = (720,480)
        self.dif = 0
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.wel = Welcom(self.screen)
        self.main_game = Main_game(self.screen)
        self.game_over = GameOver(self.screen)

    def game_loop(self):
        self.main_game.set_dif(self.dif)
        self.main_game.game_loop()

        score = self.main_game.get_score()
        time = self.main_game.get_total_time()

        self.game_over.set_score(score)
        self.game_over.set_time(time)
        hand = self.game_over.game_over()

        if(hand == 'again') :
            self.game_loop()

        if(hand == 'select') :
            self.select_def()
            self.game_loop()

    def select_def(self):
        self.dif = self.wel.wel()

    def again(self):
        self.game_loop()
    def select(self):
        self.game_loop()
if __name__ == "__main__":
    test_env = Sushida()
    test_env.select_def()
    test_env.game_loop()
    #matin_game = Main_game(test_env.screen)
