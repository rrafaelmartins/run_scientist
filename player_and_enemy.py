from pickle import FALSE
from PPlay import collision
from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.gameobject import *
from PPlay.collision import *
from PPlay.animation import *
from PPlay.sound import *
import constantes
from time import sleep
import random



class Jogador(object):
    def __init__(self, janela):
        self.janela = janela
        self.player = Sprite("player_and_enemy/boy.png", 1)
        self.heartBase = Sprite("player_and_enemy/heart.png", 1)
        self.heart0 = Sprite("player_and_enemy/heart0.png",1)
        self.heart1 = Sprite("player_and_enemy/heart1.png",1)
        self.heart2 = Sprite("player_and_enemy/heart2.png",1)
        self.heart3 = Sprite("player_and_enemy/heart3.png",1)
        self.heart4 = Sprite("player_and_enemy/heart4.png",1)
        self.heart5 = Sprite("player_and_enemy/heart5.png",1)
        self.heart6 = Sprite("player_and_enemy/heart6.png",1)
        self.teclado = self.janela.get_keyboard()
        self.duration()
        self.set_pos()
        self.score = 0
        self.fly()
        
    def duration(self):
        self.player.set_total_duration(constantes.duracao)

    def set_pos(self):
        self.player.x = self.janela.width/4
        self.player.y = self.janela.height/2
        
    def fly(self):
        if self.teclado.key_pressed("up"):
            if self.player.y >= 0:
                self.player.y += (self.janela.delta_time() * constantes.fps*-5)
        if self.teclado.key_pressed("down"):
            if self.player.y <= 308.60:
                self.player.y += (self.janela.delta_time() * constantes.fps*5)

    def changeHeart(self):
        self.heartBase.x = 500
        self.heartBase.y = 50
        if constantes.life == 6:
            self.heartBase = self.heart6
        if constantes.life == 5:
            self.heartBase = self.heart5
        if constantes.life == 4:
            self.heartBase = self.heart4
        if constantes.life == 3:
            self.heartBase = self.heart3
        if constantes.life == 2:
            self.heartBase = self.heart2
        if constantes.life == 1:
            self.heartBase = self.heart1
        if constantes.life == 0:
            self.heartBase = self.heart0
        self.heartBase.draw()

    def run(self):
        if constantes.cont == 0:
            self.set_pos()
            constantes.cont += 1
        self.fly()
        self.changeHeart()
        self.player.draw()
        self.player.update()


class Obstaculos(object):
    def __init__(self, janela):
        self.janela = janela
        self.listaObstaculos = []
        self.obstaculo1 = Sprite("player_and_enemy/beer.png")
        self.obstaculo2 = Sprite("player_and_enemy/cellphone.png")
        self.hit = Sound('musicas/hit.mp3')
        self.teclado = self.janela.get_keyboard()
        self.obstaculo1.x = self.janela.width + 20
        self.obstaculo2.x = self.janela.width + 120
        self.obstaculo1.y = self.janela.height/3
        self.obstaculo2.y = self.janela.height * (2/3)
        self.listaObstaculos.append(self.obstaculo1)
        self.listaObstaculos.append(self.obstaculo2)
        self.jogador = Jogador(self.janela)

    def set_pos(self):
        self.jogador.player.x = self.janela.width/4
        self.jogador.player.y = self.janela.height/2
        
    def spawn(self):
        if len(self.listaObstaculos) == 0:
            for c in range(2):
                sorteio = random.randint(0,1)
                if sorteio == 0:
                    self.listaObstaculos.append(Sprite("player_and_enemy/beer.png"))
                else:
                    self.listaObstaculos.append(Sprite("player_and_enemy/cellphone.png"))
            for i in self.listaObstaculos:
                index = self.listaObstaculos.index(i)
                obstaculo_x = random.randint(self.janela.width+10, self.janela.width+600)
                obstaculo_y = random.randint(self.janela.height/5, self.janela.height * (2/3))
                self.listaObstaculos[index].set_position(obstaculo_x, obstaculo_y)

    def moverObstaculos(self):
        for i in range(len(self.listaObstaculos)):
            self.listaObstaculos[i].x -= (constantes.vGame * self.janela.delta_time())
        
    def checarColisao(self):
        if len(self.listaObstaculos) > 0:
            for i in self.listaObstaculos:
                if (self.jogador.player.collided(i)):
                    self.listaObstaculos.remove(i)
                    self.hit.set_volume(50)
                    self.hit.play()
                    self.janela.update()

                    constantes.life -= 1
                    continue
                if  (i.x <= 0-i.width):
                    self.listaObstaculos.remove(i)
                    continue

    def _draw(self):
        for i in range(len(self.listaObstaculos)):
                self.listaObstaculos[i].draw()

    def run(self):
        self.spawn()
        self.moverObstaculos()
        self.jogador.fly()
        self.checarColisao()
        self._draw()


class Books(object):
    def __init__(self, janela):
        self.janela = janela
        self.listaBooks = []
        self.teclado = self.janela.get_keyboard()
        self.book1 = Sprite("player_and_enemy/book.png")
        self.book2 = Sprite("player_and_enemy/book.png")
        self.collect = Sound('musicas/collect.mp3')
        self.book1.x = self.janela.width + 100
        self.book2.x = self.janela.width + 200
        self.book1.y = self.janela.height/3
        self.book2.y = self.janela.height * (2/3)
        self.listaBooks.append(self.book1)
        self.listaBooks.append(self.book2)
        self.jogador = Jogador(self.janela)
    
    def spawn(self):
        if len(self.listaBooks) == 0:
            for c in range(2):
                book_x = random.randint(self.janela.width+10, self.janela.width+600)
                book_y = random.randint(self.janela.height/5, self.janela.height * (2/3))
                self.listaBooks.append(Sprite("player_and_enemy/book.png"))
                self.listaBooks[c].x = book_x
                self.listaBooks[c].y = book_y

    def moverBooks(self):
        for i in range(len(self.listaBooks)):
            self.listaBooks[i].x -= (constantes.vGame * self.janela.delta_time())

    def checarColisao(self):
        if len(self.listaBooks) > 0:
            for i in self.listaBooks:
                if (self.jogador.player.collided(i)):
                    self.listaBooks.remove(i)
                    self.collect.set_volume(50)
                    self.collect.play()
                    self.janela.update()
                    constantes.score += 100
                    constantes.bookCount += 1
                    continue
                if  (i.x <= 0-i.width):
                    self.listaBooks.remove(i)
                    continue

    def _draw(self):
        for i in range(len(self.listaBooks)):
                self.listaBooks[i].draw()

    def run(self):
        self.spawn()
        self.moverBooks()
        self.jogador.fly()
        self.checarColisao()
        self._draw()

class Foods(object):
    def __init__(self, janela):
        self.janela = janela
        self.listaFoods = []
        self.teclado = self.janela.get_keyboard()
        self.cronometroFood = 0
        self.food1 = Sprite("buffs/food1.png",1)
        self.food2 = Sprite("buffs/food2.png",1)
        self.food3 = Sprite("buffs/food3.png",1)
        self.powerup = Sound('musicas/powerup.mp3')
        self.food4 = Sprite("buffs/food4.png",1)
        self.food5 = Sprite("buffs/food5.png",1)
        self.food6 = Sprite("buffs/food6.png",1)
        self.jogador = Jogador(self.janela)
    
    def spawn(self):
        if len(self.listaFoods) == 0:
            for c in range(2):
                sorteio = random.randint(1,6)
                self.listaFoods.append(Sprite(f"buffs/food{sorteio}.png"))
            for i in self.listaFoods:
                index = self.listaFoods.index(i)
                food_x = random.randint(self.janela.width+10, self.janela.width+600)
                food_y = random.randint(self.janela.height/5, self.janela.height * (2/3))
                self.listaFoods[index].set_position(food_x, food_y)
    
    def moverFoods(self):
        for i in range(len(self.listaFoods)):
            self.listaFoods[i].x -= (constantes.vGame * self.janela.delta_time())

    def checarColisao(self):
        if len(self.listaFoods) > 0:
            for i in self.listaFoods:
                if (self.jogador.player.collided(i)):
                    self.listaFoods.remove(i)
                    self.powerup.set_volume(100)
                    self.powerup.play()
                    self.janela.update()
                    if constantes.life < 6:
                        constantes.life += 1
                    continue
                if (i.x <= 0-i.width):
                    self.listaFoods.remove(i)
                    continue

    def _draw(self):
        for i in range(len(self.listaFoods)):
                self.listaFoods[i].draw()

    def run(self):
        self.spawn()
        self.moverFoods()
        self.jogador.fly()
        self.checarColisao()
        self._draw()
