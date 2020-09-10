# Import packages
import pygame
import math
import copy
import operator
import time
#Alunos: Enzo Matheus Paganini, Osmar Andre Bassi e Vinicius Massao Dziewulski
#Para jogar, voce precisa apertar na peca com o botao esquerdo do mouse segurar, mover ateh a posicao que deseja movimentar a peca e soltar o botao do mouse para realizar a jogada

print("Alunos: Enzo Matheus Paganini, Osmar Andre Bassi e Vinicius Massao Dziewulski")
print("Para jogar, voce precisa apertar na peca com o botao esquerdo do mouse segurar, mover ateh a posicao que deseja movimentar a peca e soltar o botao do mouse para realizar a jogada")


#Comentarios em portugues feitos por -> Enzo Matheus Paganini, Osmar Andre Bassi e Vinicius Massao Dziewulski. Para implementacao da IA
#Comentarios em ingles feito pelo desenvolvedor original do jogo-> https://github.com/parkershamblin/checkers-pygame

#IA iniciando como peca branca
player = 2

# Inititalize Pieces
empty = 0
friendly = {'pawn': 1, 'king': 3}
enemy = {'pawn': 2, 'king': 4}

# Initalize board size
rows = 10
columns = 10

game_over = False
infinity = float(math.inf)

# Create board 
def create_board():
    board = [[empty for column in range(columns)] for row in range(rows)]
    return board


def place_starting_pieces():
    """Assign starting checker pieces for red and black"""
    # Assign starting board locations for red
    for current_row in range(6, 10, 2):
        for current_column in range(1, 10, 2):
            board[current_row][current_column] = friendly['pawn']
    for current_row in range(7, 10, 2):
        for current_column in range(0, 10, 2):
            board[current_row][current_column] = friendly['pawn']

    # Assign starting board locations for black
    for current_row in range(0, 4, 2):
        for current_column in range(1, 10, 2):
            board[current_row][current_column] = enemy['pawn']
    for current_row in range(1, 4, 2):
        for current_column in range(0, 10, 2):
            board[current_row][current_column] = enemy['pawn'] 


def is_valid_selection(board, current_player, old_x, old_y):
    """Restricts player from slecting posisitions containing no checker pieces or """
    board_selection = board[old_y][old_x]
    if board_selection is friendly['pawn'] or board_selection is friendly['king']:
        return True
    elif board_selection is (enemy['pawn'] or enemy['king']):
        print("You've selected an enemy player's piece. Please select your own piece.")
        return False
    else:
        print("You didn't select a piece. Please try selecting one of your pieces.")
        return False


def is_valid_move(current_player, board, old_x, old_y, new_x, new_y):
    """All logic for pawn pieces."""

    # Prevents moving to a location that already contains a piece.
    
    if board[new_y][new_x] != empty:
        print("You cant land on another piece. Please select another location.")
        return False

    # Checking for valid moves for Player 1
    if board[old_y][old_x] is 1:
        if (new_y - old_y) is -1 and (new_x - old_x) is 1:
            return True
        elif (new_y - old_y) is -1 and (new_x - old_x) is -1:
            return True

        # Checking for valid front jump for Player 1
        elif (new_y - old_y) is -2 and (new_x - old_x) is 2:
            if board[new_y + 1][new_x - 1] is (enemy['pawn'] or enemy['king']):
                board[new_y + 1][new_x - 1] = empty
                return True
            else:
                return False
        elif (new_y - old_y) is -2 and (new_x - old_x) is -2:
            if board[new_y + 1][new_x + 1] is (enemy['pawn'] or enemy['king']):
                board[new_y + 1][new_x + 1] = empty
                return True
            else:
                return False
        # Checking for valid rear jump for Player 1
        elif (new_y - old_y) is 2 and (new_x - old_x) is -2:
            if board[new_y - 1][new_x + 1] is (enemy['pawn'] or enemy['king']):
                board[new_y - 1][new_x + 1] = empty
                return True
            else:
                return False
        
        elif (new_y - old_y) is 2 and (new_x - old_x) is 2:
            if board[new_y - 1][new_x - 1] is (enemy['pawn'] or enemy['king']):
                board[new_y - 1][new_x - 1] = empty
                return True
            else:
                return False
        else:
            print("You can't move that far. Please select another positition to move too.")
            return False
                
    # Checking for valid moves for Player 2
    elif board[old_y][old_x] is 2:
        if (new_y - old_y) is 1 and (new_x - old_x) is 1:
            return True
        elif (new_y - old_y) is 1 and (new_x - old_x) is -1:
            return True
        # Checking for valid front jumps for Player 2
        elif (new_y - old_y) is -2 and (new_x - old_x) is 2:
            if board[new_y + 1][new_x - 1] is (enemy['pawn'] or enemy['king']):
                board[new_y + 1][new_x - 1] = empty
                return True
            else:
                return False
        elif (new_y - old_y) is -2 and (new_x - old_x) is -2:
            if board[new_y + 1][new_x + 1] is (enemy['pawn'] or enemy['king']):
                board[new_y + 1][new_x + 1] = empty
                return True
            else:
                return False
        # Checking for valid rear jump for Player 2
        elif (new_y - old_y) is 2 and (new_x - old_x) is -2:
            if board[new_y - 1][new_x + 1] is (enemy['pawn'] or enemy['king']):
                board[new_y - 1][new_x + 1] = empty
                return True
            else:
                return False
        
        elif (new_y - old_y) is 2 and (new_x - old_x) is 2:
            if board[new_y - 1][new_x - 1] is (enemy['pawn'] or enemy['king']):
                board[new_y - 1][new_x - 1] = empty
                return True
            else:
                return False
        else:
            print("You can't move that far. Please select another positition to move too.")
            return False


def no_chips_between(board, old_x, old_y, new_x, new_y):
    """Restricts king pieces from jumping over several players at once"""
    board_y_coords = []
    board_x_coords = []
    if old_y < new_y:
        for row in range(old_y, new_y):
            board_y_coords.append(row)
    if old_y > new_y:
        for row in range(old_y, new_y, -1):
            board_y_coords.append(row)
    if old_x < new_x:
        for column in range(old_x, new_x):
            board_x_coords.append(column)
    if old_x > new_x:
        for column in range(old_x, new_x, -1):
            board_x_coords.append(column)

    board_coords = list(zip(board_x_coords, board_y_coords))
    board_values = [board[y][x] for x, y in board_coords]
    if len(board_values) > 2:
        if all(i is empty for i in board_values[1:-1]) is True:
            board[new_y][new_x] = board[old_y][old_x]
            board[old_y][old_x] = empty
            return True
            
    # Allows king players to jump next to enemy pieces right next to them
    if len(board_values) is 2:
        if all(i is enemy['pawn'] for i in board_values[1:]) is True:
            board[new_y][new_x] = board[old_y][old_x]
            board[old_y][old_x] = empty
            return True
        elif all(i is enemy['king'] for i in board_values[1:]) is True:
            board[new_y][new_x] = board[old_y][old_x]
            board[old_y][old_x] = empty
            return True
        elif all(i is empty for i in board_values[1:]) is True:
            board[new_y][new_x] = board[old_y][old_x]
            board[old_y][old_x] = empty
            return True

    # Allows king players to move one spot over (like a pawn would move)
    elif len(board_values) is 1:
        if all(i is empty for i in board_values[1:]) is True:
            board[new_y][new_x] = board[old_y][old_x]
            board[old_y][old_x] = empty
            return True
    else:
        print("You can't jump over several chips at once. Please try another move.")
        return False


def is_valid_king_move(current_player, board, old_x, old_y, new_x, new_y):
    """All logic for king pieces"""
    # Prevents player from jumping onto another player
    if board[new_y][new_x] != 0:
        print("Even as king you cannot land directly onto another player's piece.")
        return False
    # Prevent horizontal moves
    if new_y is old_y:
        print("Even as a king you cannot move horizontally in this diagonal world.")
        return False
    # Prevent horizontal moves
    if new_x is old_x:
        print("Even as a king you cannot move vertically in this diagonal world.")
        return False

    # Prevent moves that do not have a slope of 1
    if new_x > old_x and new_y > old_y:
        if (new_x - old_x) != (new_y - old_y):
            return False
    if new_x < old_x and new_y < old_y:
        if (old_x - new_x) != (old_y - new_y):
            return False
    if new_x < old_x and new_y > old_y:
        if (old_x - new_x) != (new_y - old_y):
            return False
    if new_x > old_x and new_y < old_y:
        if (new_x - old_x) != (old_y - new_y):
            return False


    # King Jump Logic
    if board[old_y][old_x] is friendly['king']:
        try: # North East Jump
            if board[new_y + 1][new_x - 1] is enemy['pawn'] or enemy['king']:
                if old_x < new_x and old_y > new_y:
                    if no_chips_between(board, old_x, old_y, new_x, new_y):
                        board[new_y][new_x] = friendly['king']
                        board[new_y + 1][new_x - 1] = empty
                        board[old_y][old_x] = empty
                        return True
        except IndexError:
            pass
        try: # North West Jump 
            if board[new_y + 1][new_x + 1] is enemy['pawn'] or enemy['king']:
                if old_x > new_x and old_y > new_y:
                    if no_chips_between(board, old_x, old_y, new_x, new_y) is True:
                        board[new_y][new_x] = friendly['king']
                        board[new_y + 1][new_x + 1] = empty
                        board[old_y][old_x] = empty
                        return True
        except IndexError:
            pass
        try: # South East Jump
            if board[new_y - 1][new_x - 1] is enemy['pawn'] or enemy['king']:
                if no_chips_between(board, old_x, old_y, new_x, new_y) is True:
                    if old_x < new_x and old_y < new_y:
                        board[new_y][new_x] = friendly['king']
                        board[new_y - 1][new_x - 1] = empty
                        board[old_y][old_x] = empty
                        return True
        except IndexError:
            pass
        try: # South West Jump
            if board[new_y - 1][new_x + 1] is enemy['pawn'] or enemy['pawn']:
                if no_chips_between(board, old_x, old_y, new_x, new_y) is True:
                    if old_x > new_x and old_y < new_y:
                        board[new_y][new_x] = friendly['king']
                        board[new_y - 1][new_x + 1] = empty
                        board[old_y][old_x] = empty
                        return True
        except IndexError:
            pass

#funcao que checa se eh possivel fazer o movimento para double jump
def is_valid_move_double(current_player, board, old_x, old_y, new_x, new_y):
    """All logic for pawn pieces."""

    #caso a nova posicao seja diferente de vazia
    if board[new_y][new_x] != empty:
        return False

    # Checking for valid moves for Player 1
    if board[old_y][old_x] is 1:
        #checando a possibilidade de tomada de peca
        if (new_y - old_y) is 2 and (new_x - old_x) is -2:
            #se existe um inimigo entre a nova movimentacao na diagonal
            if board[new_y - 1][new_x + 1] is (enemy['pawn'] or enemy['king']):
                #realiza a tomada de peca
                board[new_y - 1][new_x + 1] = empty
                return True
            else:
                return False
        #checando a possibilidade de tomada de peca
        elif (new_y - old_y) is 2 and (new_x - old_x) is 2:
            #se existe um inimigo entre a nova movimentacao na diagonal
            if board[new_y - 1][new_x - 1] is (enemy['pawn'] or enemy['king']):
                #realiza a tomada de peca
                board[new_y - 1][new_x - 1] = empty
                return True
            else:
                return False
        
        #checando a possibilidade de tomada de peca
        elif (new_y - old_y) is -2 and (new_x - old_x) is 2:
            #se existe um inimigo entre a nova movimentacao na diagonal
            if board[new_y + 1][new_x - 1] is (enemy['pawn'] or enemy['king']):
                #realiza a tomada de peca
                board[new_y + 1][new_x - 1] = empty
                return True
            else:
                return False
        #checando a possibilidade de tomada de peca
        elif (new_y - old_y) is -2 and (new_x - old_x) is -2:
            if board[new_y + 1][new_x + 1] is (enemy['pawn'] or enemy['king']):
                #realiza a tomada de peca
                board[new_y + 1][new_x + 1] = empty
                return True
            else:
                return False
        else:
            #print("You can't move that far. Please select another positition to move too.")
            return False
                
    '''# Checking for valid moves for Player 2
    elif board[old_y][old_x] is 2:
        if (new_y - old_y) is 1 and (new_x - old_x) is 1:
            return True
        elif (new_y - old_y) is 1 and (new_x - old_x) is -1:
            return True
        
        # Checking for valid rear jump for Player 2
        elif (new_y - old_y) is 2 and (new_x - old_x) is -2:
            if board[new_y - 1][new_x + 1] is (enemy['pawn'] or enemy['king']):
                board[new_y - 1][new_x + 1] = empty
                return True
            else:
                return False
        
        elif (new_y - old_y) is 2 and (new_x - old_x) is 2:
            if board[new_y - 1][new_x - 1] is (enemy['pawn'] or enemy['king']):
                board[new_y - 1][new_x - 1] = empty
                return True
            else:
                return False

        # Checking for valid front jumps for Player 2
        elif (new_y - old_y) is -2 and (new_x - old_x) is 2:
            if board[new_y + 1][new_x - 1] is (enemy['pawn'] or enemy['king']):
                board[new_y + 1][new_x - 1] = empty
                return True
            else:
                return False
        elif (new_y - old_y) is -2 and (new_x - old_x) is -2:
            if board[new_y + 1][new_x + 1] is (enemy['pawn'] or enemy['king']):
                board[new_y + 1][new_x + 1] = empty
                return True
            else:
                return False
        
        else:
            #print("You can't move that far. Please select another positition to move too.")
            return False'''

#funcao para fazer double jumps da usuario
def do_double_jumps(current_player, board, new_x, new_y, game_over):
    #se for peao
    if board[new_y][new_x] is friendly["pawn"]:
        try:
            #enquanto existir jogadas validas
            while True:
                #checa se ha vitoria
                if check_for_win(current_player, board):
                    game_over = True
                    break
                ogX = new_x
                ogY = new_y
                
                #verifica se existe inimigo na diagonal e se double jump eh valido
                if (board[ogY - 1][ogX - 1] is enemy['pawn'] or enemy['king']) and is_valid_move_double(current_player, board, ogX, ogY, ogX - 2, ogY - 2):
                    #novas posicoes de X e Y
                    new_x = ogX - 2
                    new_y = ogY - 2
                    #se deslocando para a nova posicao
                    board[new_y][new_x] = friendly['pawn']
                    #deixando posicao antiga vazia
                    board[ogY][ogX] = empty
                    
                #verifica se existe inimigo na diagonal e se double jump eh valido
                elif (board[ogY - 1][ogX + 1] is enemy['pawn'] or enemy['king']) and is_valid_move_double(current_player, board, ogX, ogY, ogX + 2, ogY - 2):
                    #novas posicoes de X e Y
                    new_x = ogX + 2
                    new_y = ogY - 2
                    #se deslocando para a nova posicao
                    board[new_y][new_x] = friendly['pawn']
                    #deixando posicao antiga vazia
                    board[ogY][ogX] = empty
                    
                #verifica se existe inimigo na diagonal e se double jump eh valido
                elif (board[ogY + 1][ogX - 1] is enemy['pawn'] or enemy['king']) and is_valid_move_double(current_player, board, ogX, ogY, ogX - 2, ogY + 2):
                    #novas posicoes de X e Y
                    new_x = ogX - 2
                    new_y = ogY + 2
                    #se deslocando para a nova posicao
                    board[new_y][new_x] = friendly['pawn']
                    #deixando posicao antiga vazia
                    board[ogY][ogX] = empty
                    
                #verifica se existe inimigo na diagonal e se double jump eh valido
                elif (board[ogY + 1][ogX + 1] is enemy['pawn'] or enemy['king']) and is_valid_move_double(current_player, board, ogX, ogY, ogX + 2, ogY + 2):
                    #novas posicoes de X e Y
                    new_x = ogX + 2
                    new_y = ogY + 2
                    #se deslocando para a nova posicao
                    board[new_y][new_x] = friendly['pawn']
                    #deixando posicao antiga vazia
                    board[ogY][ogX] = empty
                    #print(f"4- New coordinates: [{new_y}, {new_x}]")
                    
                else:
                    break
                
        except IndexError:
            pass
    #caso seja dama
    #OBS: funciona da mesma maneira
    elif board[new_y][new_x] is friendly['king']:
        try:
            while True:
                #checa se ha vitoria
                if check_for_win(current_player, board):
                    game_over = True
                    break
                ogX = new_x
                ogY = new_y
                
                #verifica se existe inimigo na diagonal e se double jump eh valido
                if (board[ogY - 1][ogX - 1] is enemy['pawn'] or enemy['king']) and is_valid_move_double(current_player, board, ogX, ogY, ogX - 2, ogY - 2):
                    #novas posicoes de X e Y
                    new_x = ogX - 2
                    new_y = ogY - 2
                    #se deslocando para a nova posicao
                    board[new_y][new_x] = friendly['king']
                    #deixando posicao antiga vazia
                    board[ogY][ogX] = empty
                    
                #verifica se existe inimigo na diagonal e se double jump eh valido
                elif (board[ogY - 1][ogX + 1] is enemy['pawn'] or enemy['king']) and is_valid_move_double(current_player, board, ogX, ogY, ogX + 2, ogY - 2):
                    #novas posicoes de X e Y
                    new_x = ogX + 2
                    new_y = ogY - 2
                    #se deslocando para a nova posicao
                    board[new_y][new_x] = friendly['king']
                    #deixando posicao antiga vazia
                    board[ogY][ogX] = empty
                    
                #verifica se existe inimigo na diagonal e se double jump eh valido
                elif (board[ogY + 1][ogX - 1] is enemy['pawn'] or enemy['king']) and is_valid_move_double(current_player, board, ogX, ogY, ogX - 2, ogY + 2):
                    #novas posicoes de X e Y
                    new_x = ogX - 2
                    new_y = ogY + 2
                    #se deslocando para a nova posicao
                    board[new_y][new_x] = friendly['king']
                    #deixando posicao antiga vazia
                    board[ogY][ogX] = empty
                    
                #verifica se existe inimigo na diagonal e se double jump eh valido
                elif (board[ogY + 1][ogX + 1] is enemy['pawn'] or enemy['king']) and is_valid_move_double(current_player, board, ogX, ogY, ogX + 2, ogY + 2):
                    #novas posicoes de X e Y
                    new_x = ogX + 2
                    new_y = ogY + 2
                    #se deslocando para a nova posicao
                    board[new_y][new_x] = friendly['king']
                    #deixando posicao antiga vazia
                    board[ogY][ogX] = empty
                    #print(f"4- New coordinates: [{new_y}, {new_x}]")
                    
                else:
                    break
                
        except IndexError:
            pass


def check_for_win(current_player, board):
    remaining_enemy_pieces = 0
    # Counting the remaining pieces
    for y in range(len(board)):
        for x in range(len(board)):
            if board[y][x] is enemy['pawn'] or board[y][x] is enemy['king']:
                remaining_enemy_pieces += 1
    # If the sum of all pieces is 0 then Win for current player
    if remaining_enemy_pieces is 0:
        print(f"Player {current_player} has won!. Because there are no pieces remaining for the enemy")
        return True
    return False
    

def draw_board(board):
    for row in range(10):
        for column in range(10):
            #  Variables for pygame.draw pos paramater
            # Draw all grid locations as either white or black rectangle
            if (row + column) % 2 is 0:
                color = white
            else:
                color = black
            rect = pygame.draw.rect(screen, color, [width * column, height * row, width, height])
            rect_center = rect.center
            if board[row][column] is 1:
                pygame.draw.circle(screen, white, rect_center, radius)
                # Draw border around black pieces so that they're visible
                pygame.draw.circle(screen, grey, rect_center, radius, border)
            if board[row][column] is 2:
                pygame.draw.circle(screen, black, rect_center, radius)
                # Draw border around black pieces so that they're visible
                pygame.draw.circle(screen, grey, rect_center, radius, border)
            # Drawing king pieces borders
            if board[row][column] is 3:
                pygame.draw.circle(screen, white, rect_center, radius)
                pygame.draw.circle(screen, gold, rect_center, radius, border)
            if board[row][column] is 4:
                pygame.draw.circle(screen, gold, rect_center, radius, border)

#funcao que verifica se existe inimigos proximos a peca
def is_valid_enemy_move(board, new_x, new_y):
    try:
        #se existe inimigo em uma diagonal
        if board[new_x-1][new_y-1] is enemy['pawn'] or enemy['king']:
            #se a diagonal oposta do inimigo esta vazia
            if board[new_y+1][new_x+1] is empty:
                return True
    except IndexError:
        pass
    try:
        #se existe inimigo em uma diagonal
        if board[new_y+1][new_x-1] is enemy['pawn'] or enemy['king']:
            #se a diagonal oposta do inimigo esta vazia
            if board[new_y-1][new_x+1] is empty:
                return True
    except IndexError:
        pass
    try:
        #se existe inimigo em uma diagonal
        if board[new_y-1][new_x+1] is enemy['pawn'] or enemy['king']:
            #se a diagonal oposta do inimigo esta vazia
            if board[new_y+1][new_x-1] is empty:
                return True
    except IndexError:
        pass
    try:
        #se existe inimigo em uma diagonal
        if board[new_y+1][new_x+1] is enemy['pawn'] or enemy['king']:
            #se a diagonal oposta do inimigo esta vazia
            if board[new_y-1][new_x-1] is empty:
                return True
    except IndexError:
        pass
    else:
        return False

#funcao que retorna todas as possibilidades de jogadas da IA
def successors(current_player, board, game_over):
    #retorna sucessores possiveis para o estado atual
    #Come uma peca ganha +1 ponto, perde uma peca perde -1 ponto e se nao come nao ganha nada(0)
    cords = []
    succ = []

    #Inserindo em uma lista todas as coordenadas das pecas friendly
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] is friendly['pawn'] or board[y][x] is friendly['king']:
                cords.append([y,x])
    #para cada peca friendly que esta na lista cords
    #eh testado se eh possivel realizar os movimentos para todas as diagonais
    for c in cords:
        ogY = c[0]
        ogX = c[1]
        #caso IA seja as pecas brancas
        if player is 2:
            #se for peao a peca na cordenada
            if board[ogY][ogX] is friendly['pawn']:
                #copia do tabuleiro
                copy_board = copy.deepcopy(board)
                score = 0
                #nova posicao de X e Y
                new_x = ogX-2
                new_y = ogY-2
                #if verificando se a nova posicao esta entre 10 e 0
                if new_x >= 10 or new_y >= 10:
                    pass
                elif new_x < 0 or new_y < 0:
                    pass 
                else:
                    verif = AI_move(current_player, copy_board, ogX, ogY, new_x, new_y, score)
                    #verificando se tem um inimigo um movimento antes e se eh possivel fazer o movimento
                    if (copy_board[ogY - 1][ogX - 1] is enemy['king'] or enemy['pawn']) and verif:
                        #somando +1 no score
                        score += 1
                        #movimentando a peca para a nova posicao
                        copy_board[new_y][new_x] = friendly['pawn']
                        #esvaziando a antiga posicao
                        copy_board[ogY][ogX] = empty
                        #verificando se eh possivel realizar os double jumps
                        dds = do_double_jumps_AI(current_player, copy_board, new_x, new_y)
                        #somando o retorno que vier de do_double_jumps_AI
                        score += dds
                        
                        verif_enemy = is_valid_enemy_move(copy_board, new_x, new_y)
                        #verificando se existe uma peca inimiga em uma das diagonais logo apos o movimento
                        if verif_enemy:
                            #somando -1 no score, porque provavelmente ira perder essa peca
                            score += -1
                        #adicionando essa jogada na lista com o score
                        succ.append([copy.deepcopy(copy_board),score])
                    
                score = 0
                #copia do tabuleiro
                copy_board = copy.deepcopy(board)
                #nova posicao de X e Y
                new_x = ogX+2
                new_y = ogY-2
                #if verificando se a nova posicao esta entre 10 e 0
                if new_x >= 10 or new_y >= 10:
                    pass
                elif new_x < 0 or new_y < 0:
                    pass 
                else:
                    verif = AI_move(current_player, copy_board, ogX, ogY, new_x, new_y, score)
                    #verificando se tem um inimigo um movimento antes e se eh possivel fazer o movimento
                    if (copy_board[ogY - 1][ogX + 1] is enemy['king'] or enemy['pawn']) and verif:
                        #somando +1 no score
                        score += 1
                        #movimentando a peca para a nova posicao
                        copy_board[new_y][new_x] = friendly['pawn']
                        #esvaziando a antiga posicao
                        copy_board[ogY][ogX] = empty
                        #verificando se eh possivel realizar os double jumps
                        dds = do_double_jumps_AI(current_player, copy_board, new_x, new_y)
                        #somando o retorno que vier de do_double_jumps_AI
                        score += dds
                        
                        verif_enemy = is_valid_enemy_move(copy_board, new_x, new_y)
                        #verificando se existe uma peca inimiga em uma das diagonais logo apos o movimento
                        if verif_enemy:
                            #somando -1 no score, porque provavelmente ira perder essa peca
                            score += -1
                        #adicionando essa jogada na lista com o score
                        succ.append([copy.deepcopy(copy_board),score])
                    
                score = 0
                #copia do tabuleiro
                copy_board = copy.deepcopy(board)
                #nova posicao de X e Y
                new_x = ogX-2
                new_y = ogY+2
                #if verificando se a nova posicao esta entre 10 e 0
                if new_x >= 10 or new_y >= 10:
                    pass
                elif new_x < 0 or new_y < 0:
                    pass 
                else:
                    verif = AI_move(current_player, copy_board, ogX, ogY, new_x, new_y, score)
                    #verificando se tem um inimigo um movimento antes e se eh possivel fazer o movimento
                    if (copy_board[ogY + 1][ogX - 1] is enemy['king'] or enemy['pawn']) and verif:
                        #somando +1 no score
                        score += 1
                        #movimentando a peca para a nova posicao
                        copy_board[new_y][new_x] = friendly['pawn']
                        #esvaziando a antiga posicao
                        copy_board[ogY][ogX] = empty
                        #verificando se eh possivel realizar os double jumps
                        dds = do_double_jumps_AI(current_player, copy_board, new_x, new_y)
                        #somando o retorno que vier de do_double_jumps_AI
                        score += dds
                        
                        verif_enemy = is_valid_enemy_move(copy_board, new_x, new_y)
                        #verificando se existe uma peca inimiga em uma das diagonais logo apos o movimento
                        if verif_enemy:
                            #somando -1 no score, porque provavelmente ira perder essa peca
                            score += -1
                        #adicionando essa jogada na lista com o score
                        succ.append([copy.deepcopy(copy_board),score])
                    
                score = 0
                #copia do tabuleiro
                copy_board = copy.deepcopy(board)
                #nova posicao de X e Y
                new_x = ogX+2
                new_y = ogY+2
                #if verificando se a nova posicao esta entre 10 e 0
                if new_x >= 10 or new_y >= 10:
                    pass
                elif new_x < 0 or new_y < 0:
                    pass 
                else:
                    verif = AI_move(current_player, copy_board, ogX, ogY, new_x, new_y, score)
                    #verificando se tem um inimigo um movimento antes e se eh possivel fazer o movimento
                    if (copy_board[ogY + 1][ogX + 1] is enemy['king'] or enemy['pawn']) and verif:
                        #somando +1 no score
                        score += 1
                        #movimentando a peca para a nova posicao
                        copy_board[new_y][new_x] = friendly['pawn']
                        #esvaziando a antiga posicao
                        copy_board[ogY][ogX] = empty
                        #verificando se eh possivel realizar os double jumps
                        dds = do_double_jumps_AI(current_player, copy_board, new_x, new_y)
                        #somando o retorno que vier de do_double_jumps_AI
                        score += dds
                    
                        verif_enemy = is_valid_enemy_move(copy_board, new_x, new_y)
                        #verificando se existe uma peca inimiga em uma das diagonais logo apos o movimento
                        if verif_enemy:
                            #somando -1 no score, porque provavelmente ira perder essa peca
                            score += -1
                        #adicionando essa jogada na lista com o score
                        succ.append([copy.deepcopy(copy_board),score])
                
                score = 0
                #copia do tabuleiro
                copy_board = copy.deepcopy(board)
                #nova posicao de X e Y
                new_x = ogX+1
                new_y = ogY-1
                #if verificando se a nova posicao esta entre 10 e 0
                if new_x >= 10 or new_y >= 10:
                    pass
                elif new_x < 0 or new_y < 0:
                    pass 
                else:
                    verif = AI_move(current_player, copy_board, ogX, ogY, new_x, new_y, score)
                    #verificando se eh possivel fazer o movimento
                    if verif:
                        #movimentando a peca para a nova posicao
                        copy_board[new_y][new_x] = friendly['pawn']
                        #esvaziando a antiga posicao
                        copy_board[ogY][ogX] = empty

                        verif_enemy = is_valid_enemy_move(copy_board, new_x, new_y)
                        #verificando se existe uma peca inimiga em uma das diagonais logo apos o movimento
                        if verif_enemy:
                            #somando -2 no score, porque provavelmente ira perder essa peca
                            score += -2
                        #adicionando essa jogada na lista com o score
                        succ.append([copy.deepcopy(copy_board),score])
                
                score = 0
                #copia do tabuleiro
                copy_board = copy.deepcopy(board)
                #nova posicao de X e Y
                new_x = ogX-1
                new_y = ogY-1
                #if verificando se a nova posicao esta entre 10 e 0
                if new_x >= 10 or new_y >= 10:
                    pass
                elif new_x < 0 or new_y < 0:
                    pass 
                else:
                    verif = AI_move(current_player, copy_board, ogX, ogY, new_x, new_y, score)
                    #verificando se eh possivel fazer o movimento
                    if verif:
                        #movimentando a peca para a nova posicao
                        copy_board[new_y][new_x] = friendly['pawn']
                        #esvaziando a antiga posicao
                        copy_board[ogY][ogX] = empty

                        verif_enemy = is_valid_enemy_move(copy_board, new_x, new_y)
                        #verificando se existe uma peca inimiga em uma das diagonais logo apos o movimento
                        if verif_enemy:
                            #somando -2 no score, porque provavelmente ira perder essa peca
                            score += -2
                        #adicionando essa jogada na lista com o score
                        succ.append([copy.deepcopy(copy_board),score])
            #caso IA seja Dama
            elif board[ogY][ogX] is friendly['king']:
                #copia do tabuleiro
                copy_board = copy.deepcopy(board)
                score = 0
                #for para movimentacao da dama
                for i in range(1,10):
                    #caso a posicao antiga menos i esteja entre 10 e 0
                    if (ogX-i < 10 or ogX-i >= 0 or ogY-i < 10 or ogY-i >= 0): 
                        #nova posicao de X e Y
                        new_x = ogX-i
                        new_y = ogY-i
                        #verificando se eh possivel fazer o movimento
                        if AI_move_king(current_player, copy_board, ogX, ogY, new_x, new_y, score):
                            #checando se exite um inimigo em uma das diagonais da dama
                            if copy_board[new_y+1][new_x+1] is enemy['pawn'] or enemy['king']:
                                #somando o score
                                score += 1
                                #verificando se eh possivel fazer o double jump
                                dds = do_double_jumps_AI(current_player, copy_board, new_x, new_y)
                                #somando o retorno de do_double_jumps_AI
                                score += dds
                            
                            verif_enemy = is_valid_enemy_move(copy_board,new_x,new_y)
                            #verificando se existe uma peca inimiga em uma das diagonais logo apos o movimento
                            if verif_enemy:
                                #somando -3 no score, porque provavelmente ira perder essa peca
                                #-3 porque perder uma dama eh muito grave
                                score += -3
                            #adicionando essa jogada na lista com o score
                            succ.append([copy.deepcopy(copy_board),score])
                
                #copia do tabuleiro
                copy_board = copy.deepcopy(board)
                score = 0
                #for para movimentacao da dama
                for i in range(1,10):
                    #caso a posicao antiga menos i esteja entre 10 e 0
                    if (ogX+i < 10 or ogX+i >= 0 or ogY-i < 10 or ogY-i >= 0): 
                        #nova posicao de X e Y
                        new_x = ogX+i
                        new_y = ogY-i
                        #verificando se eh possivel fazer o movimento
                        if AI_move_king(current_player, copy_board, ogX, ogY, new_x, new_y, score):
                            #checando se exite um inimigo em uma das diagonais da dama
                            if copy_board[new_y+1][new_x-1] is enemy['pawn'] or enemy['king']:
                                #somando o score
                                score += 1
                                #verificando se eh possivel fazer o double jump
                                dds = do_double_jumps_AI(current_player, copy_board, new_x, new_y)
                                #somando o retorno de do_double_jumps_AI
                                score += dds

                            verif_enemy = is_valid_enemy_move(copy_board,new_x,new_y)
                            #verificando se existe uma peca inimiga em uma das diagonais logo apos o movimento
                            if verif_enemy:
                                #somando -3 no score, porque provavelmente ira perder essa peca
                                #-3 porque perder uma dama eh muito grave
                                score += -3
                            #adicionando essa jogada na lista com o score
                            succ.append([copy.deepcopy(copy_board),score])

                #copia do tabuleiro
                copy_board = copy.deepcopy(board)
                score = 0
                #for para movimentacao da dama
                for i in range(1,10):
                    #caso a posicao antiga menos i esteja entre 10 e 0
                    if (ogX+i < 10 or ogX+i >= 0 or ogY+i < 10 or ogY+i >= 0): 
                        #nova posicao de X e Y
                        new_x = ogX+i
                        new_y = ogY+i
                        #verificando se eh possivel fazer o movimento
                        if AI_move_king(current_player, copy_board, ogX, ogY, new_x, new_y, score):
                            #checando se exite um inimigo em uma das diagonais da dama
                            if copy_board[new_y-1][new_x-1] is enemy['pawn'] or enemy['king']:
                                #somando o score
                                score += 1
                                #verificando se eh possivel fazer o double jump
                                dds = do_double_jumps_AI(current_player, copy_board, new_x, new_y)
                                #somando o retorno de do_double_jumps_AI
                                score += dds

                            verif_enemy = is_valid_enemy_move(copy_board,new_x,new_y)
                            #verificando se existe uma peca inimiga em uma das diagonais logo apos o movimento
                            if verif_enemy:
                                #somando -3 no score, porque provavelmente ira perder essa peca
                                #-3 porque perder uma dama eh muito grave
                                score += -3
                            #adicionando essa jogada na lista com o score
                            succ.append([copy.deepcopy(copy_board),score])
                
                #copia do tabuleiro
                copy_board = copy.deepcopy(board)
                score = 0
                #for para movimentacao da dama
                for i in range(1,10):
                    #caso a posicao antiga menos i esteja entre 10 e 0
                    if (ogX-i < 10 or ogX-i >= 0 or ogY+i < 10 or ogY+i >= 0): 
                        #nova posicao de X e Y
                        new_x = ogX-i
                        new_y = ogY+i
                        #verificando se eh possivel fazer o movimento
                        if AI_move_king(current_player, copy_board, ogX, ogY, new_x, new_y, score):
                            #checando se exite um inimigo em uma das diagonais da dama
                            if copy_board[new_y-1][new_x+1] is enemy['pawn'] or enemy['king']:
                                #somando o score
                                score += 1
                                #verificando se eh possivel fazer o double jump
                                dds = do_double_jumps_AI(current_player, copy_board, new_x, new_y)
                                #somando o retorno de do_double_jumps_AI
                                score += dds

                            verif_enemy = is_valid_enemy_move(copy_board,new_x,new_y)
                            #verificando se existe uma peca inimiga em uma das diagonais logo apos o movimento
                            if verif_enemy:
                                #somando -3 no score, porque provavelmente ira perder essa peca
                                #-3 porque perder uma dama eh muito grave
                                score += -3
                            #adicionando essa jogada na lista com o score
                            succ.append([copy.deepcopy(copy_board),score])
        '''# If AI is black then
        else:
            copy_board = copy.deepcopy(board)
            score = 0
            new_x = ogX-2
            new_y = ogY-2
            if new_x >= 10 or new_y >= 10:
                pass
            elif new_x < 0 or new_y < 0:
                pass 
            else:
                verif = AI_move(current_player, copy_board, ogX, ogY, new_x, new_y, score)
                if (copy_board[ogY - 1][ogX - 1] is enemy['pawn'] or enemy['king']) and verif:
                    score += 1
                    copy_board[new_y][new_x] = friendly['pawn']
                    copy_board[ogY][ogX] = empty
                    dds = do_double_jumps_AI(current_player, copy_board, new_x, new_y)
                    score += dds
                    
                    verif_enemy = is_valid_enemy_move(copy_board, new_x, new_y)
                    if verif_enemy:
                        score += -1
                    succ.append([copy.deepcopy(copy_board),score])
                 
            score = 0
            copy_board = copy.deepcopy(board)
            new_x = ogX+2
            new_y = ogY-2
            if new_x >= 10 or new_y >= 10:
                pass
            elif new_x < 0 or new_y < 0:
                pass 
            else:
                verif = AI_move(current_player, copy_board, ogX, ogY, new_x, new_y, score)
                if (copy_board[ogY - 1][ogX + 1] is enemy['pawn'] or enemy['king']) and verif:
                    score += 1
                    copy_board[new_y][new_x] = friendly['pawn']
                    copy_board[ogY][ogX] = empty
                    dds = do_double_jumps_AI(current_player, copy_board, new_x, new_y)
                    score += dds
                    
                    verif_enemy = is_valid_enemy_move(copy_board, new_x, new_y)
                    if verif_enemy:
                        score += -1
                    succ.append([copy.deepcopy(copy_board),score])
                
            score = 0
            copy_board = copy.deepcopy(board)
            new_x = ogX-2
            new_y = ogY+2
            if new_x >= 10 or new_y >= 10:
                pass
            elif new_x < 0 or new_y < 0:
                pass 
            else:
                verif = AI_move(current_player, copy_board, ogX, ogY, new_x, new_y, score)
                if (copy_board[ogY + 1][ogX - 1] is enemy['pawn'] or enemy['king']) and verif:
                    score += 1
                    copy_board[new_y][new_x] = friendly['pawn']
                    copy_board[ogY][ogX] = empty
                    dds = do_double_jumps_AI(current_player, copy_board, new_x, new_y)
                    score += dds
                    
                    verif_enemy = is_valid_enemy_move(copy_board, new_x, new_y)
                    if verif_enemy:
                        score += -1
                    succ.append([copy.deepcopy(copy_board),score])
                
            score = 0
            copy_board = copy.deepcopy(board)
            new_x = ogX+2
            new_y = ogY+2
            if new_x >= 10 or new_y >= 10:
                pass
            elif new_x < 0 or new_y < 0:
                pass 
            else:
                verif = AI_move(current_player, copy_board, ogX, ogY, new_x, new_y, score)
                if (copy_board[ogY + 1][ogX + 1] is enemy['pawn'] or enemy['king']) and verif:
                    score += 1
                    copy_board[new_y][new_x] = friendly['pawn']
                    copy_board[ogY][ogX] = empty
                    dds = do_double_jumps_AI(current_player, copy_board, new_x, new_y)
                    score += dds
                
                    verif_enemy = is_valid_enemy_move(copy_board, new_x, new_y)
                    if verif_enemy:
                        score += -1
                    succ.append([copy.deepcopy(copy_board),score])
            
            copy_board = copy.deepcopy(board)
            if copy_board[ogY][ogX] is 1:
                score = 0
                new_x = ogX+1
                new_y = ogY+1
                if new_x >= 10 or new_y >= 10:
                    pass
                elif new_x < 0 or new_y < 0:
                    pass 
                else:
                    verif = AI_move(current_player, copy_board, ogX, ogY, new_x, new_y, score)
                    if verif:
                        copy_board[new_y][new_x] = friendly['pawn']
                        copy_board[ogY][ogX] = empty
                        verif_enemy = is_valid_enemy_move(copy_board, new_x, new_y)
                        if verif_enemy:
                            score += -1
                        succ.append([copy.deepcopy(copy_board),score])

                score = 0
                copy_board = copy.deepcopy(board)
                new_x = ogX-1
                new_y = ogY+1
                if new_x >= 10 or new_y >= 10:
                    pass
                elif new_x < 0 or new_y < 0:
                    pass 
                else:
                    verif = AI_move(current_player, copy_board, ogX, ogY, new_x, new_y, score)
                    if verif:
                        copy_board[new_y][new_x] = friendly['pawn']
                        copy_board[ogY][ogX] = empty
                        verif_enemy = is_valid_enemy_move(copy_board, new_x, new_y)
                        if verif_enemy:
                            score += -1
                        succ.append([copy.deepcopy(copy_board),score])
    '''
    succ.sort(key = operator.itemgetter(1))
    '''for i in succ:
        for j in i:
            print("===========================")
            for y in i[0]:
                print(y)
            print("Valor: ",i[1])'''

    return succ

#funcao para movimentacao da dama
def AI_move_king(current_player, board, old_x, old_y, new_x, new_y, score):
    try:
        """All logic for king pieces"""
        # Prevents player from jumping onto another player
        if board[new_y][new_x] != empty:
            return False
        # Prevent horizontal moves
        if new_y is old_y:
            return False
        # Prevent vertical moves
        if new_x is old_x:
            return False

        # Prevent moves that do not have a slope of 1
        if new_x > old_x and new_y > old_y:
            if (new_x - old_x) != (new_y - old_y):
                return False
        if new_x < old_x and new_y < old_y:
            if (old_x - new_x) != (old_y - new_y):
                return False
        if new_x < old_x and new_y > old_y:
            if (old_x - new_x) != (new_y - old_y):
                return False
        if new_x > old_x and new_y < old_y:
            if (new_x - old_x) != (old_y - new_y):
                return False


        # King Jump Logic
        if board[old_y][old_x] is friendly['king']:
            try: # North East Jump
                if board[new_y + 1][new_x - 1] is enemy['pawn'] or enemy['king']:
                    if old_x < new_x and old_y > new_y:
                        if no_chips_between(board, old_x, old_y, new_x, new_y):
                            if board[new_y + 1][new_x - 1] is enemy['king']:
                                score += 3
                            else:
                                score += 1
                            board[new_y][new_x] = friendly['king']
                            board[new_y + 1][new_x - 1] = empty
                            board_selection = empty
                            return True
            except IndexError:
                pass
            try: # North West Jump 
                if board[new_y + 1][new_x + 1] is enemy['pawn'] or enemy['king']:
                    if old_x > new_x and old_y > new_y:
                        if no_chips_between(board, old_x, old_y, new_x, new_y) is True:
                            if board[new_y + 1][new_x + 1] is enemy['king']:
                                score += 3
                            else:
                                score += 1
                            board[new_y][new_x] = friendly['king']
                            board[new_y + 1][new_x + 1] = empty
                            board_selection = empty
                            return True
            except IndexError:
                pass
            try: # South East Jump
                if board[new_y - 1][new_x - 1] is enemy['pawn'] or enemy['king']:
                    if no_chips_between(board, old_x, old_y, new_x, new_y) is True:
                        if old_x < new_x and old_y < new_y:
                            if board[new_y - 1][new_x - 1] is enemy['king']:
                                score += 3
                            else:
                                score += 1
                            board[new_y][new_x] = friendly['king']
                            board[new_y - 1][new_x - 1] = empty
                            board_selection = empty
                            return True
            except IndexError:
                pass
            try: # South West Jump
                if board[new_y - 1][new_x + 1] is enemy['pawn'] or enemy['pawn']:
                    if no_chips_between(board, old_x, old_y, new_x, new_y) is True:
                        if old_x > new_x and old_y < new_y:
                            if board[new_y - 1][new_x + 1] is enemy['king']:
                                score += 3
                            else:
                                score += 1
                            board[new_y][new_x] = friendly['king']
                            board[new_y - 1][new_x + 1] = empty
                            board_selection = empty
                            return True
            except IndexError:
                pass
            try:
                if no_chips_between(board, old_x, old_y, new_x, new_y) is True:
                    if old_x > new_x and old_y < new_y:
                        board[new_y][new_x] = friendly['king']
                        board_selection = empty
                        return True
            except IndexError:
                pass

        return False
    except IndexError:
        return False


def alpha_beta(current_player, board, game_over): # retorna a melhor jogada
    print("alpha beta")
    copy_board = copy.deepcopy(board)
    alpha = -infinity
    beta = infinity
    tab = VALOR_MAX(current_player, copy_board, alpha, beta, game_over)
    print("======retorno========")
    for i in tab:
        print(i)
    return tab
    

def VALOR_MAX(current_player, board, alpha, beta, game_over):
    if check_for_win(current_player, board):
        return board
    v = -infinity
    succ = successors(current_player, board, game_over)
    mat = []
    for s in succ:
        mat = []
        mat = VALOR_MIN(current_player, s, alpha, beta, game_over)
        v = max(v, s[1])
        if v >= beta:
            return mat
        alpha = max(alpha, v)
    return mat


def VALOR_MIN(current_player, state, alpha, beta, game_over):
    if check_for_win(current_player, board):
        return board
    v = infinity
    mat = state[0]
    v = min(v, state[1])
    if v <= alpha:
        return mat
    beta = min(beta, v)
    return mat

#funcao que verifica se eh possivel movimentar a peca para a nova posicao
def AI_move(current_player, board, old_x, old_y, new_x, new_y, score):
    try:
        #checa se a nova posicao esta vazia
        if board[new_y][new_x] != empty:
            return False
    except IndexError:
        return False

    # Checking for valid moves for Player 1
    if board[old_y][old_x] is 1:
        try:
            #checando se o novo movimento eh possivel. Movimento de tomada 
            if (new_y - old_y) is -2 and (new_x - old_x) is 2:
                #verificando se um movimento antes do de tomada existe inimigo
                if board[new_y + 1][new_x - 1] is (enemy['pawn'] or enemy['king']):
                    #esvaziando a casa onde tinha o inimigo
                    board[new_y + 1][new_x - 1] = empty
                    return True
        except IndexError:
            pass
        try:
            #checando se o novo movimento eh possivel. Movimento de tomada
            if (new_y - old_y) is -2 and (new_x - old_x) is -2:
                #verificando se um movimento antes do de tomada existe inimigo
                if board[new_y + 1][new_x + 1] is (enemy['pawn'] or enemy['king']):
                    #esvaziando a casa onde tinha o inimigo
                    board[new_y + 1][new_x + 1] = empty
                    return True
        except IndexError:
            pass
        try:
            #checando se o novo movimento eh possivel. Movimento de tomada
            if (new_y - old_y) is 2 and (new_x - old_x) is -2:
                #verificando se um movimento antes do de tomada existe inimigo
                if board[new_y - 1][new_x + 1] is (enemy['pawn'] or enemy['king']):
                    #esvaziando a casa onde tinha o inimigo
                    board[new_y - 1][new_x + 1] = empty
                    return True
        except IndexError:
            pass
        try:
            #checando se o novo movimento eh possivel. Movimento de tomada
            if (new_y - old_y) is 2 and (new_x - old_x) is 2:
                #verificando se um movimento antes do de tomada existe inimigo
                if board[new_y - 1][new_x - 1] is (enemy['pawn'] or enemy['king']):
                    #esvaziando a casa onde tinha o inimigo
                    board[new_y - 1][new_x - 1] = empty
                    return True
        except IndexError:
            pass
        try:
            #checando se o novo movimento eh possivel. Avanco de casa
            if (new_y - old_y) is -1 and (new_x - old_x) is 1:
                return True
        except IndexError:
            pass
        try:
            #checando se o novo movimento eh possivel. Avanco de casa
            if (new_y - old_y) is -1 and (new_x - old_x) is -1:
                return True
        except IndexError:
            return False
        
    '''   
    # Checking for valid moves for Player 2
    elif board[old_y][old_x] is 2:
        try:
            if (new_y - old_y) is -2 and (new_x - old_x) is 2:
                if board[new_y + 1][new_x - 1] is (enemy['pawn'] or enemy['king']):
                    board[new_y + 1][new_x - 1] = empty
                    return True
        except IndexError:
            pass
        try:
            if (new_y - old_y) is -2 and (new_x - old_x) is -2:
                if board[new_y + 1][new_x + 1] is (enemy['pawn'] or enemy['king']):
                    board[new_y + 1][new_x + 1] = empty
                    return True
        except IndexError:
            pass
        try:
            if (new_y - old_y) is 2 and (new_x - old_x) is -2:
                if board[new_y - 1][new_x + 1] is (enemy['pawn'] or enemy['king']):
                    board[new_y - 1][new_x + 1] = empty
                    return True
        except IndexError:
            pass
        try:
            if (new_y - old_y) is 2 and (new_x - old_x) is 2:
                if board[new_y - 1][new_x - 1] is (enemy['pawn'] or enemy['king']):
                    board[new_y - 1][new_x - 1] = empty
                    return True
        except IndexError:
            pass
        try:
            if (new_y - old_y) is 1 and (new_x - old_x) is 1:
                return True
        except IndexError:
            pass
        try:
            if (new_y - old_y) is 1 and (new_x - old_x) is -1:
                return True
        except IndexError:
            return False
    '''

#funcao que retorna se eh possivel realizar o double jump
def AI_move_double(current_player, board, old_x, old_y, new_x, new_y):
    #checa se a nova posicao esta vazia
    if board[new_y][new_x] != empty:
        return False

    #checando se o movimento de double jump eh possivel para player 1
    if board[old_y][old_x] is 1 or 3:
        #verificando se o movimento eh de tomada de peca
        if (new_y - old_y) is 2 and (new_x - old_x) is -2:
            #vendo de na nova posicao + 1 em X esat entre 10 e 0 e se - 1 em Y esta entre 10 e 0
            if (new_x + 1< 10 and new_x + 1>= 0) and (new_y - 1 < 10 and new_y - 1 >= 0):
                #checando se na diagonal existe uma peca inimiga
                if board[new_y - 1][new_x + 1] is (enemy['pawn'] or enemy['king']):
                    #jah esta deixando a posicao do inimigo vazia porque a IA ira fazer esse movimento
                    board[new_y - 1][new_x + 1] = empty
                    return True
        #verificando se o movimento eh de tomada de peca
        if (new_y - old_y) is 2 and (new_x - old_x) is 2:
            #vendo de na nova posicao - 1 em X esat entre 10 e 0 e se - 1 em Y esta entre 10 e 0
            if (new_x - 1< 10 and new_x - 1>= 0) and (new_y - 1 < 10 and new_y - 1 >= 0):    
                #checando se na diagonal existe uma peca inimiga
                if board[new_y - 1][new_x - 1] is (enemy['pawn'] or enemy['king']):
                    #jah esta deixando a posicao do inimigo vazia porque a IA ira fazer esse movimento
                    board[new_y - 1][new_x - 1] = empty
                    return True
        #verificando se o movimento eh de tomada de peca
        if (new_y - old_y) is -2 and (new_x - old_x) is 2:
            #vendo de na nova posicao - 1 em X esat entre 10 e 0 e se + 1 em Y esta entre 10 e 0
            if (new_x - 1< 10 and new_x - 1>= 0) and (new_y + 1 < 10 and new_y + 1 >= 0):
                #checando se na diagonal existe uma peca inimiga
                if board[new_y + 1][new_x - 1] is (enemy['pawn'] or enemy['king']):
                    #jah esta deixando a posicao do inimigo vazia porque a IA ira fazer esse movimento
                    board[new_y + 1][new_x - 1] = empty
                    return True
        #verificando se o movimento eh de tomada de peca
        if (new_y - old_y) is -2 and (new_x - old_x) is -2:
            #vendo de na nova posicao + 1 em X esat entre 10 e 0 e se + 1 em Y esta entre 10 e 0
            if (new_x + 1< 10 and new_x + 1>= 0) and (new_y + 1 < 10 and new_y + 1 >= 0):
                #checando se na diagonal existe uma peca inimiga
                if board[new_y + 1][new_x + 1] is (enemy['pawn'] or enemy['king']):
                    #jah esta deixando a posicao do inimigo vazia porque a IA ira fazer esse movimento
                    board[new_y + 1][new_x + 1] = empty
                    return True
        else:
            return False

#funcao que realiza o double jump
def do_double_jumps_AI(current_player, board, new_x, new_y):
    score = 0
    #checando se a peca eh um peao
    if board[new_x][new_y] is friendly["pawn"]:
        try:
            ogX = new_x
            ogY = new_y
            
            #newX recebendo uma nova possibilidade de posicao no eixo X
            #newY recebendo uma nova possibilidade de posicao no eixo Y
            #movimentacao de tomada de peca para cima e para esquerda
            newX = ogX - 2
            newY = ogY - 2
            #checando newX e newY esta entre 10 e 0
            if (newX < 10 and newX >= 0) and (newY < 10 and newY >= 0):
                #checando se eh possivel fazer a movimentacao de tomada, caso exista um inimigo entao ele ira tomar a peca
                if (board[ogY - 1][ogX - 1] is enemy['pawn'] or enemy['king']) and AI_move_double(current_player, board, ogX, ogY, newX, newY):
                    #somando +2 no score na IA
                    score += 2
                    new_x = newX
                    new_y = newY
                    #falando para IA se movimentar para o local
                    board[new_y][new_x] = friendly['pawn']
                    #e deixando a posicao antiga vazia
                    board[ogY][ogX] = empty
                    return int(score)
            
            #newX recebendo uma nova possibilidade de posicao no eixo X
            #newY recebendo uma nova possibilidade de posicao no eixo Y
            #movimentacao de tomada de peca para cima e para direita
            newX = ogX + 2
            newY = ogY - 2
            #checando newX e newY esta entre 10 e 0
            if (newX < 10 and newX >= 0) and (newY < 10 and newY >= 0):    
                #checando se eh possivel fazer a movimentacao de tomada, caso exista um inimigo entao ele ira tomar a peca
                if (board[ogY - 1][ogX + 1] is enemy['pawn'] or enemy['king']) and AI_move_double(current_player, board, ogX, ogY, newX, newY):
                    #somando +2 no score na IA
                    score += 2
                    new_x = newX
                    new_y = newY
                    #falando para IA se movimentar para o local
                    board[new_y][new_x] = friendly['pawn']
                    #e deixando a posicao antiga vazia
                    board[ogY][ogX] = empty
                    return int(score)
                
            #newX recebendo uma nova possibilidade de posicao no eixo X
            #newY recebendo uma nova possibilidade de posicao no eixo Y
            #movimentacao de tomada de peca para baixo e para esquerda
            newX = ogX - 2
            newY = ogY + 2
            #checando newX e newY esta entre 10 e 0
            if (newX < 10 and newX >= 0) and (newY < 10 and newY >= 0):   
                #checando se eh possivel fazer a movimentacao de tomada, caso exista um inimigo entao ele ira tomar a peca 
                if (board[ogY + 1][ogX - 1] is enemy['pawn'] or enemy['king']) and AI_move_double(current_player, board, ogX, ogY, newX, newY):
                    #somando +2 no score na IA
                    score += 2
                    new_x = newX
                    new_y = newY
                    #falando para IA se movimentar para o local
                    board[new_y][new_x] = friendly['pawn']
                    #e deixando a posicao antiga vazia
                    board[ogY][ogX] = empty
                    return int(score)
                
            #newX recebendo uma nova possibilidade de posicao no eixo X
            #newY recebendo uma nova possibilidade de posicao no eixo Y
            #movimentacao de tomada de peca para baixo e para direita
            newX = ogX + 2
            newY = ogY + 2
            #checando newX e newY esta entre 10 e 0
            if (newX < 10 and newX >= 0) and (newY < 10 and newY >= 0):  
                #checando se eh possivel fazer a movimentacao de tomada, caso exista um inimigo entao ele ira tomar a peca
                if (board[ogY + 1][ogX + 1] is enemy['pawn'] or enemy['king']) and AI_move_double(current_player, board, ogX, ogY, newX, newY):
                    #somando +2 no score na IA
                    score += 2
                    new_x = newX
                    new_y = newY
                    #falando para IA se movimentar para o local
                    board[new_y][new_x] = friendly['pawn']
                    #e deixando a posicao antiga vazia
                    board[ogY][ogX] = empty
                    return int(score)
            return int(score)
        except IndexError as error:
            print("Erro -> ", error)
            pass
    #checando se a peca eh uma dama
    #OBS: a atitude de double jump da dama eh igual a do peao
    elif board[new_x][new_y] is friendly["king"]:
        try:
            ogX = new_x
            ogY = new_y
            
            #newX recebendo uma nova possibilidade de posicao no eixo X
            #newY recebendo uma nova possibilidade de posicao no eixo Y
            #movimentacao de tomada de peca para cima e para esquerda
            newX = ogX - 2
            newY = ogY - 2
            #checando newX e newY esta entre 10 e 0
            if (newX < 10 and newX >= 0) and (newY < 10 and newY >= 0):
                #checando se eh possivel fazer a movimentacao de tomada, caso exista um inimigo entao ele ira tomar a peca
                if (board[ogY - 1][ogX - 1] is enemy['pawn'] or enemy['king']) and AI_move_double(current_player, board, ogX, ogY, newX, newY):
                    #somando +2 no score na IA
                    score += 2
                    new_x = newX
                    new_y = newY
                    #falando para IA se movimentar para o local
                    board[new_y][new_x] = friendly['king']
                    #e deixando a posicao antiga vazia
                    board[ogY][ogX] = empty
                    return int(score)
            
            #newX recebendo uma nova possibilidade de posicao no eixo X
            #newY recebendo uma nova possibilidade de posicao no eixo Y
            #movimentacao de tomada de peca para cima e para direita
            newX = ogX + 2
            newY = ogY - 2
            #checando newX e newY esta entre 10 e 0
            if (newX < 10 and newX >= 0) and (newY < 10 and newY >= 0):    
                #checando se eh possivel fazer a movimentacao de tomada, caso exista um inimigo entao ele ira tomar a peca
                if (board[ogY - 1][ogX + 1] is enemy['pawn'] or enemy['king']) and AI_move_double(current_player, board, ogX, ogY, newX, newY):
                    #somando +2 no score na IA
                    score += 2
                    new_x = newX
                    new_y = newY
                    #falando para IA se movimentar para o local
                    board[new_y][new_x] = friendly['king']
                    #e deixando a posicao antiga vazia
                    board[ogY][ogX] = empty
                    return int(score)

            #newX recebendo uma nova possibilidade de posicao no eixo X
            #newY recebendo uma nova possibilidade de posicao no eixo Y
            #movimentacao de tomada de peca para baixo e para esquerda  
            newX = ogX - 2
            newY = ogY + 2
            #checando newX e newY esta entre 10 e 0
            if (newX < 10 and newX >= 0) and (newY < 10 and newY >= 0):   
                #checando se eh possivel fazer a movimentacao de tomada, caso exista um inimigo entao ele ira tomar a peca 
                if (board[ogY + 1][ogX - 1] is enemy['pawn'] or enemy['king']) and AI_move_double(current_player, board, ogX, ogY, newX, newY):
                    #somando +2 no score na IA
                    score += 2
                    new_x = newX
                    new_y = newY
                    #falando para IA se movimentar para o local
                    board[new_y][new_x] = friendly['king']
                    #e deixando a posicao antiga vazia
                    board[ogY][ogX] = empty
                    return int(score)
                
            #newX recebendo uma nova possibilidade de posicao no eixo X
            #newY recebendo uma nova possibilidade de posicao no eixo Y
            #movimentacao de tomada de peca para baixo e para direita
            newX = ogX + 2
            newY = ogY + 2
            #checando newX e newY esta entre 10 e 0
            if (newX < 10 and newX >= 0) and (newY < 10 and newY >= 0):  
                #checando se eh possivel fazer a movimentacao de tomada, caso exista um inimigo entao ele ira tomar a peca
                if (board[ogY + 1][ogX + 1] is enemy['pawn'] or enemy['king']) and AI_move_double(current_player, board, ogX, ogY, newX, newY):
                    #somando +2 no score na IA
                    score += 2
                    new_x = newX
                    new_y = newY
                    #falando para IA se movimentar para o local
                    board[new_y][new_x] = friendly['king']
                    #e deixando a posicao antiga vazia
                    board[ogY][ogX] = empty
                    return int(score)
            return int(score)
        except IndexError as error:
            print("Erro -> ", error)
            pass
    return score

# Initalize vairables

board = create_board()
place_starting_pieces()

# Initalize pygame
pygame.init()

# Set the height and width of the screen
window_size = [600, 600]
screen = pygame.display.set_mode(window_size)

# Set title of screen
pygame.display.set_caption("Checkers")

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
dark_red = (139 , 0, 0)
grey = (128, 128, 128)
gold = (255, 215, 0)

# This sets the width, height and margin of each board cell
window_width = window_size[0]
window_height = window_size[1]
total_rows = 10
total_columns = 10
width = (window_width // total_columns)
height = (window_height // total_rows)

# Set the radius and border border of each checker piece
radius = (window_width // 20)
border = (window_width // 200)

# Current player turn
current_player = 1
print("White's Turn") # Printing at start of the game before main loop

'''
# Main active game loop
while not game_over:
    for event in pygame.event.get():  # User did something
        mouse_pos = pygame.mouse.get_pos()
        mouse_matrix_pos = ((mouse_pos[0] // width), (mouse_pos[1] // height)) # Matrix Cordinates of Mouse posisiton
        # print(mouse_matrix_pos)
        
        if event.type is pygame.QUIT:  # If user clicked close
            game_over = True  # Flag that the user has quit so we exit this loop


        elif event.type is pygame.MOUSEBUTTONDOWN:
            current_pos = pygame.mouse.get_pos()
            # Translating mouse x, y screen coordinates to matrix coordinates
            old_x = (current_pos[0] // width)
            old_y = (current_pos[1] // height)
            # print(f"Old coordinates: [{old_x}, {old_y}]")


            # I didn't know about classes at all when I first started working on this project so
            # I've taken an easy but pretty sloppy approach to decided if a jump has occured
            # or not.
            previous_piece_total = sum([sum(row) for row in board])

            if is_valid_selection(board, current_player, old_x, old_y):
                pass # Do nothing if player has made a valid selection
            else:
                continue # Looping indefintely until a valid choice has been selected by the current player

            while True:
                event = pygame.event.wait()
                if event.type is pygame.QUIT:
                    game_over = True
                elif event.type is pygame.MOUSEBUTTONUP:
                    new_pos = pygame.mouse.get_pos()
                    # Translating mouse x, y screen coordinates to matrix coordinates
                    new_x = (new_pos[0] // width)
                    new_y = (new_pos[1] // height)
                    # print(f"New coordinates: [{new_x}, {new_y}]")

                    if board[old_y][old_x] is friendly['pawn']:
                        if is_valid_move(current_player, board, old_x, old_y, new_x, new_y):
                            board[new_y][new_x] = friendly['pawn']
                            board[old_y][old_x] = empty

                            if check_for_win(current_player, board):
                                game_over = True

                            # If the total amount of chips has changed and a double
                            # jump opportunity is available do not switch sides.
                            current_piece_total = sum([sum(row) for row in board])

                            if previous_piece_total > current_piece_total:
                                
                                do_double_jumps(current_player, board, new_x, new_y, game_over)
                            
                                # Swap sides
                                if current_player is 1:
                                    current_player = 2
                                    print("Black's Turn")
                                else:
                                    current_player = 1
                                    print("White's Turn")

                                friendly, enemy = enemy, friendly
                            else:
                                # Swap sides
                                if current_player is 1:
                                    current_player = 2
                                    print("Black's Turn")
                                else:
                                    current_player = 1
                                    print("White's Turn")

                                friendly, enemy = enemy, friendly

                    if board[old_y][old_x] is (friendly['king']):
                        if is_valid_king_move(current_player, board, old_x, old_y, new_x, new_y):

                            if check_for_win(current_player, board):
                                game_over = True

                            # If the total amount of chips has changed and a double
                            # jump opportunity is available do not switch sides.
                            current_piece_total = sum([sum(row) for row in board])

                            if previous_piece_total > current_piece_total:
                                
                                do_double_jumps(current_player, board, new_x, new_y, game_over)

                                # Swap sides
                                if current_player is 1:
                                    current_player = 2
                                    print("Black's Turn")
                                else:
                                    current_player = 1
                                    print("White's Turn")

                                friendly, enemy = enemy, friendly
                            else:
                                # Swap sides
                                if current_player is 1:
                                    current_player = 2
                                    print("Black's Turn")
                                else:
                                    current_player = 1
                                    print("White's Turn")

                                friendly, enemy = enemy, friendly

                    # Turn player into king if they make it to the opposite side of the board
                    for row in range(10):
                        for column in range(10):
                            # Checking for player 1 king pieces
                            if board[0][column] == 1:
                                board[0][column] = 3
                             # Cecking for player 2 king pieces
                            elif board[9][column] == 2:
                                board[9][column] = 4
                    break

    # Limit to 60 frames per second
    clock.tick(60)

    # Draw onto screen
    draw_board(board)

    # Update screen with what we drew
    pygame.display.flip()
'''

while not game_over:
    if player is 2:
        if current_player is 1:
            #chamando o algoritmo da IA que retorna a jogada
            tab = alpha_beta(current_player, board, game_over)
            #fazendo a jogada
            board = tab
            #verificando se alguma peca chegou ao outro lado para virar dama
            for row in range(10):
                for column in range(10):
                    # Checking for player 1 king pieces
                    if board[0][column] is friendly['pawn']:
                        board[0][column] = friendly['king']
            #60 fps
            clock.tick(60)
            #desenhando o quadro                
            draw_board(board)
            pygame.display.flip()
            #mudando de jogador da IA pro usuario
            if current_player is 1:
                current_player = 2
                print("Black's Turn")
            else:
                current_player = 1
                print("White's Turn")
            friendly, enemy = enemy, friendly
            

        for event in pygame.event.get():  # User did something
            
            mouse_pos = pygame.mouse.get_pos()
            mouse_matrix_pos = ((mouse_pos[0] // width), (mouse_pos[1] // height)) # Matrix Cordinates of Mouse posisiton
            # print(mouse_matrix_pos)
            
            if event.type is pygame.QUIT:  # If user clicked close
                game_over = True  # Flag that the user has quit so we exit this loop


            elif event.type is pygame.MOUSEBUTTONDOWN:
                current_pos = pygame.mouse.get_pos()
                # Translating mouse x, y screen coordinates to matrix coordinates
                old_x = (current_pos[0] // width)
                old_y = (current_pos[1] // height)
                # print(f"Old coordinates: [{old_x}, {old_y}]")


                # I didn't know about classes at all when I first started working on this project so
                # I've taken an easy but pretty sloppy approach to decided if a jump has occured
                # or not.
                previous_piece_total = sum([sum(row) for row in board])

                if is_valid_selection(board, current_player, old_x, old_y):
                    pass # Do nothing if player has made a valid selection
                else:
                    continue # Looping indefintely until a valid choice has been selected by the current player

                while True:
                    event = pygame.event.wait()
                    if event.type is pygame.QUIT:
                        game_over = True
                    elif event.type is pygame.MOUSEBUTTONUP:
                        new_pos = pygame.mouse.get_pos()
                        # Translating mouse x, y screen coordinates to matrix coordinates
                        new_x = (new_pos[0] // width)
                        new_y = (new_pos[1] // height)
                        # print(f"New coordinates: [{new_x}, {new_y}]")

                        if board[old_y][old_x] is friendly['pawn']:
                            if is_valid_move(current_player, board, old_x, old_y, new_x, new_y):
                                board[new_y][new_x] = friendly['pawn']
                                board[old_y][old_x] = empty

                                if check_for_win(current_player, board):
                                    game_over = True

                                # If the total amount of chips has changed and a double
                                # jump opportunity is available do not switch sides.
                                current_piece_total = sum([sum(row) for row in board])

                                if previous_piece_total > current_piece_total:
                                    
                                    do_double_jumps(current_player, board, new_x, new_y, game_over)
                                
                                    # Swap sides
                                    if current_player is 1:
                                        current_player = 2
                                        print("Black's Turn")
                                    else:
                                        current_player = 1
                                        print("White's Turn")

                                    friendly, enemy = enemy, friendly
                                else:
                                    # Swap sides
                                    if current_player is 1:
                                        current_player = 2
                                        print("Black's Turn")
                                    else:
                                        current_player = 1
                                        print("White's Turn")

                                    friendly, enemy = enemy, friendly

                        if board[old_y][old_x] is (friendly['king']):
                            if is_valid_king_move(current_player, board, old_x, old_y, new_x, new_y):

                                if check_for_win(current_player, board):
                                    game_over = True

                                # If the total amount of chips has changed and a double
                                # jump opportunity is available do not switch sides.
                                current_piece_total = sum([sum(row) for row in board])

                                if previous_piece_total > current_piece_total:
                                    
                                    do_double_jumps(current_player, board, new_x, new_y, game_over)

                                    # Swap sides
                                    if current_player is 1:
                                        current_player = 2
                                        print("Black's Turn")
                                    else:
                                        current_player = 1
                                        print("White's Turn")

                                    friendly, enemy = enemy, friendly
                                else:
                                    # Swap sides
                                    if current_player is 1:
                                        current_player = 2
                                        print("Black's Turn")
                                    else:
                                        current_player = 1
                                        print("White's Turn")

                                    friendly, enemy = enemy, friendly

                        # Turn player into king if they make it to the opposite side of the board
                        for row in range(10):
                            for column in range(10):
                                # Checking for player 1 king pieces
                                if board[0][column] == 1:
                                    board[0][column] = 3
                                # Cecking for player 2 king pieces
                                elif board[9][column] == 2:
                                    board[9][column] = 4
                        break
     
    # Limit to 60 frames per second
    #clock.tick(60)

    # Draw onto screen
    #draw_board(board)

    # Update screen with what we drew
    #pygame.display.flip()

# Exit the game
pygame.quit()