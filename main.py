from PPlay.gameimage import*
from PPlay.window import Window
from menu import Menu
from game import Game
from lead import Lead
import constantes
from time import sleep




janela = Window(640, 480)
janela.set_title("Run Scientist")
fundo = GameImage("background/background1.jpg")

menu = Menu(janela)
game = Game(janela)
lead = Lead(janela)

#Game loop
while constantes.screen != 2:
    fundo.draw()
    
    if constantes.screen == 0:
        sleep(0.1)
        menu.run()

    elif constantes.screen == 1:
        game.run()
    
    elif constantes.screen == 3:
        lead.run()
    

    janela.update()