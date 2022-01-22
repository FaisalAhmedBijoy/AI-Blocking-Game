# MODULES
import pygame, sys
import numpy as np

# initializes pygame
pygame.init()

# ---------
# CONSTANTS
# ---------
WIDTH = 800
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
pygame.display.set_caption( 'Blocking Game' )
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

def is_board_full():
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			if board[row][col] == 0:
				return False

	return True

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



def bestMove(player = 2):
	bestScore = -100000
	move = None

	global playerTwoCurrentCol
	global playerTwoCurrentRow




	if(player == 1):
		currentRow = playerOneCurrentRow
		currentCol = playerOneCurrentCol
	else:
		currentRow = playerTwoCurrentRow
		currentCol = playerTwoCurrentCol


	if(currentRow == -1 or currentCol == -1):
		for row in range(BOARD_ROWS):
			for col in range(BOARD_COLS):
				if(board[row][col] == 0):
					board[row][col] = 2
					score = minimax(board,2,playerOneCurrentRow,playerOneCurrentCol,row,col,0,False)
					board[row][col] = 0

					if(score>bestScore):
						bestScore = score
						move = (row,col)

	if(-1 < currentRow-2 and currentRow-2 < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and board[currentRow-2][currentCol-1] == 0 ):
		board[currentRow-2][currentCol-1] = 2
		score = minimax(board,2,playerOneCurrentRow,playerOneCurrentCol,currentRow-2 , currentCol-1,0,False)
		board[currentRow-2][currentCol-1] = 0

		if(score>bestScore):
			bestScore = score
			move = (currentRow-2 , currentCol-1)

	if(-1 < currentRow-2 and currentRow-2 < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and board[currentRow-2][currentCol+1] == 0 ):
		board[currentRow-2][currentCol+1] = 2
		score = minimax(board,2,playerOneCurrentRow,playerOneCurrentCol,currentRow-2,currentCol+1,0,False)
		board[currentRow-2][currentCol+1] = 0

		if(score>bestScore):
			bestScore = score
			move = (currentRow-2,currentCol+1)

	if(-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol-2 and currentCol-2 < BOARD_COLS and board[currentRow-1][currentCol-2] == 0 ):
		board[currentRow-1][currentCol-2] = 2
		score = minimax(board,2,playerOneCurrentRow,playerOneCurrentCol,currentRow-1,currentCol-2,0,False)
		board[currentRow-1][currentCol-2] = 0

		if(score>bestScore):
			bestScore = score
			move = (currentRow-1,currentCol-2)

	if(-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol+2 and currentCol+2 < BOARD_COLS and board[currentRow-1][currentCol+2] == 0 ):
		board[currentRow-1][currentCol+2] = 2
		score = minimax(board,2,playerOneCurrentRow,playerOneCurrentCol,currentRow-1,currentCol+2,0,False)
		board[currentRow-1][currentCol+2] = 0

		if(score>bestScore):
			bestScore = score
			move = (currentRow-1,currentCol+2)

	if(-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol-2 and currentCol-2 < BOARD_COLS and board[currentRow+1][currentCol-2] == 0 ):
		board[currentRow+1][currentCol-2] = 2
		score = minimax(board,2,playerOneCurrentRow,playerOneCurrentCol,currentRow+1,currentCol-2,0,False)
		board[currentRow+1][currentCol-2] = 0

		if(score>bestScore):
			bestScore = score
			move = (currentRow+1,currentCol-2)

	if(-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol+2 and currentCol+2 < BOARD_COLS and board[currentRow+1][currentCol+2] == 0 ):
		board[currentRow+1][currentCol+2] = 2
		score = minimax(board,2,playerOneCurrentRow,playerOneCurrentCol,currentRow+1,currentCol+2,0,False)
		board[currentRow+1][currentCol+2] = 0

		if(score>bestScore):
			bestScore = score
			move = (currentRow+1,currentCol+2)

	if(-1 < currentRow+2 and currentRow+2 < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and board[currentRow+2][currentCol-1] == 0 ):
		board[currentRow+2][currentCol-1] = 2
		score = minimax(board,2,playerOneCurrentRow,playerOneCurrentCol,currentRow+2,currentCol-1,0,False)
		board[currentRow+2][currentCol-1] = 0

		if(score>bestScore):
			bestScore = score
			move = (currentRow+2,currentCol-1)

	if(-1 < currentRow+2 and currentRow+2 < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and board[currentRow+2][currentCol+1] == 0 ):
		board[currentRow+2][currentCol+1] = 2
		score = minimax(board,2,playerOneCurrentRow,playerOneCurrentCol,currentRow+2,currentCol+1,0,False)
		board[currentRow+2][currentCol+1] = 0

		if(score>bestScore):
			bestScore = score
			move = (currentRow+2,currentCol+1)
	

	playerTwoCurrentRow = move[0];
	playerTwoCurrentCol = move[1];
	mark_square( move[0], move[1], 2)
	


	
scores = {
  1: -10,
  2: 10,
  0: 0
}

def minimax(board, player, playerOneCurrentRow, playerOneCurrentCol, playerTwoCurrentRow, playerTwoCurrentCol , depth, isMaximizing):
	result = player if check_lose(player) else 0
	if result is not None:
		return scores[result]


	if(player == 1):
		currentRow = playerOneCurrentRow
		currentCol = playerOneCurrentCol
	else:
		currentRow = playerTwoCurrentRow
		currentCol = playerTwoCurrentCol
	
	if isMaximizing:
		bestScore = -100000


		if(-1 < currentRow-2 and currentRow-2 < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and board[currentRow-2][currentCol-1] == 0 ):
			board[currentRow-2][currentCol-1] = 2
			score = minimax(board,2,playerOneCurrentRow,playerOneCurrentCol,currentRow-2 , currentCol-1,0,False)
			board[currentRow-2][currentCol-1] = 0

			bestScore = max(score,bestScore)

		if(-1 < currentRow-2 and currentRow-2 < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and board[currentRow-2][currentCol+1] == 0 ):
			board[currentRow-2][currentCol+1] = 2
			score = minimax(board,2,playerOneCurrentRow,playerOneCurrentCol,currentRow-2,currentCol+1,0,False)
			board[currentRow-2][currentCol+1] = 0

			bestScore = max(score,bestScore)

		if(-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol-2 and currentCol-2 < BOARD_COLS and board[currentRow-1][currentCol-2] == 0 ):
			board[currentRow-1][currentCol-2] = 2
			score = minimax(board,2,playerOneCurrentRow,playerOneCurrentCol,currentRow-1,currentCol-2,0,False)
			board[currentRow-1][currentCol-2] = 0

			bestScore = max(score,bestScore)

		if(-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol+2 and currentCol+2 < BOARD_COLS and board[currentRow-1][currentCol+2] == 0 ):
			board[currentRow-1][currentCol+2] = 2
			score = minimax(board,2,playerOneCurrentRow,playerOneCurrentCol,currentRow-1,currentCol+2,0,False)
			board[currentRow-1][currentCol+2] = 0

			bestScore = max(score,bestScore)

		if(-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol-2 and currentCol-2 < BOARD_COLS and board[currentRow+1][currentCol-2] == 0 ):
			board[currentRow+1][currentCol-2] = 2
			score = minimax(board,2,playerOneCurrentRow,playerOneCurrentCol,currentRow+1,currentCol-2,0,False)
			board[currentRow+1][currentCol-2] = 0

			bestScore = max(score,bestScore)

		if(-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol+2 and currentCol+2 < BOARD_COLS and board[currentRow+1][currentCol+2] == 0 ):
			board[currentRow+1][currentCol+2] = 2
			score = minimax(board,2,playerOneCurrentRow,playerOneCurrentCol,currentRow+1,currentCol+2,0,False)
			board[currentRow+1][currentCol+2] = 0

			bestScore = max(score,bestScore)

		if(-1 < currentRow+2 and currentRow+2 < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and board[currentRow+2][currentCol-1] == 0 ):
			board[currentRow+2][currentCol-1] = 2
			score = minimax(board,2,playerOneCurrentRow,playerOneCurrentCol,currentRow+2,currentCol-1,0,False)
			board[currentRow+2][currentCol-1] = 0

			bestScore = max(score,bestScore)

		if(-1 < currentRow+2 and currentRow+2 < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and board[currentRow+2][currentCol+1] == 0 ):
			board[currentRow+2][currentCol+1] = 2
			score = minimax(board,2,playerOneCurrentRow,playerOneCurrentCol,currentRow+2,currentCol+1,0,False)
			board[currentRow+2][currentCol+1] = 0

			bestScore = max(score,bestScore)
		
		return bestScore

	else:
		bestScore = 100000

		if(-1 < currentRow-2 and currentRow-2 < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and board[currentRow-2][currentCol-1] == 0 ):
			board[currentRow-2][currentCol-1] = 1
			score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow-2 , currentCol-1,0,True)
			board[currentRow-2][currentCol-1] = 0

			bestScore = min(score,bestScore)

		if(-1 < currentRow-2 and currentRow-2 < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and board[currentRow-2][currentCol+1] == 0 ):
			board[currentRow-2][currentCol+1] = 1
			score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow-2,currentCol+1,0,True)
			board[currentRow-2][currentCol+1] = 0

			bestScore = min(score,bestScore)

		if(-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol-2 and currentCol-2 < BOARD_COLS and board[currentRow-1][currentCol-2] == 0 ):
			board[currentRow-1][currentCol-2] = 1
			score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow-1,currentCol-2,0,True)
			board[currentRow-1][currentCol-2] = 0

			bestScore = min(score,bestScore)

		if(-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol+2 and currentCol+2 < BOARD_COLS and board[currentRow-1][currentCol+2] == 0 ):
			board[currentRow-1][currentCol+2] = 1
			score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow-1,currentCol+2,0,True)
			board[currentRow-1][currentCol+2] = 0

			bestScore = min(score,bestScore)

		if(-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol-2 and currentCol-2 < BOARD_COLS and board[currentRow+1][currentCol-2] == 0 ):
			board[currentRow+1][currentCol-2] = 1
			score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow+1,currentCol-2,0,True)
			board[currentRow+1][currentCol-2] = 0

			bestScore = min(score,bestScore)

		if(-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol+2 and currentCol+2 < BOARD_COLS and board[currentRow+1][currentCol+2] == 0 ):
			board[currentRow+1][currentCol+2] = 1
			score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow+1,currentCol+2,0,True)
			board[currentRow+1][currentCol+2] = 0

			bestScore = min(score,bestScore)

		if(-1 < currentRow+2 and currentRow+2 < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and board[currentRow+2][currentCol-1] == 0 ):
			board[currentRow+2][currentCol-1] = 1
			score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow+2,currentCol-1,0,True)
			board[currentRow+2][currentCol-1] = 0

			bestScore = min(score,bestScore)

		if(-1 < currentRow+2 and currentRow+2 < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and board[currentRow+2][currentCol+1] == 0 ):
			board[currentRow+2][currentCol+1] = 1
			score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow+2,currentCol+1,0,True)
			board[currentRow+2][currentCol+1] = 0

			bestScore = min(score,bestScore)

		
		return bestScore




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

			if available_square( clicked_row, clicked_col, 1 ):
				player = 1
				mark_square( clicked_row, clicked_col, player )

				playerOneCurrentRow = clicked_row;
				playerOneCurrentCol = clicked_col;
				print('Player One Current Row and Col: (',str(playerOneCurrentRow)+','+str(playerOneCurrentCol)+')')


				if check_lose( 2 ):
					losePlayer = 2
					game_over = True

					draw_figures()

				else:
					player = 2
					bestMove(player)

					if check_lose( 1 ):
						losePlayer = 1
						game_over = True
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
				losePlayer = 0
				playerOneCurrentRow = -1;
				playerOneCurrentCol = -1;
				playerTwoCurrentRow = -1;
				playerTwoCurrentCol = -1;
            
			elif event.key == pygame.K_q:
				pygame.display.quit()

	pygame.display.update()

