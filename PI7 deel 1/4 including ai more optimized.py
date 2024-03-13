import pygame
import pygame.freetype
import constants

class Game():
    def __init__(self):
        """
        Initialize the game board and other game variables.
        """
        #make a 2 dimensional array of 6 rows and 6 columns
        self.board = [[0 for row in range(constants.ROWS)] for col in range(constants.ROWS)] #0 is empty, 1 is player 1, 2 is player 2, 3 is destroyed
        self.turn = 1
        self.winner = 0
        self.moves = 0
        
    def is_move_valid(self, player_row, player_col, dest_row, dest_col):  #TODO change I and J to row and col
        """
        Check if a move is valid.

        Parameters:
        - player_row (int): row-coordinate of the current player's position
        - player_col (int): y-coordinate of the current player's position
        - dest_row (int): row-coordinate of the destination position
        - dest_col (int): y-coordinate of the destination position

        Returns:
        - bool: True if the move is valid, False otherwise
        """
        #check if destination is empty
        if self.board[dest_row][dest_col] != constants.EMPTY:
            return False
        
        #check if destination is in same row or column as player and check if destination is on same diagonal as player
        if (player_row != dest_row and player_col != dest_col) and (abs(player_row - dest_row) != abs(player_col - dest_col)):
                return False
            
        #check if there is another player or destroyed tile between player and destination
        if player_row == dest_row:
            for i in range(min(player_col, dest_col) + 1, max(player_col, dest_col)):
                if self.board[player_row][i] != constants.EMPTY:
                    return False
        elif player_col == dest_col:
            for i in range(min(player_row, dest_row) + 1, max(player_row, dest_row)):
                if self.board[i][player_col] != constants.EMPTY:
                    return False
        else:
            for i in range(1, abs(player_row - dest_row)):
                if self.board[player_row + i * (1 if dest_row > player_row else -1)][player_col + i * (1 if dest_col > player_col else -1)] != constants.EMPTY:
                    return False
        
        return True
    
    def move(self, player_row, player_col, dest_row, dest_col, simulate_player: int=None):
        """
        Move the current player to the destination position.
        Also switches the turn to the other player. and increments the moves.

        Parameters:
        - player_row (int): row-coordinate of the current player's position
        - player_col (int): y-coordinate of the current player's position
        - dest_row (int): row-coordinate of the destination position
        - dest_col (int): y-coordinate of the destination position

        Returns:
        - bool: True if the move is successful, False otherwise
        """
        if simulate_player and self.is_move_valid(player_row, player_col, dest_row, dest_col):
            self.board[dest_row][dest_col] = simulate_player
            self.board[player_row][player_col] = constants.DESTROYED
            return True
        
        
        elif self.is_move_valid(player_row, player_col, dest_row, dest_col):
            self.board[dest_row][dest_col] = self.turn #destination is now the player
            self.board[player_row][player_col] = constants.DESTROYED #old tile is now destroyed
            self.moves += 1 #increment moves
            self.turn = constants.PLAYER1 if self.turn == constants.PLAYER2 else constants.PLAYER2 #change turn
            return True
        else:
            return False
        
    def getplayer(self, player=None): #TODO change I and J to row and col
        """
        Get the current player's position.

        Returns:
        - tuple: (row, y) coordinates of the current player's position
        """
        #return row,y of current player in the grid based on the turn
        
        #if player is specified, return the position of the specified player
        if player:
            for row in range(constants.ROWS):
                for col in range(constants.COLS):
                    if self.board[row][col] == player:
                        return row, col
        else:
            for row in range(constants.ROWS):
                for col in range(constants.COLS):
                    if self.board[row][col] == self.turn:
                        return row, col
                
    def is_game_over(self, active_player: int=None):
        """
        Check if the game is over.

        Returns:
        - bool: True if the game is over, False otherwise
        """
        #check if there are no more moves left for the current player
        #if active_player is specified, check if there are no more moves left for the specified player
        if active_player:
            if len(self.available_moves(active_player)) == constants.EMPTY:
                self.winner = constants.PLAYER1 if active_player == constants.PLAYER2 else constants.PLAYER2
                return True
            else:
                return False
        
        if len(self.available_moves()) == constants.EMPTY:
            self.winner = constants.PLAYER1 if self.turn == constants.PLAYER2 else constants.PLAYER2
            return True
        
        return False

    def available_moves(self, player=None):
        """
        Get a list of available moves for the current player.

        Returns:
        - list: List of available moves as tuples (row, y)
        """
        #return a list of available moves for the current player
        #if player is specified, return a list of available moves for the specified player
        if player:
            player_row, player_col = self.getplayer(player)
        else:
            player_row, player_col = self.getplayer()
        moves = []
        for dest_row in range(constants.ROWS):
            for dest_col in range(constants.COLS):
                if self.is_move_valid(player_row, player_col, dest_row, dest_col):
                    moves.append((dest_row, dest_col))
        return moves

    def drawboard(self):
        """
        Draw the game board on the screen.
        """
        #draw grid and alternates colors
        for row in range(constants.ROWS):
            for col in range(constants.COLS):
                if (row + col) % 2 == constants.EMPTY: #alternates colors
                    pygame.draw.rect(screen, constants.ALT_GRAY, (row * constants.SQUARE_SIZE, col * constants.SQUARE_SIZE, constants.SQUARE_SIZE, constants.SQUARE_SIZE))
                else:
                    pygame.draw.rect(screen, constants.GRAY, (row * constants.SQUARE_SIZE, col * constants.SQUARE_SIZE, constants.SQUARE_SIZE, constants.SQUARE_SIZE))
        
        #draw players and destroyed tiles
        for row in range(constants.ROWS):
            for col in range(constants.COLS):
                if self.board[row][col] == constants.PLAYER1:
                    #pygame.draw.rect(screen, constants.RED, (row * 100, col * 100, 100, 100))
                    
                    #draw chess-queen.svg on player 1
                    queen = pygame.image.load(constants.QUEEN)
                    #resize image to cover the entire tile
                    queen = pygame.transform.scale(queen, (constants.QUEEN_SIZE, constants.QUEEN_SIZE))
                    
                    #if current player is player 1, set image to red
                    if self.turn == 1:
                        queen.fill(constants.RED, special_flags=pygame.BLEND_RGB_MAX)
                    
                    screen.blit(queen, (row * constants.SQUARE_SIZE, col * constants.SQUARE_SIZE))
                    
                elif self.board[row][col] == constants.PLAYER2:
                    # pygame.draw.rect(screen, constants.BLUE, (row * 100, col * 100, 100, 100))
                    
                    #draw chess-queen.svg on player 2
                    queen = pygame.image.load(constants.QUEEN)
                    #resize image to cover the entire tile
                    queen = pygame.transform.scale(queen, (constants.QUEEN_SIZE, constants.QUEEN_SIZE))
                    
                    #if current player is player 2, set image to blue, else set to white
                    if self.turn == constants.PLAYER2:
                        queen.fill(constants.BLUE, special_flags=pygame.BLEND_RGB_MAX)
                    else:
                        queen.fill(constants.WHITE, special_flags=pygame.BLEND_RGB_MAX)
                    
                    screen.blit(queen, (row * constants.SQUARE_SIZE, col * constants.SQUARE_SIZE))
                    
                elif self.board[row][col] == constants.DESTROYED:
                    pygame.draw.rect(screen, constants.BLACK, (row * constants.SQUARE_SIZE, col * constants.SQUARE_SIZE, constants.SQUARE_SIZE, constants.SQUARE_SIZE))
                    #draws an X on destroyed tiles
                    pygame.draw.line(screen, constants.RED, (row * constants.SQUARE_SIZE, col * constants.SQUARE_SIZE), (row * constants.SQUARE_SIZE + constants.SQUARE_SIZE, col * constants.SQUARE_SIZE + constants.SQUARE_SIZE), 5)
                    pygame.draw.line(screen, constants.RED, (row * constants.SQUARE_SIZE + constants.SQUARE_SIZE, col * constants.SQUARE_SIZE), (row * constants.SQUARE_SIZE, col * constants.SQUARE_SIZE + constants.SQUARE_SIZE), 5)
                    
                    
        #draws circle over active player
        # player_row, player_col = self.getplayer()
        # pygame.draw.circle(screen, constants.WHITE, (player_row * 100 + 50, player_col * 100 + 50), 40, 5)
        
        #draws available moves for the current player with a semi-transparent green color
        for move in self.available_moves():
            dest_row, dest_col = move
            if (dest_row + dest_col) % 2 == constants.EMPTY:
                pygame.draw.rect(screen, constants.SEMI_GREEN_ALT_GRAY, (dest_row * constants.SQUARE_SIZE, dest_col * constants.SQUARE_SIZE, constants.SQUARE_SIZE, constants.SQUARE_SIZE))
            else:
                pygame.draw.rect(screen, constants.SEMI_GREEN_GRAY, (dest_row * constants.SQUARE_SIZE, dest_col * constants.SQUARE_SIZE, constants.SQUARE_SIZE, constants.SQUARE_SIZE))

#takes a game object and returns the best move for the current player

def MiniMax(game: Game, depth: int, is_maximizing: bool) -> int:
    if game.is_game_over(constants.PLAYER2):
        return -100
    elif game.is_game_over(constants.PLAYER1):
        return 100
        
    #if depth is max_depth, check the possible amount of moves for the current player
    if depth == constants.MAX_DEPTH:
            return len(game.available_moves(constants.PLAYER2)) - len(game.available_moves(constants.PLAYER1))
        
    if is_maximizing:
        Bestscore = -1000
        for move in game.available_moves(constants.PLAYER2):
            dest_row, dest_col = move
            player_row, player_col = game.getplayer(constants.PLAYER2)
            game.move(player_row, player_col, dest_row, dest_col, constants.PLAYER2)
            score = MiniMax(game, depth + 1, False)
            game.board[player_row][player_col] = constants.PLAYER2
            game.board[dest_row][dest_col] = constants.EMPTY
            Bestscore = max(score, Bestscore)
        return Bestscore
    else:
        Bestscore = 1000
        for move in game.available_moves(constants.PLAYER1):
            dest_row, dest_col = move
            player_row, player_col = game.getplayer(constants.PLAYER1)
            game.move(player_row, player_col, dest_row, dest_col, constants.PLAYER1)
            score = MiniMax(game, depth + 1, True)
            game.board[player_row][player_col] = constants.PLAYER1
            game.board[dest_row][dest_col] = constants.EMPTY
            Bestscore = min(score, Bestscore)
        return Bestscore

pygame.init()
pygame.display.set_caption("Isolation Game")
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
clock = pygame.time.Clock()
running = True

game = Game()

game.board[0][0] = constants.PLAYER1
game.board[5][5] = constants.PLAYER2

def draw_winner_on_screen(game, screen):
        GAME_FONT = pygame.freetype.SysFont("Arial", 50)
        text_surface, rect = GAME_FONT.render(f"Black wins!" if game.winner == constants.PLAYER1 else "White wins!", constants.WHITE)
        GAME_FONT.render_to(screen, (constants.WIDTH//2 - rect.width//2, constants.HEIGHT//2 - rect.height//2), f"Black wins!" if game.winner == constants.PLAYER1 else "White wins!", constants.WHITE)
        pygame.display.flip()
                
def draw_screen(game, screen):
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # RENDER YOUR GAME HERE
    game.drawboard()
    
    # flip() the display to put your work on screen
    pygame.display.flip()

def ai_move(game):
    bestScore = -1000
    bestmove = (0, 0)
    
    #make the AI move
    player_row, player_col = game.getplayer()
    for move in game.available_moves():
        
        dest_row, dest_col = move
        player_row, player_col = game.getplayer(constants.PLAYER2)
        game.move(player_row, player_col, dest_row, dest_col, constants.PLAYER2)
        
        score = MiniMax(game, 0, False)
        if score > bestScore:
            bestScore = score
            bestmove = move
        game.board[player_row][player_col] = constants.PLAYER2
        game.board[dest_row][dest_col] = constants.EMPTY
        
    game.move(player_row, player_col, bestmove[0], bestmove[1])

while running:
    draw_screen(game, screen)
    
    if game.is_game_over():
        draw_winner_on_screen(game, screen)
        running = False
            
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            row, col = pygame.mouse.get_pos()
            player_row, player_col = game.getplayer()
            dest_row, dest_col = row // constants.SQUARE_SIZE, col // constants.SQUARE_SIZE
            if game.move(player_row, player_col, dest_row, dest_col):
                if game.is_game_over():
                    game.drawboard()
                    draw_winner_on_screen()

                    running = False
                else:
                    draw_screen(game, screen)
                    ai_move(game)

    clock.tick(constants.FPS)  # limits FPS to 60

#sleep for 3 seconds before quitting
pygame.time.wait(3000)
pygame.quit()