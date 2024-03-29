import pygame
import pygame.freetype
import constants
import random

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
        self.zobrist_keys = [[[0 for piece in range(3)] for y_axis in range(constants.COLS)] for x_axis in range(constants.ROWS)] #The 3 stands for the 3 possible pieces: player 1, player 2, destroyed
        self.initialize_zobrist_keys()
        
    def initialize_zobrist_keys(self) -> None:
        """
        Initialize the Zobrist keys for the game board.
        
        parameters:
        - None
        
        returns:
        - None
        """
        random.seed(constants.SEED)
        for x_axis in range(constants.ROWS):
            for y_axis in range(constants.COLS):
                for piece in range(3):
                    self.zobrist_keys[x_axis][y_axis][piece] = random.randint(0, 2**64 - 1)
        
    def is_move_valid(self, player_x_axis, player_y_axis, dest_x_axis, dest_y_axis) -> bool:
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
    
    def move(self, player_x_axis, player_y_axis, dest_x_axis, dest_y_axis, simulate_player: int=None) -> bool:
        """
        Move the current player to the destination position.
        Also switches the turn to the other player. and increments the moves.

        Parameters:
        - player_x_axis (int): x_axis-coordinate of the current player's position
        - player_y_axis (int): y_axis-coordinate of the current player's position
        - dest_x_axis (int): x_axis-coordinate of the destination position
        - dest_y_axis (int): y_axis-coordinate of the destination position
        - simulate_player (int): The player to simulate the move for

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
        
    def getplayer(self, player=None) -> tuple:
        """
        Get the current player's position.
        If player is specified, return the position of the specified player instead.


        Parameters:
        - player (int): The player to get the position for

        Returns:
        - tuple: (x_axis, y_axis) coordinates of the current player's position
        """        
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
                
    def is_game_over(self, active_player: int=None) -> bool:
        """
        Check if the game is over.
        
        parameters:
        - active_player (int): The player to check if the game is over for

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

    def available_moves(self, player=None) -> list:
        """
        Get a list of available moves for the current player.
        If player is specified, return a list of available moves for the specified player instead.
        
        parameters:
        - player (int): The player to get the available moves for

        Returns:
        - list: List of available moves as tuples (x_axis, y_axis)
        """
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

    def drawboard(self, screen) -> None:
        """
        Draw the game board on the screen.
        
        parameters:
        - screen (pygame.Surface): The screen to draw on
        
        Returns:
        - None
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
                    #draw chess-queen.svg on player 1
                    queen = pygame.image.load(constants.QUEEN)
                    #resize image to cover the entire tile
                    queen = pygame.transform.scale(queen, (constants.QUEEN_SIZE, constants.QUEEN_SIZE))
                    
                    #if current player is player 1, set image to red
                    if self.turn == 1:
                        queen.fill(constants.RED, special_flags=pygame.BLEND_RGB_MAX)
                    
                    screen.blit(queen, (x_axis * constants.SQUARE_SIZE, y_axis * constants.SQUARE_SIZE))
                    
                elif self.board[x_axis][y_axis] == constants.PLAYER2:
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
                    
        #draws available moves for the current player with a semi-transparent green color
        for move in self.available_moves():
            dest_x_axis, dest_y_axis = move
            if (dest_x_axis + dest_y_axis) % 2 == constants.EMPTY:
                pygame.draw.rect(screen, constants.SEMI_GREEN_ALT_GRAY, (dest_x_axis * constants.SQUARE_SIZE, dest_y_axis * constants.SQUARE_SIZE, constants.SQUARE_SIZE, constants.SQUARE_SIZE))
            else:
                pygame.draw.rect(screen, constants.SEMI_GREEN_GRAY, (dest_x_axis * constants.SQUARE_SIZE, dest_y_axis * constants.SQUARE_SIZE, constants.SQUARE_SIZE, constants.SQUARE_SIZE))


def MiniMax(game: Game, depth: int, alfa: int, beta: int, is_maximizing: bool) -> int:
    """
    The MiniMax algorithm.
    parameters:
    - game (Game): The game state to evaluate
    - depth (int): The current depth of the search
    - alfa (int): The current best score for the maximizing player
    - beta (int): The current best score for the minimizing player
    - is_maximizing (bool): True if the current player is the maximizing player, False otherwise
    
    Returns:
    - int: The best score for the current game state
    """
    
    #set ai_player to constants.PLAYER2 if game.turn is constants.PLAYER2, else set to constants.PLAYER1
    ai_player = constants.PLAYER2 if game.turn == constants.PLAYER2 else constants.PLAYER1
    other_player = constants.PLAYER1 if game.turn == constants.PLAYER2 else constants.PLAYER2
    
    if game.is_game_over(ai_player):
        return -constants.WINNING_SCORE
    elif game.is_game_over(other_player):
        return constants.WINNING_SCORE
        
    #if depth is max_depth, check the possible amount of moves for the current player
    if depth  == constants.MAX_DEPTH: # old algorithm can be found at: https://www.desmos.com/calculator/bijlk0fzbv
        return len(game.available_moves(ai_player)) - len(game.available_moves(other_player))
        
    current_player = other_player
    best_score = constants.DEFAULT_BEST_SCORE
    get_best_score = max if is_maximizing else min #uses the max function if is_maximizing is True, else uses the min function
    if is_maximizing:
        current_player = ai_player
        best_score = -constants.DEFAULT_BEST_SCORE

    for move in game.available_moves(current_player):
        dest_x_axis, dest_y_axis = move
        player_x_axis, player_y_axis = game.getplayer(current_player)
        game.move(player_x_axis, player_y_axis, dest_x_axis, dest_y_axis, current_player)
        score = MiniMax(game, depth + 1, alfa, beta, not is_maximizing)
        game.board[player_x_axis][player_y_axis] = current_player
        game.board[dest_x_axis][dest_y_axis] = constants.EMPTY
        best_score = get_best_score(score, best_score)

        if (is_maximizing and best_score > beta) or (not is_maximizing and best_score < alfa):
            break
        if is_maximizing:
            alfa = max(best_score, alfa)
        else:
            beta = min(best_score, beta)
        
    return best_score

def draw_winner_on_screen(game, screen) -> None:
    """
    Draw the winner on the screen.
    
    Parameters:
    - game (Game): The game state
    - screen (pygame.Surface): The screen to draw on
    
    Returns:
    - None
    """    
    GAME_FONT = pygame.freetype.SysFont("Arial", 50)
    text_surface, rect = GAME_FONT.render(f"Black wins!" if game.winner == constants.PLAYER1 else "White wins!", constants.WHITE)
    GAME_FONT.render_to(screen, (constants.WIDTH//2 - rect.width//2, constants.HEIGHT//2 - rect.height//2), f"Black wins!" if game.winner == constants.PLAYER1 else "White wins!", constants.WHITE)
    pygame.display.flip()
                
def draw_screen(game, screen) -> None:
    """
    Draw the game screen.
    
    Parameters:
    - game (Game): The game state
    - screen (pygame.Surface): The screen to draw on
    
    Returns:
    - None
    """

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # renders game board
    game.drawboard(screen)
    
    # flip() the display to put your work on screen
    pygame.display.flip()

def zobrist_hash(game: Game) -> int:
    """
    Get the Zobrist hash for the current game state.
    
    parameters:
    - game (Game): The game state

    Returns:
    - int: The Zobrist hash for the current game state
    """
    hash = 0
    for x_axis in range(constants.ROWS):
        for y_axis in range(constants.COLS):
            piece = game.board[x_axis][y_axis]
            if piece != constants.EMPTY:
                hash ^= game.zobrist_keys[x_axis][y_axis][piece - 1] #piece - 1 because the pieces are 1, 2 and 3, but the zobrist_keys are 0, 1 and 2
    
    # print("Zobrist hash:", hash)
    # print("current board state:", game.board)
    # print("current player:", game.turn)
        
    return hash

def is_in_transition_table(game: Game, transition_table: dict) -> bool:
    """
    Check if the current game state is in the transition table.
    
    parameters:
    - game (Game): The game state
    - transition_table (dict): The transition table

    Returns:
    - bool: True if the current game state is in the transition table, False otherwise
    """
    is_in_transition_table = zobrist_hash(game) in transition_table
    # print("Is in transition table:", is_in_transition_table)
    return is_in_transition_table

def get_best_move_from_transition_table(game: Game, transition_table: dict) -> tuple:
    """
    Get the best move for the current game state from the transition table.
    
    parameters:
    - game (Game): The game state
    - transition_table (dict): The transition table

    Returns:
    - tuple: The best move for the current game state
    """
    #print("Retrieved", zobrist_hash(game), ":", transition_table[zobrist_hash(game)])
    return transition_table[zobrist_hash(game)]

#make a function to store the best move in the transition table
def store_best_move_in_transition_table(game: Game, best_move: tuple, transition_table: dict) -> dict:
    """
    Store the best move for the current game state in the transition table.
    
    parameters:
    - game (Game): The game state
    - best_move (tuple): The best move for the current game state
    - transition_table (dict): The transition table

    Returns:
    - dict: The updated transition table
    """
    transition_table[zobrist_hash(game)] = best_move
    # print("Transition table updated")
    # print("Added", zobrist_hash(game), ":", best_move)    
    # print(transition_table)
    return transition_table

def get_transition_table_from_file() -> dict:
    """
    Get the transition table from a file.

    Returns:
    - dict: The transition table
    """
    try:
        with open("transition_table.txt", "r") as file:
            transition_table = eval(file.read())
            print("Transition table retrieved from file")
            return transition_table
    except FileNotFoundError:
        print("Transition table file not found")
        return {}
    
def store_transition_table_in_file(transition_table: dict) -> None:
    """
    Store the transition table in a file.

    Returns:
    - None
    """
    with open("transition_table.txt", "w") as file:
        file.write(str(transition_table))
        print("Transition table stored in file")


def ai_move(game, transition_table, ai_player: int=constants.PLAYER2) -> None: #Should be reworked to use current player instead of constants.PLAYER2
    """
    Make the AI move.
    
    parameters:
    - game (Game): The game state
    - transition_table (dict): The transition table
    - ai_player (int): The AI player
    
    Returns:
    - None
    """    
    if is_in_transition_table(game, transition_table):
        best_move = get_best_move_from_transition_table(game, transition_table)
        player_x_axis, player_y_axis = game.getplayer()
        game.move(player_x_axis, player_y_axis, best_move[0], best_move[1])
        return
    
    bestScore = -constants.DEFAULT_BEST_SCORE
    bestmove = (0, 0)
    
    #make the AI move
    for move in game.available_moves():
        dest_x_axis, dest_y_axis = move
        player_x_axis, player_y_axis = game.getplayer()
        game.move(player_x_axis, player_y_axis, dest_x_axis, dest_y_axis, ai_player)
        
        score = MiniMax(game, 0, -constants.DEFAULT_BEST_SCORE, constants.DEFAULT_BEST_SCORE, False)
        if score > bestScore:
            bestScore = score
            bestmove = move
        game.board[player_x_axis][player_y_axis] = ai_player
        game.board[dest_x_axis][dest_y_axis] = constants.EMPTY
        if bestScore == constants.WINNING_SCORE:
            break
        
    #store the best move in the transition table
    transition_table = store_best_move_in_transition_table(game, bestmove, transition_table)
    game.move(player_x_axis, player_y_axis, bestmove[0], bestmove[1])

#initialize the transition table
transition_table = get_transition_table_from_file()

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
        ai_move(game, transition_table, game.turn)

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

store_transition_table_in_file(transition_table)

#sleep for 3 seconds before quitting
pygame.time.wait(3000)
pygame.quit()