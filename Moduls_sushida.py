import pygame
from pygame.locals import *


#buttonオブジェクト
# obj = Button(surface,line_width,width,height)
# obj.create_button(left,top,(0,0,0))
#オブジェクト生成->配置->テキストの順に使用すること
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

    #(テキスト、サイズ、色)->fontをスクリーンに配置
    def set_text(self,text,size,co):
        font = pygame.font.SysFont(None,size)
        button_text = font.render(str(text),True,co)

        pos = font.size(text)
        text_width , text_heght = pos[0] , pos[1]
        cen = (
            self.left + self.rect.width / 2 - text_width / 2,
            self.top + self.rect.height /2 - text_heght / 2
        )
        self.SURFACE.blit(button_text,cen)

    def is_selectred(self,events):
        for event in events:
            if(event.type == MOUSEBUTTONDOWN):
                pos = pygame.mouse.get_pos()
                if(self.rect.collidepoint(pos)):
                    return True
                else:
                    return False

#最初に出る画面 コースの選択もできる
#Welcom.wel()  で eazy=0,nomal=1,hard=3 を返す