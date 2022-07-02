from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.gameobject import *
from PPlay.mouse import Mouse
import constantes

pygame.init()
pygame.mixer.music.load('musicas/menu.mp3')
pygame.mixer.music.play()
pygame.event.wait()



class Menu(object):
    
    def __init__(self, janela):
        self.janela = janela
        self.flag = False
        self.start = Sprite("buttons/start.png")
        self.exit = Sprite("buttons/exit.png")
        self.score = Sprite("buttons/score.png")
        self.title = Sprite("background/title.png")
        self.title.set_position(95, 30)
        self.mouse = Mouse()

    def set_pos(self):
        self.start.set_position(self.janela.width/2 - self.start.width/2, self.janela.height/3)
        self.score.set_position(self.start.x+10, self.start.y * 1.5)
        self.exit.set_position(self.start.x, self.start.y * 2)

    def _draw(self):
        self.start.draw()
        self.exit.draw()
        self.score.draw()
        self.title.draw()
    
    def musicaMenu(self):
        pygame.init()
        pygame.mixer.music.load('musicas/menu.mp3')
        pygame.mixer.music.play(-1)
        pygame.event.wait()

    def run(self):
        self._draw()
        self.set_pos()
        
        if constantes.screen == 0 or constantes.screen == 3:
            if self.flag == False:
                self.musicaMenu()
                if pygame.mixer.music.get_busy == False:
                    pygame.mixer.music.rewind
                self.flag = True

        if(self.mouse.is_over_object(self.start)):
            if(self.mouse.is_button_pressed(1)):
                constantes.screen = 1
                pygame.mixer.music.unload()
                self.flag = False
            
        if(self.mouse.is_over_object(self.exit)):
            if(self.mouse.is_button_pressed(1)):
                constantes.screen = 2
        
        if(self.mouse.is_over_object(self.score)):
            if(self.mouse.is_button_pressed(1)):
                constantes.screen = 3

