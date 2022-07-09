from PPlay.sprite import *
from PPlay.animation import *
from PPlay.window import *
from player_and_enemy import Jogador, Obstaculos, Books, Foods
from PPlay.collision import *
from PPlay.sound import *
import random
from time import sleep
import constantes

pygame.init()
pygame.mixer.music.load('musicas/menu.mp3')
pygame.mixer.music.play()
pygame.event.wait()

class Game(object):
     
    def __init__(self, janela):
        self.janela = janela
        self.teclado = janela.get_keyboard()
        self.jogador = Jogador(self.janela)
        self.obstaculos = Obstaculos(self.janela)
        self.books = Books(self.janela)
        self.gameover = Sound('musicas/game-over.mp3')
        self.win = Sound('musicas/win.mp3')
        self.foods = Foods(self.janela)
        self.pontuacao = constantes.score
        self.flag = False
        self.FPS = 0
        self.fpsAtual = 0
        self.cronometroFPS = 0
        self.timeout = 0
        self.fundo1 = Sprite("background/background1.jpg")
        self.fundo2 = Sprite("background/background2.jpg")
        self.vivo = True


    def scrolling(self): 
        self.fundo1.x -= constantes.vGame * self.janela.delta_time()
        self.fundo2.x -= constantes.vGame * self.janela.delta_time()
    
        if self.fundo2.x <= 0:
            self.fundo1.x = 0
            self.fundo2.x = +self.fundo2.width
    
        self.fundo1.draw()
        self.fundo2.draw()

    def levelScreen(self):
        if constantes.level <= 9:
            fundo1 = Sprite("background/background1.jpg")
            fundo1.draw()
            self.janela.draw_text(f"LEVEL {constantes.level+1}", self.janela.width/2 - 110 , (self.janela.height/2) - 80, size=70, bold=True, color=(0,0,0), font_name="Minecraft")
            self.janela.update()
            sleep(2)

    def nextLevel(self):
        self.reset()
        self.janela.update()
        constantes.level += 1
        constantes.vPlayer += 50
        constantes.vGame += 50

    def musicaGameplay(self):
        pygame.init()
        pygame.mixer.music.load('musicas/gameplay.mp3')
        pygame.mixer.music.play(-1)
        pygame.event.wait()

    def reset(self):
        self.jogador = Jogador(self.janela)
        self.obstaculos = Obstaculos(self.janela)
        self.books = Books(self.janela)
        self.foods = Foods(self.janela)
        self.jogador.set_pos()
        self.obstaculos.listaObstaculos.clear()
        self.books.listaBooks.clear()
        self.foods.listaFoods.clear()
        constantes.life = 6
        constantes.win = False
        constantes.bookCount = 0
    
    def gameOver(self):
        self.jogador = Jogador(self.janela)
        self.obstaculos = Obstaculos(self.janela)
        self.books = Books(self.janela)
        self.foods = Foods(self.janela)
        self.jogador.set_pos()
        self.obstaculos.listaObstaculos.clear()
        self.books.listaBooks.clear()
        self.foods.listaFoods.clear()
        self.janela.update()
        constantes.bookCount = 0
        constantes.vGame = constantes.vPlayer = 350
        constantes.life = 6
        constantes.level = 1


    def pedir_nome(self, debug=None):
            nome = ''
            backspace_cronometro = 0
            campo_nome = Sprite('buttons/textbox.png', 1)
            campo_nome.set_position(self.janela.width/2 - 210, self.janela.height/2 - 3)
            pressed_past = [False for i in range(26)]
            space_pressed_past = backspace_pressed_past = False
            letra_atual = ''
            while not self.teclado.key_pressed('enter'):
                nome_maxsize = 11
                self.janela.update()
                campo_nome.draw()
                self.janela.draw_text(f"PLAYER NAME:", self.janela.width/2 - 120, self.janela.height/2 - 50,
                                        45, (0, 0, 0), font_name="Minecraft")
                self.janela.draw_text(f"{nome}", self.janela.width/2 - 150, self.janela.height/2 + 50,
                                        48, (255, 255, 255))
                letra_atual = 'A'
                for i in range(26):
                    letra_atual = chr(ord('A') + (ord(letra_atual) + 1) % ord('A') % 26)
                    if self.teclado.key_pressed(letra_atual) and not pressed_past[i]\
                            and len(nome) < nome_maxsize:
                        nome += letra_atual
                    elif nome:
                        # if nome cumpre dois propositos: nao deixar o primeiro char ser espaço e evitar crash com nome[-1]
                        if self.teclado.key_pressed('space') and not space_pressed_past\
                                and len(nome) < nome_maxsize and nome[-1] != ' ':
                            nome += ' '
                        elif self.teclado.key_pressed('backspace') and not backspace_pressed_past \
                                and len(nome) > 0:
                            nome = nome[:-1]

                    pressed_past[i] = self.teclado.key_pressed(letra_atual)
                    space_pressed_past = self.teclado.key_pressed('space')
                    backspace_pressed_past = self.teclado.key_pressed('backspace')
                if debug:
                    debug.show_fps_if_debug()
            return nome


    def ranking(self):
        self.fundo1.draw()
        pygame.mixer.music.unload()
        if constantes.win == False:
            self.gameover.set_volume(100)
            self.gameover.play()
            fundo1 = Sprite("background/background1.jpg")
            fundo1.draw()
            self.janela.draw_text("GAME OVER =(", self.janela.width/2 - 200 , (self.janela.height/2) - 170, size=80, color=(0,0,0), font_name="Minecraft")
            nome = self.pedir_nome()
        else:
            self.win.set_volume(80)
            self.win.play()
            fundo1 = Sprite("background/background1.jpg")
            fundo1.draw()
            self.janela.draw_text(f"YOU WIN! =)", self.janela.width/2 - 160 , (self.janela.height/2) - 170, size=80, color=(0,0,0), font_name="Minecraft")
            nome = self.pedir_nome() 
        self.janela.update()
        arq = open('ranking.txt','r')
        conteudo = arq.readlines()
        linha = nome + '/' + str(int(constantes.score)) + '\n'
        conteudo.append(linha)
        arq.close()
        arq = open('ranking.txt', 'w')
        arq.writelines(conteudo)
        arq.close()
        print('Ranking atualizado com sucesso')
        constantes.screen = 3


    def run(self):
        #Controle de FPS
        self.cronometroFPS += self.janela.delta_time()
        self.FPS += 1
        if self.cronometroFPS > 1: 
            self.fpsAtual = self.FPS   
            self.FPS = 0
            self.cronometroFPS = 0
        
        if constantes.screen == 1:
            if self.flag == False:
                self.musicaGameplay()
                self.flag = True
                
        else:
            pygame.mixer.music.unload()

        self.scrolling()
        self.jogador.run()
        self.obstaculos.run()
        self.books.run()
        self.foods.run()

        if constantes.life == 0:
            self.ranking()
            constantes.score = 0
            self.flag = False
            self.gameOver()
            constantes.life = 6
            if(self.teclado.key_pressed("ESC")):
                constantes.screen = 0

        if constantes.bookCount >= 10:
            self.levelScreen()
            self.nextLevel()

        if constantes.level > 10:
            constantes.win = True
            self.ranking()
            self.gameOver()
            constantes.life = 6
            constantes.score = 0
            self.flag = False


        if(self.teclado.key_pressed("ESC")):
            constantes.screen = 0
            constantes.score = 0
            self.flag = False
            self.gameOver()
            constantes.life = 6

        self.janela.draw_text("FPS: "+f'{self.fpsAtual}', 0, 0, size=28, color=(255,255,255), font_name="Adolfine")
        self.janela.draw_text(f"SCORE = {constantes.score}", 30, 50, size=28, color=(0,0,0), font_name="Adolfine")
        self.janela.draw_text(f"BOOKS = {constantes.bookCount}/10", 30, 80, size=28, color=(0,0,0), font_name="Adolfine")
        self.janela.draw_text(f"LEVEL = {constantes.level}", 30, 110, size=28, color=(0,0,0), font_name="Adolfine")
        
        


