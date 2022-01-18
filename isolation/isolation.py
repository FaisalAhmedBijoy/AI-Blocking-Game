# MODULES
import pygame, sys
import numpy as np

# initializes pygame
pygame.init()

# ---------
# CONSTANTS
# ---------
WIDTH = 600
HEIGHT = WIDTH
LINE_WIDTH = 15
WIN_LINE_WIDTH = 15
BOARD_ROWS = 5
BOARD_COLS = BOARD_ROWS
SQUARE_SIZE = WIDTH/BOARD_ROWS
CIRCLE_RADIUS = SQUARE_SIZE/3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE/4
# rgb: red green blue
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

# ---------
# VARIABLES
# ---------
player = 1
game_over = False
losePlayer = 0

# ------
# SCREEN
# ------
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption( 'Isolation' )
screen.fill( BG_COLOR )

# -------------
# CONSOLE BOARD
# -------------
board = np.zeros( (BOARD_ROWS, BOARD_COLS) )


#-------------
# Player Current Possition
#-------------
playerOneCurrentRow = -1;
playerOneCurrentCol = -1;
playerTwoCurrentRow = -1;
playerTwoCurrentCol = -1;


# ---------
# FUNCTIONS
# ---------
def draw_lines():

	for i in range(1,BOARD_ROWS):
		# horizontal
		pygame.draw.line( screen, LINE_COLOR, (0, SQUARE_SIZE*i), (WIDTH, SQUARE_SIZE*i), LINE_WIDTH )

	for i in range(1,BOARD_COLS):
		# vertical
		pygame.draw.line( screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH )


def draw_figures():
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			if board[row][col] == 1:
				color = RED if (row == playerOneCurrentRow and col == playerOneCurrentCol and losePlayer == 1 ) else GREEN if (row == playerOneCurrentRow and col == playerOneCurrentCol) else  CIRCLE_COLOR
				pygame.draw.circle( screen, color, (int( col * SQUARE_SIZE + SQUARE_SIZE//2 ), int( row * SQUARE_SIZE + SQUARE_SIZE//2 )), CIRCLE_RADIUS, CIRCLE_WIDTH )
			elif board[row][col] == 2:
				color = RED if (row == playerTwoCurrentRow and col == playerTwoCurrentCol and losePlayer == 2 ) else GREEN if (row == playerTwoCurrentRow and col == playerTwoCurrentCol) else   CROSS_COLOR
				pygame.draw.line( screen, color , (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH )	
				pygame.draw.line( screen, color , (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH )


def mark_square(row, col, player):
	board[row][col] = player
	print ("----------------------------------------------------")
	print("Player " + str(player) + " marked square : (" + str(row) + "," + str(col) + ")")
	print(board)
	print ("----------------------------------------------------")

def available_square(row, col, player):
	if(player == 1):
		currentRow = playerOneCurrentRow
		currentCol = playerOneCurrentCol
	else:
		currentRow = playerTwoCurrentRow
		currentCol = playerTwoCurrentCol

	return (board[row][col] == 0 and ( 
		(currentRow == -1 and currentCol==-1) or
		(currentRow-2 == row and currentCol-1 == col) or
		(currentRow-2 == row and currentCol+1 == col) or
		(currentRow-1 == row and currentCol-2 == col) or
		(currentRow-1 == row and currentCol+2 == col) or
		(currentRow+1 == row and currentCol-2 == col) or
		(currentRow+1 == row and currentCol+2 == col) or
		(currentRow+2 == row and currentCol-1 == col) or
		(currentRow+2 == row and currentCol+1 == col)
	))				



def check_lose(player):
	if(player == 1):
		currentRow = playerOneCurrentRow
		currentCol = playerOneCurrentCol
	else:
		currentRow = playerTwoCurrentRow
		currentCol = playerTwoCurrentCol


	if(currentRow == -1 or currentCol == -1):
		return False

	return not (
		(-1 < currentRow-2 and currentRow-2 < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and board[currentRow-2][currentCol-1] == 0 ) or
		(-1 < currentRow-2 and currentRow-2 < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and board[currentRow-2][currentCol+1] == 0 ) or
		(-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol-2 and currentCol-2 < BOARD_COLS and board[currentRow-1][currentCol-2] == 0 ) or
		(-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol+2 and currentCol+2 < BOARD_COLS and board[currentRow-1][currentCol+2] == 0 ) or
		(-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol-2 and currentCol-2 < BOARD_COLS and board[currentRow+1][currentCol-2] == 0 ) or
		(-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol+2 and currentCol+2 < BOARD_COLS and board[currentRow+1][currentCol+2] == 0 ) or
		(-1 < currentRow+2 and currentRow+2 < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and board[currentRow+2][currentCol-1] == 0 ) or
		(-1 < currentRow+2 and currentRow+2 < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and board[currentRow+2][currentCol+1] == 0 )
	)

def restart():
	screen.fill( BG_COLOR )
	draw_lines()
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			board[row][col] = 0





draw_lines()

# ---------
# VARIABLES
# ---------
player = 1
game_over = False

# --------
# MAINLOOP
# --------
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEBUTTONDOWN and not game_over:

			mouseX = event.pos[0] # x
			mouseY = event.pos[1] # y

			clicked_row = int(mouseY // SQUARE_SIZE)
			clicked_col = int(mouseX // SQUARE_SIZE)
			
			#print('Mouse X position: ' + str(mouseX))
			#print('Mouse Y position: ' + str(mouseY))
			print('Clicked row: ' + str(clicked_row))
			print('Clicked col: ' + str(clicked_col))

            

			if available_square( clicked_row, clicked_col, player ):

				mark_square( clicked_row, clicked_col, player )
				if(player == 1):
					playerOneCurrentRow = clicked_row;
					playerOneCurrentCol = clicked_col;
				else:
					playerTwoCurrentRow = clicked_row;
					playerTwoCurrentCol = clicked_col;

				print('Player One Current Row and Col: (',str(playerOneCurrentRow)+','+str(playerOneCurrentCol)+')') 
				print('Player Two Current Row and Col: (',str(playerTwoCurrentRow)+','+str(playerTwoCurrentCol)+')') 
				# Switch player
				player = player % 2 + 1
				print("Sign:  0-> Player 1, X-> Player 2")
				print('Player turn:' + str(player))
				

				if check_lose( player ):
					losePlayer = player
					game_over = True
					
					print("\n\n")
					print("********************************************************")
					print('Player ' + str(losePlayer) + ' loses!')
					player = player % 2 + 1
					print("Congratulations ! Player Win: " + str(player))
					print("********************************************************")
					print("Restarting game : Press -> R")
					print("Quit game : Press -> Q")
					print("********************************************************")

				draw_figures()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_r:
				restart()
				player = 1
				game_over = False
            
			elif event.key == pygame.K_q:
				pygame.display.quit()

	pygame.display.update()

