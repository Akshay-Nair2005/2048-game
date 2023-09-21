# importing modules
import numpy as np
import random
import pygame
from pygame.locals import *
import pygame_menu

# global variables
N = 4
W = 400
H = 400
SPACING = 10

# colors
COLORS = {
    'back': (189, 172, 161),
    0: (204, 192, 179),
    2: (238, 228, 219),
    4: (240, 226, 202),
    8: (242, 177, 121),
    16: (236, 141, 85),
    32: (250, 123, 92),
    64: (234, 90, 56),
    128: (237, 207, 114),
    256: (242, 208, 75),
    512: (237, 200, 80),
    1024: (227, 186, 19),
    2048: (236, 196, 2)
}

# The main Game Logic
class GameLogic:
    
    # This method is called every time an object is created from the class
    def __init__(self):
        self.grid = grid = np.zeros((N,N), dtype=int)
        
        self.W = 400
        self.H = self.W
        self.SPACING = 10

        pygame.init()
        pygame.display.set_caption(" Game in Python ")

        pygame.font.init()
        self.myfont = pygame.font.SysFont('Times New Roman', 30)

        self.screen = pygame.display.set_mode((self.W, self.H))
        logo = pygame.image.load('logo.png')
        pygame.display.set_icon(logo)
    
    
    # This method generated new number
    def new_number (self, k=1):
        pos_zeros = list(zip(*np.where(self.grid == 0)))
        
        for pos in random.sample(pos_zeros, k=k):
            if random.random() < 0.1:
                self.grid[pos] = 4
            else:
                self.grid[pos] = 2
    
    
    # 
    @staticmethod           
    def get_number(this):
        this_n = this[this!=0]
        this_n_sum = []
        skip = False
        
        for j in range(len(this_n)):
            if skip:
                skip = False
                continue
            
            if j != len(this_n) - 1 and this_n[j] == this_n[j+1]:
                new_number = this_n[j] * 2
                skip = True
                
            else:
                new_number = this_n[j]
                
            this_n_sum.append(new_number)
        
        return np.array(this_n_sum)
     
    
    # This method shifts the elements in the array 
    def make_move(self, move):
        
        for i in range(N):
            
            if move in 'lr':
                this = self.grid[i,:]
                
            elif move in 'ud':
                this = self.grid[:,i]
                
            else:
                print('wrong command')
                break
             
            flipped = False   
            if move in 'rd':
                flipped = True
                this = this[::-1]
                
            this_n = self.get_number(this)
            
            new_this = np.zeros_like(this)
            new_this[:len(this_n)] = this_n
            
            if flipped:
                new_this = new_this[::-1]
                
            if move in 'lr':
                self.grid[i,:] = new_this
            else:
                self.grid[:,i] = new_this


    # This method creates the GUI needed for the game
    def draw_game(self):
        
        if self.game_over():
            self.screen.fill(COLORS['back'])
            self.game_over_screen()
        
        elif (2048 in self.grid):
            self.screen.fill(COLORS['back'])
            self.win_screen()
           
        else:
            self.screen.fill(COLORS['back'])
            for i in range(N):
                for j in range(N):
                    n = self.grid[i][j]

                    rect_x = j * self.W // N + self.SPACING
                    rect_y = i * self.H // N + self.SPACING
                    rect_w = self.W // N - 2 * self.SPACING
                    rect_h = self.H // N - 2 * self.SPACING

                    pygame.draw.rect(self.screen,
                                    COLORS[n],
                                    pygame.Rect(rect_x, rect_y, rect_w, rect_h),
                                    border_radius=8)
                    if n == 0:
                        continue
                    text_surface = self.myfont.render(f'{n}', True, (0, 0, 0))
                    text_rect = text_surface.get_rect(center=(rect_x +  rect_w / 2, rect_y + rect_h / 2))
                    self.screen.blit(text_surface, text_rect)
    
    
    # This method waits for key press and returns the desired value
    @staticmethod
    def wait_for_key():
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return 'q'
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        return 'u'
                    elif event.key == K_RIGHT:
                        return 'r'
                    elif event.key == K_LEFT:
                        return 'l'
                    elif event.key == K_DOWN:
                        return 'd'
                    elif event.key == K_q or event.key == K_ESCAPE:
                        return 'q'


    # This methods checks whether there are no more possible moves left
    def game_over(self):
        grid_bu = self.grid.copy()
        for move in 'lrud':
            self.make_move(move)
            if not all((self.grid == grid_bu).flatten()):
                self.grid = grid_bu
                return False
        return True

    
    # This method creates GUI for game over screen
    def game_over_screen(self):
        
        text = self.myfont.render("Game Over", True, (0,0,0))
        text_rect = text.get_rect()
        text_x = self.screen.get_width() / 2 - text_rect.width / 2
        text_y = self.screen.get_height() / 2 - text_rect.height / 2
        self.screen.blit(text, [text_x, text_y])
        clock = pygame.time.Clock()
        clock.tick(120)
        
    
    # This method creates GUI for winning screen
    def win_screen(self):
               
        text = self.myfont.render("Congrats! You won!", True, (0,0,0))
        text_rect = text.get_rect()
        text_x = self.screen.get_width() / 2 - text_rect.width / 2
        text_y = self.screen.get_height() / 2 - text_rect.height / 2
        self.screen.blit(text, [text_x, text_y])
        clock = pygame.time.Clock()
        clock.tick(120)
        
    
    # This is the main method, that combines all the above given methods together to create and run the game   
    def play(self):
        self.new_number(k=2)
        
        while(True):
            self.draw_game()
            pygame.display.flip()
            cmd = self.wait_for_key()
            if cmd == 'q':
                break
            old_grid = self.grid.copy()
            self.make_move(cmd)
            
            if self.game_over():
                self.game_over_screen()
                break
            
            if (2048 in self.grid):
                self.win_screen()
                break
            
            if not all((self.grid == old_grid).flatten()): 
                self.new_number()


def how_play():
    print('''
                                In this game we are using the adition skill of human.
                    The Goal here is to reach the number 2048 by Adding randomly generated powers of 2.
''')
    print('''
                                               Up Key to move the Grid up.
                                             Down Key to move the Grid down.
                                             Left Key to move the Grid left.
                                            Right Key to move the Grid right.
                                                   Esc Key to Quit.

            ---------------------------------------------------------------------------------------------------
            
          ''')


# Creates a game object and calls the 'play' method
def start_the_game():
    game = GameLogic()
    how_play()
    game.play()


#Creates a screen needed for the main menu
pygame.init()
surface = pygame.display.set_mode((400, 400))
pygame.display.set_caption(" Game in Python ")
logo = pygame.image.load('logo.png')
pygame.display.set_icon(logo)

#Designing the menu
mytheme = pygame_menu.themes.THEME_ORANGE.copy()
mytheme.title_background_color= COLORS['back']
mytheme.background_color= COLORS[0]
mytheme.title_font_color = (0,0,0)
mytheme.widget_font_color = (0,0,0)

menu = pygame_menu.Menu('   2048   ', 400, 400, theme = mytheme)

#Adding buttons
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

#This method returns until the Menu is updated (a widget status has changed). 
menu.mainloop(surface)
