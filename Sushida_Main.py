import pygame
import sys
import random
import glob
import time
from pygame.locals import *


#buttonオブジェクト
# obj = Button(surface,line_width,width,height)
# obj.create_button(left,top,(0,0,0))
class Button():
    def __init__(self,surface,line_width,width,height):
        self.SURFACE = surface
        self.LINE_WIDTH = line_width
        (self.WIDTH,self.HEIGHT) = (width,height)

    def creat_button(self,x,y,co):
        self.left = x
        self.top = y
        self.rect = pygame.Rect((self.left,self.top),(self.WIDTH,self.HEIGHT))
        pygame.draw.rect(self.SURFACE,co,self.rect,self.LINE_WIDTH)

    def is_selectred(self,events):
        for event in events:
            if(event.type == MOUSEBUTTONDOWN):
                pos = pygame.mouse.get_pos()
                if(self.rect.collidepoint(pos)):
                    print("oh")
                    return True
                else:
                    print("nono")
                    return False


class Welcom():

    def __init__(self,screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
    def wel(self):
        self.screen.fill((0,0,0))
        pygame.display.update()
        start_button = Button(self.screen,0,200,50)
        start_button.creat_button(600,400,(255,255,255))
        pygame.display.update()
        while(True):
            events = pygame.event.get()
            if(start_button.is_selectred(events)):
                break
            else : self.clock.tick(30)

#メインクラス
class Main_game():

    #コンストラクタ
    def __init__(self,screen):
        self.screen = screen
        self.font_big = pygame.font.SysFont(None,128)
        self.font_smole = pygame.font.SysFont(None,48)
        self.limit_time=30
        self.scor=0
        self.clock = pygame.time.Clock()
        self.sushi_list = self.make_sushi_list()
        self.img_sushi=self.sushi_list[0]

    #ゲームの進行を担当するメソッド
    def game_loop(self):
        self.init_game()
        self.main_game()
    #ゲームの初期化をするメソッド
    def init_game(self):
        self.scor=0
        self.word=self.select_word()
        pygame.display.set_caption("scor="+str(self.scor))

    def main_game(self):
        self.start_time = pygame.time.get_ticks()
        self.finished_time = pygame.time.get_ticks()
        while(True):
            self.screen.fill((200,200,200))

            pr_word = self.font_big.render(self.word,True,((0,0,0)))
            self.screen.blit(pr_word,(50,200))

            total_time = (pygame.time.get_ticks() - self.start_time)/1000
            total_time_lb = self.font_smole.render(str(total_time),True,(0,0,0))
            self.screen.blit(total_time_lb,(50,400))
            if(total_time>self.limit_time):
                self.game_over()

            delta_time = (pygame.time.get_ticks()-self.finished_time)/1000
            if(delta_time>3 and delta_time<5) :
                count5s_lb = self.font_big.render(str(delta_time),True,(255,0,0))
            elif (delta_time>5) :
                self.game_over()
            else :
                count5s_lb = self.font_big.render(str(delta_time),True,(0,0,0))
            self.screen.blit(count5s_lb,(280,10))

            self.screen.blit(self.img_sushi,(720*delta_time/5,300))

            limit_time=int(30-total_time)
            limit_time_lb = self.font_smole.render('last '+str(limit_time)+" seconds",True,(0,0,0))
            self.screen.blit(limit_time_lb,(100,100))

            pygame.display.update()

            for event in pygame.event.get():
                self.handle_key_event(event)
            self.clock.tick(30)


    def handle_key_event(self,event):
        if event.type == pygame.QUIT:
            sys.exit()
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
        word = [
            'apple',
            'pineapple',
            'pen'
            ]
        leng = len(word)
        return word[random.randint(0,leng-1)]

    def select_img(self):
        leng = len(self.sushi_list)
        i = random.randint(0,leng-1)
        return self.sushi_list[i]

    def make_sushi_list(self):
        sushi_list = []
        path_list = glob.glob('sushida/img/*.gif')
        for path in path_list:
            sushi_list.append(pygame.image.load(path))
        return sushi_list

    def game_over(self):
        self.screen.fill((200,200,200))
        type_speed = self.scor/30
        type_speed = round(type_speed,3)
        speed_lb=self.font_big.render(str(type_speed)+'key/s',True,(0,0,0))
        height = self.screen.get_height()
        self.screen.blit(speed_lb,(10,height/2))
        pygame.display.update()
        pygame.time.delay(1000000)

class Sushida():
    pygame.init()
    (WIDTH,HEIGHT)=(720,480)
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    wel = Welcom(screen)
    wel.wel()
    time.sleep(2)
    matin_game = Main_game(screen)
    matin_game.game_loop()
if __name__ == "__main__":
    test_env = Sushida()
    #matin_game = Main_game(test_env.screen)