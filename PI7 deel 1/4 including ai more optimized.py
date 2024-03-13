import pygame
import pygame.freetype
import constants

class Game():
    def __init__(self):
        """
        Initialize the game board and other game variables.
        """
        #make a 2 dimensional array of 6 rows and 6 columns
        self.board = [[0 for x_axis in range(constants.ROWS)] for y_axis in range(constants.ROWS)] #0 is empty, 1 is player 1, 2 is player 2, 3 is destroyed
        self.turn = 1
        self.winner = 0
        self.moves = 0
        
    def is_move_valid(self, player_x_axis, player_y_axis, dest_x_axis, dest_y_axis):  #TODO change I and J to x_axis and y_axis
        """
        Check if a move is valid.

        Parameters:
        - player_x_axis (int): x_axis-coordinate of the current player's position
        - player_y_axis (int): y_axis-coordinate of the current player's position
        - dest_x_axis (int): x_axis-coordinate of the destination position
        - dest_y_axis (int): y_axis-coordinate of the destination position

        Returns:
        - bool: True if the move is valid, False otherwise
        """
        #check if destination is empty
        if self.board[dest_x_axis][dest_y_axis] != constants.EMPTY:
            return False
        
        #check if destination is in same x_axis or y_axis as player and check if destination is on same diagonal as player
        if (player_x_axis != dest_x_axis and player_y_axis != dest_y_axis) and (abs(player_x_axis - dest_x_axis) != abs(player_y_axis - dest_y_axis)):
                return False
            
        #check if there is another player or destroyed tile between player and destination
        if player_x_axis == dest_x_axis:
            for i in range(min(player_y_axis, dest_y_axis) + 1, max(player_y_axis, dest_y_axis)):
                if self.board[player_x_axis][i] != constants.EMPTY:
                    return False
        elif player_y_axis == dest_y_axis:
            for i in range(min(player_x_axis, dest_x_axis) + 1, max(player_x_axis, dest_x_axis)):
                if self.board[i][player_y_axis] != constants.EMPTY:
                    return False
        else:
            for i in range(1, abs(player_x_axis - dest_x_axis)):
                if self.board[player_x_axis + i * (1 if dest_x_axis > player_x_axis else -1)][player_y_axis + i * (1 if dest_y_axis > player_y_axis else -1)] != constants.EMPTY:
                    return False
        
        return True
    
    def move(self, player_x_axis, player_y_axis, dest_x_axis, dest_y_axis, simulate_player: int=None):
        """
        Move the current player to the destination position.
        Also switches the turn to the other player. and increments the moves.

        Parameters:
        - player_x_axis (int): x_axis-coordinate of the current player's position
        - player_y_axis (int): y_axis-coordinate of the current player's position
        - dest_x_axis (int): x_axis-coordinate of the destination position
        - dest_y_axis (int): y_axis-coordinate of the destination position

        Returns:
        - bool: True if the move is successful, False otherwise
        """
        if simulate_player and self.is_move_valid(player_x_axis, player_y_axis, dest_x_axis, dest_y_axis):
            self.board[dest_x_axis][dest_y_axis] = simulate_player
            self.board[player_x_axis][player_y_axis] = constants.DESTROYED
            return True
        
        
        elif self.is_move_valid(player_x_axis, player_y_axis, dest_x_axis, dest_y_axis):
            self.board[dest_x_axis][dest_y_axis] = self.turn #destination is now the player
            self.board[player_x_axis][player_y_axis] = constants.DESTROYED #old tile is now destroyed
            self.moves += 1 #increment moves
            self.turn = constants.PLAYER1 if self.turn == constants.PLAYER2 else constants.PLAYER2 #change turn
            return True
        else:
            return False
        
    def getplayer(self, player=None): #TODO change I and J to x_axis and y_axis
        """
        Get the current player's position.

        Returns:
        - tuple: (x_axis, y) coordinates of the current player's position
        """
        #return x_axis,y of current player in the grid based on the turn
        
        #if player is specified, return the position of the specified player
        if player:
            for x_axis in range(constants.ROWS):
                for y_axis in range(constants.COLS):
                    if self.board[x_axis][y_axis] == player:
                        return x_axis, y_axis
        else:
            for x_axis in range(constants.ROWS):
                for y_axis in range(constants.COLS):
                    if self.board[x_axis][y_axis] == self.turn:
                        return x_axis, y_axis
                
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
        - list: List of available moves as tuples (x_axis, y)
        """
        #return a list of available moves for the current player
        #if player is specified, return a list of available moves for the specified player
        if player:
            player_x_axis, player_y_axis = self.getplayer(player)
        else:
            player_x_axis, player_y_axis = self.getplayer()
        moves = []
        for dest_x_axis in range(constants.ROWS):
            for dest_y_axis in range(constants.COLS):
                if self.is_move_valid(player_x_axis, player_y_axis, dest_x_axis, dest_y_axis):
                    moves.append((dest_x_axis, dest_y_axis))
        return moves

    def drawboard(self):
        """
        Draw the game board on the screen.
        """
        #draw grid and alternates colors
        for x_axis in range(constants.ROWS):
            for y_axis in range(constants.COLS):
                if (x_axis + y_axis) % 2 == constants.EMPTY: #alternates colors
                    pygame.draw.rect(screen, constants.ALT_GRAY, (x_axis * constants.SQUARE_SIZE, y_axis * constants.SQUARE_SIZE, constants.SQUARE_SIZE, constants.SQUARE_SIZE))
                else:
                    pygame.draw.rect(screen, constants.GRAY, (x_axis * constants.SQUARE_SIZE, y_axis * constants.SQUARE_SIZE, constants.SQUARE_SIZE, constants.SQUARE_SIZE))
        
        #draw players and destroyed tiles
        for x_axis in range(constants.ROWS):
            for y_axis in range(constants.COLS):
                if self.board[x_axis][y_axis] == constants.PLAYER1:
                    #pygame.draw.rect(screen, constants.RED, (x_axis * 100, y_axis * 100, 100, 100))
                    
                    #draw chess-queen.svg on player 1
                    queen = pygame.image.load(constants.QUEEN)
                    #resize image to cover the entire tile
                    queen = pygame.transform.scale(queen, (constants.QUEEN_SIZE, constants.QUEEN_SIZE))
                    
                    #if current player is player 1, set image to red
                    if self.turn == 1:
                        queen.fill(constants.RED, special_flags=pygame.BLEND_RGB_MAX)
                    
                    screen.blit(queen, (x_axis * constants.SQUARE_SIZE, y_axis * constants.SQUARE_SIZE))
                    
                elif self.board[x_axis][y_axis] == constants.PLAYER2:
                    # pygame.draw.rect(screen, constants.BLUE, (x_axis * 100, y_axis * 100, 100, 100))
                    
                    #draw chess-queen.svg on player 2
                    queen = pygame.image.load(constants.QUEEN)
                    #resize image to cover the entire tile
                    queen = pygame.transform.scale(queen, (constants.QUEEN_SIZE, constants.QUEEN_SIZE))
                    
                    #if current player is player 2, set image to blue, else set to white
                    if self.turn == constants.PLAYER2:
                        queen.fill(constants.BLUE, special_flags=pygame.BLEND_RGB_MAX)
                    else:
                        queen.fill(constants.WHITE, special_flags=pygame.BLEND_RGB_MAX)
                    
                    screen.blit(queen, (x_axis * constants.SQUARE_SIZE, y_axis * constants.SQUARE_SIZE))
                    
                elif self.board[x_axis][y_axis] == constants.DESTROYED:
                    pygame.draw.rect(screen, constants.BLACK, (x_axis * constants.SQUARE_SIZE, y_axis * constants.SQUARE_SIZE, constants.SQUARE_SIZE, constants.SQUARE_SIZE))
                    #draws an X on destroyed tiles
                    pygame.draw.line(screen, constants.RED, (x_axis * constants.SQUARE_SIZE, y_axis * constants.SQUARE_SIZE), (x_axis * constants.SQUARE_SIZE + constants.SQUARE_SIZE, y_axis * constants.SQUARE_SIZE + constants.SQUARE_SIZE), 5)
                    pygame.draw.line(screen, constants.RED, (x_axis * constants.SQUARE_SIZE + constants.SQUARE_SIZE, y_axis * constants.SQUARE_SIZE), (x_axis * constants.SQUARE_SIZE, y_axis * constants.SQUARE_SIZE + constants.SQUARE_SIZE), 5)
                    
                    
        #draws circle over active player
        # player_x_axis, player_y_axis = self.getplayer()
        # pygame.draw.circle(screen, constants.WHITE, (player_x_axis * 100 + 50, player_y_axis * 100 + 50), 40, 5)
        
        #draws available moves for the current player with a semi-transparent green color
        for move in self.available_moves():
            dest_x_axis, dest_y_axis = move
            if (dest_x_axis + dest_y_axis) % 2 == constants.EMPTY:
                pygame.draw.rect(screen, constants.SEMI_GREEN_ALT_GRAY, (dest_x_axis * constants.SQUARE_SIZE, dest_y_axis * constants.SQUARE_SIZE, constants.SQUARE_SIZE, constants.SQUARE_SIZE))
            else:
                pygame.draw.rect(screen, constants.SEMI_GREEN_GRAY, (dest_x_axis * constants.SQUARE_SIZE, dest_y_axis * constants.SQUARE_SIZE, constants.SQUARE_SIZE, constants.SQUARE_SIZE))

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
            dest_x_axis, dest_y_axis = move
            player_x_axis, player_y_axis = game.getplayer(constants.PLAYER2)
            game.move(player_x_axis, player_y_axis, dest_x_axis, dest_y_axis, constants.PLAYER2)
            score = MiniMax(game, depth + 1, False)
            game.board[player_x_axis][player_y_axis] = constants.PLAYER2
            game.board[dest_x_axis][dest_y_axis] = constants.EMPTY
            Bestscore = max(score, Bestscore)
        return Bestscore
    else:
        Bestscore = 1000
        for move in game.available_moves(constants.PLAYER1):
            dest_x_axis, dest_y_axis = move
            player_x_axis, player_y_axis = game.getplayer(constants.PLAYER1)
            game.move(player_x_axis, player_y_axis, dest_x_axis, dest_y_axis, constants.PLAYER1)
            score = MiniMax(game, depth + 1, True)
            game.board[player_x_axis][player_y_axis] = constants.PLAYER1
            game.board[dest_x_axis][dest_y_axis] = constants.EMPTY
            Bestscore = min(score, Bestscore)
        return Bestscore

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
    player_x_axis, player_y_axis = game.getplayer()
    for move in game.available_moves():
        
        dest_x_axis, dest_y_axis = move
        player_x_axis, player_y_axis = game.getplayer(constants.PLAYER2)
        game.move(player_x_axis, player_y_axis, dest_x_axis, dest_y_axis, constants.PLAYER2)
        
        score = MiniMax(game, 0, False)
        if score > bestScore:
            bestScore = score
            bestmove = move
        game.board[player_x_axis][player_y_axis] = constants.PLAYER2
        game.board[dest_x_axis][dest_y_axis] = constants.EMPTY
        
    game.move(player_x_axis, player_y_axis, bestmove[0], bestmove[1])


pygame.init()
pygame.display.set_caption("Isolation Game")
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
clock = pygame.time.Clock()
running = True

game = Game()

game.board[0][0] = constants.PLAYER1
game.board[5][5] = constants.PLAYER2


while running:
    
    if game.turn == constants.PLAYER2:
        ai_move(game) #needs to be async with protection against multiple calls

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and game.turn == constants.PLAYER1:
            x_axis, y_axis = pygame.mouse.get_pos()
            player_x_axis, player_y_axis = game.getplayer()
            
            dest_x_axis, dest_y_axis = x_axis // constants.SQUARE_SIZE, y_axis // constants.SQUARE_SIZE
            game.move(player_x_axis, player_y_axis, dest_x_axis, dest_y_axis)

    draw_screen(game, screen)
    
    if game.is_game_over():
        draw_winner_on_screen(game, screen)
        running = False

    clock.tick(constants.FPS)  # limits FPS to 60

#sleep for 3 seconds before quitting
pygame.time.wait(3000)
pygame.quit()