from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.gameobject import *
import constantes

class Lead(object):
    def __init__(self, janela):
        self.janela = janela
        self.teclado = janela.get_keyboard()
        self.fundo = GameImage("background/background1.jpg")
        self.leaderboard = GameImage("background/leaderboard.png")
        self.leaderboard.set_position(70, 30)

    
    def run(self):
        self.fundo.draw()
        self.leaderboard.draw()
        arq = open('ranking.txt','r')
        conteudo = arq.readlines()
        nomes=[]
        pontos=[]
        for i in range(len(conteudo)):
            linha=conteudo[i].split('/')
            nomes.append(linha[0])
            pontos.append(int(linha[1].rstrip('\n')))
        arq.close()
        
        for j in range(10):
            for i in range(len(pontos)-1):
                if pontos[i] < pontos[i+1]:
                    pontos[i+1],pontos[i]=pontos[i],pontos[i+1]
                    nomes[i+1],nomes[i]=nomes[i],nomes[i+1]

        for i in range(len(nomes)):
            if i == 5:
                break
            self.janela.draw_text('{} - Name: {} / Score: {}'.format(i+1, nomes[i], pontos[i]), self.janela.width/2 - 230, (self.janela.height/2 - 60) + i*50, size=28, color=(0, 0, 0), font_name="")
        
        if(self.teclado.key_pressed("ESC")):
            constantes.screen = 0 