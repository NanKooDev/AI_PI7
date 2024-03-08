import pygame
import pygame.freetype
import constants

class Game():
    def __init__(self):
        """
        Initialize the game board and other game variables.
        """
        #make a 2 dimensional array of 6 rows and 6 columns
        self.board = [[0 for x in range(constants.ROWS)] for y in range(constants.ROWS)] #0 is empty, 1 is player 1, 2 is player 2, 3 is destroyed
        self.turn = 1
        self.winner = 0
        self.moves = 0
        
    def is_move_valid(self, player_x, player_y, dest_x, dest_y):
        """
        Check if a move is valid.

        Parameters:
        - player_x (int): x-coordinate of the current player's position
        - player_y (int): y-coordinate of the current player's position
        - dest_x (int): x-coordinate of the destination position
        - dest_y (int): y-coordinate of the destination position

        Returns:
        - bool: True if the move is valid, False otherwise
        """
        #check if destination is empty
        if self.board[dest_x][dest_y] != constants.EMPTY:
            return False
        
        #check if destination is in same row or column as player and check if destination is on same diagonal as player
        if (player_x != dest_x and player_y != dest_y) and (abs(player_x - dest_x) != abs(player_y - dest_y)):
                return False
            
        #check if there is another player or destroyed tile between player and destination
        if player_x == dest_x:
            for i in range(min(player_y, dest_y) + 1, max(player_y, dest_y)):
                if self.board[player_x][i] != constants.EMPTY:
                    return False
        elif player_y == dest_y:
            for i in range(min(player_x, dest_x) + 1, max(player_x, dest_x)):
                if self.board[i][player_y] != constants.EMPTY:
                    return False
        else:
            for i in range(1, abs(player_x - dest_x)):
                if self.board[player_x + i * (1 if dest_x > player_x else -1)][player_y + i * (1 if dest_y > player_y else -1)] != constants.EMPTY:
                    return False
        
        return True
    
    def move(self, player_x, player_y, dest_x, dest_y):
        """
        Move the current player to the destination position.

        Parameters:
        - player_x (int): x-coordinate of the current player's position
        - player_y (int): y-coordinate of the current player's position
        - dest_x (int): x-coordinate of the destination position
        - dest_y (int): y-coordinate of the destination position

        Returns:
        - bool: True if the move is successful, False otherwise
        """
        if self.is_move_valid(player_x, player_y, dest_x, dest_y):
            self.board[dest_x][dest_y] = self.turn #destination is now the player
            self.board[player_x][player_y] = constants.DESTROYED #old tile is now destroyed
            self.moves += 1 #increment moves
            self.turn = constants.PLAYER1 if self.turn == constants.PLAYER2 else constants.PLAYER2 #change turn
            return True
        else:
            return False
        
    def getplayer(self):
        """
        Get the current player's position.

        Returns:
        - tuple: (x, y) coordinates of the current player's position
        """
        #return x,y of current player in the grid based on the turn
        for i in range(constants.ROWS):
            for j in range(constants.COLS):
                if self.board[i][j] == self.turn:
                    return i, j
                
    def is_game_over(self):
        """
        Check if the game is over.

        Returns:
        - bool: True if the game is over, False otherwise
        """
        #check if there are no more moves left for the current player
        if len(self.available_moves()) == constants.EMPTY:
            self.winner = constants.PLAYER1 if self.turn == constants.PLAYER2 else constants.PLAYER2
            return True

    def available_moves(self):
        """
        Get a list of available moves for the current player.

        Returns:
        - list: List of available moves as tuples (x, y)
        """
        #return a list of available moves for the current player
        player_x, player_y = self.getplayer()
        moves = []
        for i in range(constants.ROWS):
            for j in range(constants.COLS):
                if self.is_move_valid(player_x, player_y, i, j):
                    moves.append((i, j))
        return moves

    def drawboard(self):
        """
        Draw the game board on the screen.
        """
        #draw grid and alternates colors
        for i in range(constants.ROWS):
            for j in range(constants.COLS):
                if (i + j) % 2 == constants.EMPTY: #alternates colors
                    pygame.draw.rect(screen, constants.ALT_GRAY, (i * constants.SQUARE_SIZE, j * constants.SQUARE_SIZE, constants.SQUARE_SIZE, constants.SQUARE_SIZE))
                else:
                    pygame.draw.rect(screen, constants.GRAY, (i * constants.SQUARE_SIZE, j * constants.SQUARE_SIZE, constants.SQUARE_SIZE, constants.SQUARE_SIZE))
        
        #draw players and destroyed tiles
        for i in range(constants.ROWS):
            for j in range(constants.COLS):
                if self.board[i][j] == constants.PLAYER1:
                    #pygame.draw.rect(screen, constants.RED, (i * 100, j * 100, 100, 100))
                    
                    #draw chess-queen.svg on player 1
                    queen = pygame.image.load(constants.QUEEN)
                    #resize image to cover the entire tile
                    queen = pygame.transform.scale(queen, (constants.QUEEN_SIZE, constants.QUEEN_SIZE))
                    
                    #if current player is player 1, set image to red
                    if self.turn == 1:
                        queen.fill(constants.RED, special_flags=pygame.BLEND_RGB_MAX)
                    
                    screen.blit(queen, (i * constants.SQUARE_SIZE, j * constants.SQUARE_SIZE))
                    
                elif self.board[i][j] == constants.PLAYER2:
                    # pygame.draw.rect(screen, constants.BLUE, (i * 100, j * 100, 100, 100))
                    
                    #draw chess-queen.svg on player 2
                    queen = pygame.image.load(constants.QUEEN)
                    #resize image to cover the entire tile
                    queen = pygame.transform.scale(queen, (constants.QUEEN_SIZE, constants.QUEEN_SIZE))
                    
                    #if current player is player 2, set image to blue, else set to white
                    if self.turn == constants.PLAYER2:
                        queen.fill(constants.BLUE, special_flags=pygame.BLEND_RGB_MAX)
                    else:
                        queen.fill(constants.WHITE, special_flags=pygame.BLEND_RGB_MAX)
                    
                    screen.blit(queen, (i * constants.SQUARE_SIZE, j * constants.SQUARE_SIZE))
                    
                elif self.board[i][j] == constants.DESTROYED:
                    pygame.draw.rect(screen, constants.BLACK, (i * constants.SQUARE_SIZE, j * constants.SQUARE_SIZE, constants.SQUARE_SIZE, constants.SQUARE_SIZE))
                    #draws an X on destroyed tiles
                    pygame.draw.line(screen, constants.RED, (i * constants.SQUARE_SIZE, j * constants.SQUARE_SIZE), (i * constants.SQUARE_SIZE + constants.SQUARE_SIZE, j * constants.SQUARE_SIZE + constants.SQUARE_SIZE), 5)
                    pygame.draw.line(screen, constants.RED, (i * constants.SQUARE_SIZE + constants.SQUARE_SIZE, j * constants.SQUARE_SIZE), (i * constants.SQUARE_SIZE, j * constants.SQUARE_SIZE + constants.SQUARE_SIZE), 5)
                    
                    
        #draws circle over active player
        # player_x, player_y = self.getplayer()
        # pygame.draw.circle(screen, constants.WHITE, (player_x * 100 + 50, player_y * 100 + 50), 40, 5)
        
        #draws available moves for the current player with a semi-transparent green color
        for move in self.available_moves():
            i, j = move
            if (i + j) % 2 == constants.EMPTY:
                pygame.draw.rect(screen, constants.SEMI_GREEN_ALT_GRAY, (i * constants.SQUARE_SIZE, j * constants.SQUARE_SIZE, constants.SQUARE_SIZE, constants.SQUARE_SIZE))
            else:
                pygame.draw.rect(screen, constants.SEMI_GREEN_GRAY, (i * constants.SQUARE_SIZE, j * constants.SQUARE_SIZE, constants.SQUARE_SIZE, constants.SQUARE_SIZE))

pygame.init()
pygame.display.set_caption("Isolation Game")
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
clock = pygame.time.Clock()
running = True

game = Game()

game.board[0][0] = constants.PLAYER1
game.board[5][5] = constants.PLAYER2

while running:
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # RENDER YOUR GAME HERE
    game.drawboard()
    
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            player_x, player_y = game.getplayer()
            dest_x, dest_y = x // constants.SQUARE_SIZE, y // constants.SQUARE_SIZE
            if game.move(player_x, player_y, dest_x, dest_y):
                if game.is_game_over():
                    
                    game.drawboard()
                    
                    #draw winner text on screen
                    GAME_FONT = pygame.freetype.SysFont("Arial", 50)
                    text_surface, rect = GAME_FONT.render(f"Black wins!" if game.winner == constants.PLAYER1 else "White wins!", constants.WHITE)
                    GAME_FONT.render_to(screen, (constants.WIDTH//2 - rect.width//2, constants.HEIGHT//2 - rect.height//2), f"Black wins!" if game.winner == constants.PLAYER1 else "White wins!", constants.WHITE)
                    
                    running = False

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(constants.FPS)  # limits FPS to 60

#sleep for 3 seconds before quitting
pygame.time.wait(3000)
pygame.quit()