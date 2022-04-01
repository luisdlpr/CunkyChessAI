""""
Credits to original developer Aryan9301 - https://github.com/Aryan9301/ChessGame
'This is our main driver file. It will be responsible for handling user input and displaying the current GameState object.'

Rules and bugfixes implemented by luisdlpr. 01.04.22
"""
import pygame_textinput as pytxt
import pygame as p
import ChessEngine
import chess

p.init()
WIDTH = HEIGHT = 512
#400 is another great option

DIMENSION = 8
#Dimentions of a chess board are 8x8

SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 30
#For animations later on

IMAGES = {}
'''
Initialize a global dictionary of images. This will be called exactly once in the main
'''
def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    #Note: we can access an image by saying 'IMAGES['wp']'

'''
The main driver for our code. This will handle user input and updating the graphics
'''
def main():
    p.init()

    ### Generate GUI ###
    # Set Font
    fontsize = 40
    font = p.font.Font("ARCADECLASSIC.TTF", fontsize)
    # pytxt text manager - set max length
    manager = pytxt.TextInputManager(validator = lambda input: len(input) <= 16)
    # define text field and link manager and font
    textinput = pytxt.TextInputVisualizer(manager=manager, font_object=font)
    # generate screen and refresh clock
    screen = p.display.set_mode((WIDTH, HEIGHT + 200))
    p.display.set_caption('CunkyChess')
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    loadImages()

    # constant messages to display
    instructor = font.render('Enter Command', False, (0, 0, 0))
    findcommands = font.render('H  for  a  list  of  commands', False, (0, 0, 0))


    # define commands
    commands = {
        'quit': 'q',
        'move': 'm',
        'undo': 'z',
        'help': '?'
    }

    running = True
    sqSelected = () #no square is selected, keep track of the last click of the user (tuple: (row, col))
    playerClicks = [] #keep track of player clicks (two tuples: [(6, 4), (4, 4)])
    
    while running:
        # gs.makeMove(move)
        # p.draw
        # Fill background
        screen.fill(p.Color("white"), (0, HEIGHT, WIDTH, 200))
    
        events = p.event.get()
        textinput.update(events)

        # text input screen placement
        screen.blit(instructor,(10, HEIGHT + 10))
        screen.blit(textinput.surface, (10, HEIGHT + 20 + fontsize))
        screen.blit(findcommands,(10, HEIGHT + 30 + 2*fontsize))


        for e in events:
            if e.type == p.QUIT:
                running = False
            ## Method to access user input.
            elif e.type == p.KEYDOWN and e.key == p.K_RETURN:
                print(f"User pressed enter! Input so far: {textinput.value}")
            # mouse handler

            # elif e.type == p.MOUSEBUTTONDOWN:
            #     location = p.mouse.get_pos() #(x, y) location of mouse
            #     col = location[0]//SQ_SIZE
            #     row = location[1]//SQ_SIZE
            #     if sqSelected == (row, col): #user clicked the same square twice
            #         sqSelected = () #deselect
            #         playerClicks = [] #clear player clicks
            #     else:
            #         sqSelected = (row, col)
            #         playerClicks.append(sqSelected) #append for both 1st and 2nd clicks
            #     if len(playerClicks) == 2: #after 2nd click
            #         move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
            #         print(move.getChessNotation())
            #         gs.makeMove(move)
            #         sqSelected = () #reset user clicks
            #         playerClicks = []

            #key handlers
            # elif e.type == p.KEYDOWN:
            #     if e.key == p.K_z: #undo when 'z' is pressed
            #         gs.undoMove()
        
        # update display
        drawGameState(screen, gs)
        p.display.update()
        clock.tick(MAX_FPS)
        # p.display.flip()


def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": #not empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()