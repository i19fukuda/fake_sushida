import pygame
import sys
import random
import glob

#メインクラス
class Main_game():

    #コンストラクタ
    def __init__(self):
        pygame.init()
        (self.WIDTH,self.HEIGHT)=(720,480)
        self.screen = pygame.display.set_mode((self.WIDTH,self.HEIGHT))
        self.font_big = pygame.font.SysFont(None,128)
        self.font_smole = pygame.font.SysFont(None,48)
        self.limit_time=30
        self.scor=0
        self.clock = pygame.time.Clock()
        self.sushi_list = self.make_sushi_list()
        self.img_sushi=self.sushi_list[0]
        self.game_loop()

    #ゲームの進行を担当するメソッド
    def game_loop(self):
        self.init_game()
        self.main_game()
    #ゲームの初期化をするメソッド
    def init_game(self):
        self.scor=0
        self.word=self.select_word()
        self.start_time = pygame.time.get_ticks()
        self.finished_time = 0
        pygame.display.set_caption("scor="+str(self.scor))

    def main_game(self):
        while(True):
            self.screen.fill((200,200,200))

            pr_word = self.font_big.render(self.word,True,((0,0,0)))
            self.screen.blit(pr_word,(50,200))

            total_time = (pygame.time.get_ticks()-self.start_time)/1000
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
        self.screen.blit(speed_lb,(10,self.HEIGHT/2))
        pygame.display.update()
        pygame.time.delay(1000000)
if __name__ == "__main__":
    test_env = Main_game()