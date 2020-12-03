#-------------------------------------
#           Tetris Game
# Controls: 
# Left Key: Move block to left
# Right Key: Move blocks to right
# Up Key: Rotate a dropping block
# Down Key: Move dropping block downward by single step
# Space Key: Sudden drop at the projected positon
# Escape Ley: Pause the game
#-------------------------------------

# Importing Packages 
import pygame
import random
from pygame import mixer
import time
 

#Initializing the Pygame components
pygame.font.init()  #For displaying texts
pygame.mixer.init() #For playing music

# Global Variables
screen_width = 1300          #Width of Pygame window
screen_height = 700          #Height of Pygame window
no_of_hor_boxes = 10    #No of horizontal block in playing window
no_of_ver_boxes = 20    #No of vertical block in playing window
block_size = 30         #Each square of the tetris is 30x30 pixels
playing_window_width = no_of_hor_boxes * block_size 
playing_window_height = no_of_ver_boxes * block_size

score=0                 #Initialising score

top_left_x_coordinate = (screen_width - playing_window_width) // 2    #x coordiante of the top left of playing window
top_left_y_coordinate = screen_height - playing_window_height         #y coordiante of the top left of playing window

#control variable for gameplay
pause=False           
menu=False
gameover=False 
control=False
main_menu_active = True
intermediate_menu_active = False
counter_t_menu = 1
 
# Various shapes
Shape1 = [[ '     ',
            '  O  ',
            '  OO ',
            '   O ',
            '     '],
            ['     ',
            '     ',
            '  OO ',
            ' OO  ',
            '     ']]
 
Shape2 = [[ '     ',
            '     ',
            ' OO  ',
            '  OO ',
            '     '],
            ['     ',
            '  O  ',
            ' OO  ',
            ' O   ',
            '     ']]
 
Shape3 = [[ '  O  ',
            '  O  ',
            '  O  ',
            '  O  ',
            '     '],
            ['     ',
            'OOOO ',
            '     ',
            '     ',
            '     ']]
 
Shape4 = [[ '     ',
            '     ',
            ' OO  ',
            ' OO  ',
            '     ']]
 
Shape5 = [[ '     ',
            ' O   ',
            ' OOO ',
            '     ',
            '     '],
            ['     ',
            '  OO ',
            '  O  ',
            '  O  ',
            '     '],
            ['     ',
            '     ',
            ' OOO ',
            '   O ',
            '     '],
            ['     ',
            '  O  ',
            '  O  ',
            ' OO  ',
            '     ']]
 
Shape6 = [[ '     ',
            '   O ',
            ' OOO ',
            '     ',
            '     '],
            ['     ',
            '  O  ',
            '  O  ',
            '  OO ',
            '     '],
            ['     ',
            '     ',
            ' OOO ',
            ' O   ',
            '     '],
            ['     ',
            ' OO  ',
            '  O  ',
            '  O  ',
            '     ']]
 
Shape7 = [[ '     ',
            '  O  ',
            ' OOO ',
            '     ',
            '     '],
            ['     ',
            '  O  ',
            '  OO ',
            '  O  ',
            '     '],
            ['     ',
            '     ',
            ' OOO ',
            '  O  ',
            '     '],
            ['     ',
            '  O  ',
            ' OO  ',
            '  O  ',
            '     ']]
 
shapes = [Shape1, Shape2, Shape3, Shape4, Shape5, Shape6, Shape7] #List of shapes

#Loading the images for background and block textures
background = pygame.image.load('asset/image/background.jpeg')
control_img = pygame.image.load('asset/image/control.jpg')
block1 = pygame.image.load('asset/image/1.jpg')
block2 = pygame.image.load('asset/image/2.jpg')
block3 = pygame.image.load('asset/image/3.jpg')
block4 = pygame.image.load('asset/image/4.jpg')
block5 = pygame.image.load('asset/image/5.jpg')
block6 = pygame.image.load('asset/image/6.jpg')
block7 = pygame.image.load('asset/image/7.jpg')
block8 = pygame.image.load('asset/image/8.jpg')
block9 = pygame.image.load('asset/image/9.jpg')
block10 = pygame.image.load('asset/image/10.jpg')
block11 = pygame.image.load('asset/image/11.jpg')
block12 = pygame.image.load('asset/image/12.jpg')
projected = pygame.image.load('asset/image/projected.png')
buttonpause=pygame.image.load('asset/image/pause_button.png')
button_active=pygame.image.load('asset/image/button_active.png')
button_inactive=pygame.image.load('asset/image/button_inactive.png')

shape_colors = [block1,block2,block3,block4,block5,block6,block7,block8,block9,block10,block11,block12]


#Loading music files.
music_main_page = pygame.mixer.Sound('asset/audio/main_page.mp3')
music_first_level = pygame.mixer.Sound('asset/audio/first_level.mp3')
music_second_level = pygame.mixer.Sound('asset/audio/second_level.mp3')
music_last_level = pygame.mixer.Sound('asset/audio/last_level.mp3')
music_line_clear = pygame.mixer.Sound('asset/audio/line.mp3')
music_game_over = pygame.mixer.Sound('asset/audio/game_over.mp3')

#Class for a single shape
class Shape(object):
    def __init__(self, x, y, shape):
        self.x = x                                  #x coordinate of the shape
        self.y = y                                  #y coordinate of the shapes
        self.shape = shape
        self.color = random.choice(shape_colors)    #randomly choosing a texture for the block
        self.rotation = 0                           #initial rotation

#Function to create grid of the tetris
#Grid contains a list of list of all positions of the tetris playing window
#Example:  1. grid[i][j] = ("UNOCCUPIED"  , (0,0,0))     #(0,0,0) denotes black color
#          2. grid[i][j] = ("OCCUPIED"    , Textue )     #Texture denotes the particular texture of that grid
#locked_positions is a dictionary that contains the locked position of the block, i.e. blocks that has already fallen
#Example:   locked_positions[(i,j)] = Texture
def create_grid(locked_positions):
    grid = []
    #First initializing the grid with all blacks
    for i in range(no_of_ver_boxes):
        lst = []
        for j in range(no_of_hor_boxes):
            lst.append(("UNOCCUPIED",(0,0,0)))
        grid.append(lst)
    #Replace the blacks with texture using the locked position dictionary
    for i in range(no_of_ver_boxes):
        for j in range(no_of_hor_boxes):
            if (j,i) in locked_positions:
                grid[i][j] = ("OCCUPIED",locked_positions[(j,i)])
    return grid

#Convert a particular shape to a list of indices based of the existance of blocks in the shapes
def convert_shape_to_index(shape):
    positions = []
    format = shape.shape[shape.rotation]
    for i in range(len(format)):
        line = format[i]
        for j in range(len(line)):
            if line[j] == 'O':
                positions.append((shape.x+j-2,shape.y+i-4))
    return positions

#Checking is the shape can be fit in the current grid, based on this we are stopping the blocks
def check_validity(shape, grid):
    accepted_positions = [[(j, i) for j in range(no_of_hor_boxes) if grid[i][j][0] == "UNOCCUPIED"] for i in range(no_of_ver_boxes)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_to_index(shape)
    for pos in formatted:
        if pos[0]<0:                        #Left bound
            return False
        if pos[0]>=no_of_hor_boxes:         #Right bound 
            return False
        if pos not in accepted_positions:   #Obstacle
            if pos[1] > -1:
                return False
    return True     #If nothing is found then its valid block
    
#Check when we lose the game, based on the highest block, i.e, if any block touch the top wall
def is_losing(positions):
    for _,y in positions:
        if y<1:
            return True
    return False

#Generating a random shape
def get_new_shape():
    return Shape(5,0,random.choice(shapes))

#Clearing a row when entire row is occupied
def clear_rows(grid, locked):
    inc=0
    for i in range(len(grid)-1,-1,-1):
        row= grid[i]
        if ("UNOCCUPIED",(0,0,0)) not in row:
            pygame.mixer.Channel(2).play(music_line_clear) #Playing the music when row is clear
            inc+=1
            ind=i
            for j in range(len(row)):
                try:
                    del locked[(j,i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x ,y = key
            if y < ind:
                newkey = (x,y+inc)
                locked[newkey]= locked.pop(key)
    return locked,inc

#Function to draw the next shape and next to next shape which are going to come
def draw_next_shape(shape, shape1, win):
    #Displaying the text on the right side of playing window
    draw_text('Next Shape',30,(255,255,0),win, (top_left_x_coordinate+playing_window_width+140,top_left_y_coordinate-30))
    draw_text('Next to Next',30,(255,255,0),win, (top_left_x_coordinate+playing_window_width+140,top_left_y_coordinate+150))
    next_shape = shape.shape[shape.rotation]                #selecting the rotation of the shapes
    next_to_next_shape = shape1.shape[shape1.rotation]
    for i in range(5):
        for j in range(5):
            if next_shape[i][j] == 'O':
                win.blit(shape.color,(top_left_x_coordinate+playing_window_width+50+j*30 ,  top_left_y_coordinate+i*30))    #Drawing the textures
            if next_to_next_shape[i][j] == 'O':
                win.blit(shape1.color,(top_left_x_coordinate+playing_window_width+50+j*30 , top_left_y_coordinate+180+i*30))#Drawing the textures

#Drawing the playing windows using the given grid, 
def draw_playing_window(win,grid):
    #Displaying the background
    win.blit(background,(0,0))
    #Drawing the boundary of the playing window on top of the backgroung
    pygame.draw.rect(win,(255,0,0), (top_left_x_coordinate-5,  top_left_y_coordinate-5, playing_window_width+10, playing_window_height+10), 5)
    for i in range(no_of_ver_boxes):
        for j in range(no_of_hor_boxes):
            if(grid[i][j][0]=="OCCUPIED"):
                #Drawing the blocks on top of the background, only if that block has a texture(occupied)
                win.blit(grid[i][j][1],(top_left_x_coordinate + j*block_size ,  top_left_y_coordinate + i*block_size))

#Function to display the score
def display_score(score,position, win):
    '''Displays a number on that tile'''
    font = pygame.font.SysFont('arial', 50)
    text = font.render("Score : "+str(score), 1, (255, 255, 0))
    win.blit(text, position)

#function to quit the game
def quitgame(win):
    pygame.quit()
    pygame.display.quit()
    exit()

#This is the main function of our game
#It handles all the events, calls other function to run the game
def gameplay(win):
    global counter_t_menu
    global score
    global gameover
    #Channel 0 -> For Playing music on main page
    #Channel 1 -> For playing music when there is a game over
    #Channel 2 -> For playing music when we have to clear a row
    #Channel 3 -> For playing music at various levels
    pygame.mixer.Channel(0).stop()      
    pygame.mixer.Channel(1).stop()      
    pygame.mixer.Channel(3).play(music_first_level, loops = -1)     #Playing music for 1st level
    locked_postions = {}        #Initally the locked position is empty
    grid = create_grid(locked_postions)

    #control variables
    run = True
    change_piece = False        #to know is new Shape to be generated or not
    curr_shape = get_new_shape()     # Genrating current shape
    next_shape = get_new_shape()        # Generating next shape

    #Ensure no two consecutive blocks have same texture
    if(next_shape.color==curr_shape.color):
        next_shape.color = shape_colors[(shape_colors.index(curr_shape.color) + 1 ) % len(shape_colors)]
    next_to_next_shape = get_new_shape()
    if(next_to_next_shape.color==next_shape.color):
        next_to_next_shape.color = shape_colors[(shape_colors.index(next_shape.color) + 1 ) % len(shape_colors)]

    #game clock for discrete movement of the blocks
    clock = pygame.time.Clock()
    delay = 0.8 #delay in falling of block , i.e speed  = 1/delay, increase delay if you want the blocks to fall slowly
    falling_time = 0
    score=0
    temp_score=score
    #variable to decide the difficulty level based on score
    flag_less_than_500 = True   #Easy Level
    flag_betw_500_1000 = True   #Medium Level
    flag_more_than_500 = True   #Hard Level
    while run:
        #Deciding delay, and music for first level
        if score<500 and flag_less_than_500:    
            pygame.mixer.Channel(3).play(music_first_level, loops = -1)
            delay = 0.5
            flag_less_than_500 = False
        #Deciding delay, and music for second level
        if score>=500 and score<1000 and flag_betw_500_1000:
            pygame.mixer.Channel(3).play(music_second_level, loops = -1)
            delay = 0.35
            flag_betw_500_1000 = False
        #Deciding delay, and music for last level
        if score>=1000 and flag_more_than_500:
            pygame.mixer.Channel(3).play(music_last_level, loops = -1)
            delay = 0.2
            flag_more_than_500 = False
        
        #initializing the grid
        grid = create_grid(locked_postions)

        #getting clok time to decide whether or not to descend the block
        falling_time += clock.get_rawtime()
        clock.tick()

        if falling_time/1000 > delay:
            falling_time = 0
            curr_shape.y += 1
            if not (check_validity(curr_shape,grid)) and curr_shape.y > 0: #checking if the descending block hits an obstacle or the floor
                curr_shape.y += -1
                change_piece = True

        #Handling event during the gameplay
        for events in pygame.event.get(): 

            if events.type == pygame.KEYDOWN:       #this checks if any key from the keyboard is pressed or not
                if events.key == pygame.K_ESCAPE:   #this checks if ESCAPE KEY is being pressed
                    pause_menu(win)                 #pause the game is ESCAPE KEY is pressed

                if events.key == pygame.K_RIGHT:    #this checks if RIGHT KEY is being pressed
                    curr_shape.x += 1               #move the block rightwards if RIGHT KEY is pressed
                    if not (check_validity(curr_shape,grid)):  #Handle boundary conditions
                        curr_shape.x -= 1
                
                if events.key == pygame.K_LEFT:     #this checks if LEFT KEY is being pressed
                    curr_shape.x -= 1               #move the block leftwards if LEFT KEY is pressed
                    if not (check_validity(curr_shape,grid)):  #Handle boundary conditions
                        curr_shape.x += 1

                if events.key == pygame.K_UP:       #this checks if UP ARROW KEY is being pressed
                    curr_shape.rotation = (curr_shape.rotation + 1) % len(curr_shape.shape)     #change the roation if UP ARROW KEY is pressed
                    if not check_validity(curr_shape, grid):   #Handle clashes with obstacles while rotating
                        curr_shape.rotation-=1

                if events.key == pygame.K_DOWN:     #this checks si DOWN ARROW KEY is being pressed
                    curr_shape.y += 1               #bring the block 1 step downwards, i.e. soft drop if DOWN ARROW KEY is pressed
                    score += 1
                    if not (check_validity(curr_shape,grid)):  #Handling the clashes with obstacles
                        curr_shape.y -= 1
                        score -=1
                
                if events.key == pygame.K_SPACE:    #this check if the SPACE KEY is being pressed
                    score+=10                       #incrementing the score at hard drop
                    while check_validity(curr_shape,grid): #Handling the clashes with obstacles
                        curr_shape.y += 1
                    curr_shape.y += -1
                    change_piece = True             #change chiece to True since after hard drop new Shape is going to arrive

            if events.type == pygame.QUIT:          #this check if close button at top right is being pressed
                run = False                         #stop the program if close button is pressed
                break

        shape_pos = convert_shape_to_index(curr_shape)    #converting shape to index positions
        
        #this manages the projection of a block below, where the block is going to fall
        #we are creating new block while descending at each iterationg until it hit an obstacle or the floor
        #------------------------------------------
        y_temp = curr_shape.y + 1
        while True: 
            new_piece = Shape(curr_shape.x,y_temp,curr_shape.shape)
            new_piece.rotation = curr_shape.rotation
            if not check_validity(new_piece,grid):
                break
            y_temp+=1
        y_temp -= 1
        #y_temp notes the y coordinates of the projected block
        #----------------------------------------------

        #updating the grid with the current falling block
        for i in range(len(shape_pos)):
            x,y = shape_pos[i]
            if y>-1:
                grid[y][x] = ("OCCUPIED",curr_shape.color)  #update with current block, with its texture

        #checks if new Shape is to be generated, change_piece is true only when last block has fallen.
        if change_piece:
            for pos in shape_pos:
                p = (pos[0],pos[1])
                locked_postions[p] = curr_shape.color #updating locked positions, adding the current block to the locked position when it has fallen
            curr_shape = next_shape             #updating current shape to next shape
            next_shape = next_to_next_shape     #updating next shape to next to next shape
            next_to_next_shape = get_new_shape()    #generating a new next to next shape

            #Ensuring that no two consecutive shapes are of same texture
            if(next_to_next_shape.color==next_shape.color):
                next_to_next_shape.color = shape_colors[(shape_colors.index(next_shape.color) + 1 ) % len(shape_colors)]
            change_piece = False
            locked_positions,inc=clear_rows(grid , locked_postions)
            score += 30*inc             #score increases according to no. of rows disappear
            score += 10                 #Current Shape has fallen so, new score increments
        #Drawing the graphics based on the grid, overwriting on them
        draw_playing_window(win, grid)  
        draw_next_shape(next_shape, next_to_next_shape, win)
        display_score(score,(top_left_x_coordinate+playing_window_width+50,top_left_y_coordinate+playing_window_height/2+50), win)
        button_pause(screen_width-300,screen_height-200,150,150,"PAUSE", win,pause_menu)  #displaying pause button
        #Managing the projected blocks
        #----------------------------------
        current_piece_temp = curr_shape.shape[curr_shape.rotation]
        for i in range(5):
            for j in range(5):
                if current_piece_temp[i][j] == 'O' and (curr_shape.x-2+j,y_temp-4+i) not in shape_pos:
                    win.blit(projected,(top_left_x_coordinate+(curr_shape.x-2+j)*30 ,  top_left_y_coordinate+(y_temp-4+i)*30)) #display the projected block on top of the blocks
        #----------------------------------
        pygame.display.update()
        if is_losing(locked_postions): #Check if there is a game over
            gameover=True
            counter_t_menu = "GAME OVER DISPLAY"
            game_over(win)
            pygame.display.update()        #Updating the window
            run = False

# function for the pause button
def button_pause(pos_x,pos_y, width, height, message, win, task=None):
    mouse_pos=pygame.mouse.get_pos() #to store the position of the cursor in the screen in the form of (x_coordinate, y_coordinate)
    mouse_click=pygame.mouse.get_pressed() # to detect the click of the mouse button. 
    #It store the which of the buttons are pressed in the form of an array of binary values.  
    # 0 if the button is not pressed and 1 if the button is not pressed

    # Checks if the positon of the cursor lies inside the button size  
    if pos_x<mouse_pos[0]<pos_x+width and pos_y<mouse_pos[1]<pos_y+height :
        # to display the picture of the pause button in the screen
        win.blit(buttonpause,(pos_x,pos_y-10))
        # If the mouse button is pressed then perform the task
        if mouse_click[0]==1 and task!=None :
            task(win)
    win.blit(buttonpause,(pos_x,pos_y-10)) #display the button in the screen

def draw_text(text, size, color, win,position):
    pygame.font.init() # initialising the font component of pygame
    font = pygame.font.SysFont('comicsansms', size , bold= True) # initialising the font style, size and the type
    label = font.render(text, 1, color) #rendering the font to display the font
    label_rect=label.get_rect() # to return the image of the font in rectangle shape
    label_rect.center=(position) # to set the position of the returned image above in the display screen
    win.blit(label, label_rect) #to display the text finally on the screen 

# button method to create button and define their functionalities
def button(pos_x,pos_y, width, height, message, win, task=None,txtsz=0, come="None", gover = False):
    #using global variable
    global counter_t_menu
    mouse_pos=pygame.mouse.get_pos() #to store the position of the cursor in the screen in the form of (x_coordinate, y_coordinate)
    mouse_click=pygame.mouse.get_pressed() # to detect the click of the mouse button. 
    #It store the which of the buttons are pressed in the form of an array of binary values.  
    # 0 if the button is not pressed and 1 if the button is not pressed

    # Checks if the positon of the cursor lies inside the button size  
    if pos_x<mouse_pos[0]<pos_x+width and pos_y<mouse_pos[1]<pos_y+height:
        win.blit(button_active,(pos_x,pos_y-10)) # To change the picture of the button in case of hovering over it
        if come == "EXIT":
            event = pygame.event.wait()
            if (event.type == pygame.MOUSEBUTTONUP):
                if task!=None :
                    task(win)
        if come == "PAUSE MENU":
            counter_t_menu = "FROM PAUSE"
            event = pygame.event.wait()
            if (event.type == pygame.MOUSEBUTTONUP):
                if task!=None :
                    task(win)
        elif counter_t_menu == "FROM PAUSE":
            counter_t_menu = "NEW PAUSE"
            pass
        else:
            if come == "GOVER" and counter_t_menu == "GAME OVER DISPLAY":
                pass   
            else:
                event = pygame.event.wait()
                if (event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEBUTTONDOWN):
                    if task!=None :
                        task(win)

    else:
        win.blit(button_inactive,(pos_x,pos_y-10))
    draw_text(message,txtsz,(255,255,255),win,(pos_x+width/2,pos_y+height/2))

# function to unpause the game
def unpause(win):
    global pause
    pause=False

# function for pause gameplay
def pause_menu(win):
    #using the global variables
    global pause
    global counter_t_menu
    #initialising the pause valriable to zero
    pause=True

    #loop to display the pause screen
    while pause:
        #displaying the background image
        win.blit(background,(0,0))

        #displaying the text "GAME PAUSED" in the screen using draw_text function created above
        draw_text("GAME PAUSED",70,(255,255,0),win,(screen_width/2,screen_height/2-100))

        #displaying the buttons on the pause menu screen
        button(screen_width/2-100,screen_height/2,200,50,"RESUME",win,unpause, 35, come = "PAUSE MENU")
        counter_t_menu = "FROM PAUSE"
        button(screen_width/2-100,screen_height/2+100,200,50,"MAIN MENU",win,game_menu, 25, come = "PAUSE MENU")
        button(screen_width/2-100,screen_height/2+200,200,50,"EXIT",win,quitgame, 25, come = "EXIT")       
        pygame.display.update()     # updating the pygame window
        if counter_t_menu == "NEW PAUSE":
            counter_t_menu = ""
        for event in pygame.event.get():
            if event.type==pygame.QUIT:     # if the close button is pressed in the window then the game closes
                pygame.quit()
                pygame.display.quit()
                quit()
                break

# function for game over
def game_over(win):
    #using the global variables
    global counter_t_menu
    global gameover

    #ensuring that only the game over music is only played here
    pygame.mixer.Channel(1).play(music_game_over,loops=-1)
    pygame.mixer.Channel(3).stop()
    pygame.mixer.Channel(0).stop()
    
    #initialising the gameover to zero
    gameover=True

    #initialising strval to display in the game over menu
    strval="YOUR SCORE:"+str(score)

    #loop to display the gameover screen
    while gameover:
        #displaying the background image
        win.blit(background,(0,0))

        #displaying the text "GAME OVER" in the screen using draw_text function created above
        draw_text("GAME OVER :(",70,(255,255,0),win,(screen_width/2,screen_height/2-170))
        #displaying the text strval in the screen using draw_text function created above
        draw_text(strval,50,(255,255,0),win,(screen_width/2,screen_height/2-80))

        #displaying the buttons on the game over screen
        button(screen_width/2-100,screen_height/2,200,50,"PLAY AGAIN",win,gameplay, 25, come = "GOVER", gover = True)
        counter_t_menu = "FROM PAUSE"
        button(screen_width/2-100,screen_height/2+100,200,50,"MAIN MENU", win, game_menu, 25,come = "PAUSE MENU", gover = True)
        button(screen_width/2-100,screen_height/2+200,200,50,"EXIT", win,quitgame, 20, come = "EXIT")       
        pygame.display.update()         # updating the pygame window
        counter_t_menu = ""
        for event in pygame.event.get():
            if event.type==pygame.QUIT:     # if the close button is pressed in the window then the game closes
                pygame.quit()
                pygame.display.quit()
                quit()
                break 

# function for the controls menu
def controls(win):
    #using the global variables
    global control

    #initialising the control variable to True to ensure that the main menu is displayed 
    control=True

    #loop for the control menu
    while(control):

        # displaying the control image 
        win.blit(control_img,(0,0),(0,0, win.get_width(), win.get_height()))
        counter_t_menu = "CONTROLS"

        #back button to go back to the main menu from controls option
        button(10,10,200,50,"Back", win,game_menu,25, come = "CONTROLS")
        pygame.display.update()         # updating the background
        for event in pygame.event.get():
            if event.type==pygame.QUIT:     # if the close button is pressed in the window then the game closes
                pygame.quit()
                pygame.display.quit()
                quit()
                break

# function for the main menu 
def game_menu(win):
    #using the global variables
    global menu  
    global score
    global counter_t_menu
    #ensuring that only the main menu music is only played here
    pygame.mixer.Channel(1).stop()
    pygame.mixer.stop()
    pygame.mixer.Channel(0).play(music_main_page, loops=-1)
    #initialising the score to zero
    score=0
    #initialising the menu variable to True to ensure that the main menu is displayed 
    menu=True
    #loop for game menu
    while menu:
        win.blit(background,(0,0))  # displaying the background
        draw_text("Welcome to Tetris",100,(255,255,0),win,(screen_width/2,screen_height/2-100))   #displaying "welcome to tetris" in the main menu by calling the function draw_text
        button(screen_width/2-100,screen_height/2,200,50,"PLAY", win,gameplay,35, come = "MAIN MENU")  #calling button function to make the "Play" button in the main menu 
        button(screen_width/2-100,screen_height/2+100,200,50,"CONTROLS", win,controls,25, come = "MAIN MENU") #calling button function to make the "Controls" button in the main menu
        button(screen_width/2-100,screen_height/2+200,200,50,"EXIT", win,quitgame, 25,come = "EXIT")  #calling button function to make the "EXIT" button in the main menu    
        pygame.display.update()     #updating the pygame window
        event = pygame.event.wait()
        if event.type == pygame.QUIT:   #listening the close button of the window
            pygame.quit()               #stop the game once the close button is pressed
            pygame.display.quit()
            quit()
            break
                
    pygame.display.quit()           #quit the pygame display
    
win = pygame.display.set_mode((screen_width,screen_height))       #initializing a window for the game

pygame.display.set_caption('Tetris')        
counter_t_menu = ""
game_menu(win)      #calling the game menu