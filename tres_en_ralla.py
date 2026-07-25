import os
import random
import time
import sys

COLORS = {
    'reset': '\033[0m',
    'cyan': '\033[96m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'magenta': '\033[95m',
    'red': '\033[91m',
    'bold': '\033[1m',
}

BOARD_TEMPLATE = [
    ' {0} | {1} | {2} ',
    '---+---+---',
    ' {3} | {4} | {5} ',
    '---+---+---',
    ' {6} | {7} | {8} '
]

WIN_PATTERNS = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
]


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def color(text: str, shade: str) -> str:
    if sys.platform.startswith('win'):
        return text
    return COLORS.get(shade, '') + text + COLORS['reset']


def animated_print(message: str, delay: float = 0.01) -> None:
    for char in message:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


def draw_board(board: list[str]) -> None:
    clear_screen()
    palette = [
        color(board[i], 'cyan') if board[i] == 'X' else
        color(board[i], 'magenta') if board[i] == 'O' else
        color(board[i], 'yellow')
        for i in range(9)
    ]
    for line in BOARD_TEMPLATE:
        print(line.format(*palette))
    print()


def get_player_move(board: list[str], player_symbol: str) -> int:
    while True:
        try:
            value = input(color(f'Jugador {player_symbol}, elige una casilla (1-9): ', 'bold'))
            index = int(value.strip()) - 1
            if index < 0 or index >= 9:
                raise ValueError()
            if board[index] != ' ':
                print(color('La casilla ya está ocupada. Intenta otra vez.', 'red'))
                continue
            return index
        except ValueError:
            print(color('Entrada inválida. Usa un número entre 1 y 9.', 'red'))


def available_moves(board: list[str]) -> list[int]:
    return [index for index, cell in enumerate(board) if cell == ' ']


def check_winner(board: list[str]) -> str | None:
    for a, b, c in WIN_PATTERNS:
        if board[a] == board[b] == board[c] and board[a] != ' ':
            return board[a]
    return None


def check_draw(board: list[str]) -> bool:
    return ' ' not in board and check_winner(board) is None


def prompt_mode() -> str:
    while True:
        print(color('Modo de juego:', 'bold'))
        print(' 1. Jugador vs Jugador')
        print(' 2. Jugador vs CPU')
        modo = input(color('Selecciona opción (1 o 2): ', 'green'))
        if modo in {'1', '2'}:
            return modo
        print(color('Opción inválida, prueba nuevamente.', 'red'))


def prompt_symbols() -> tuple[str, str]:
    print(color('Puedes usar los símbolos clásicos o personalizar los tuyos.', 'bold'))
    x = input('Símbolo para el primer jugador [X]: ').strip() or 'X'
    o = input('Símbolo para el segundo jugador [O]: ').strip() or 'O'
    if x == o:
        o = 'O' if x != 'O' else 'X'
    print(color(f'Jugador 1: {x}   Jugador 2/CPU: {o}', 'cyan'))
    time.sleep(0.8)
    return x[:1].upper(), o[:1].upper()


def cpu_best_move(board: list[str], cpu_symbol: str, human_symbol: str) -> int:
    for symbol in (cpu_symbol, human_symbol):
        for index in available_moves(board):
            candidate = board.copy()
            candidate[index] = symbol
            if check_winner(candidate) == symbol:
                return index
    corners = [i for i in [0, 2, 6, 8] if board[i] == ' ']
    if corners:
        return random.choice(corners)
    if board[4] == ' ':
        return 4
    return random.choice(available_moves(board))


def play_round(board: list[str], mode: str, symbols: tuple[str, str]) -> str:
    current_symbol = symbols[0]
    human_symbol, cpu_symbol = symbols[0], symbols[1]
    while True:
        draw_board(board)
        if mode == '2' and current_symbol == cpu_symbol:
            animated_print(color('CPU está pensando...', 'yellow'), delay=0.02)
            move = cpu_best_move(board, cpu_symbol, human_symbol)
        else:
            move = get_player_move(board, current_symbol)
        board[move] = current_symbol
        winner = check_winner(board)
        if winner:
            draw_board(board)
            return winner
        if check_draw(board):
            draw_board(board)
            return 'EMPATE'
        current_symbol = symbols[1] if current_symbol == symbols[0] else symbols[0]


def ask_yes_no(message: str) -> bool:
    while True:
        answer = input(color(f'{message} (s/n): ', 'green')).strip().lower()
        if answer in {'s', 'si', 'y', 'yes'}:
            return True
        if answer in {'n', 'no'}:
            return False
        print(color('Responde con s o n.', 'red'))


def show_welcome() -> None:
    clear_screen()
    print(color('╔════════════════════════════════╗', 'magenta'))
    print(color('║      3 EN RAYA AVANZADO       ║', 'magenta'))
    print(color('╠════════════════════════════════╣', 'magenta'))
    print(color('║   Juego dinámico, moderno y    ║', 'magenta'))
    print(color('║   diseñado con funciones       ║', 'magenta'))
    print(color('╚════════════════════════════════╝', 'magenta'))
    print()
    animated_print(color('Bienvenido. Controla el tablero con números del 1 al 9.', 'cyan'), delay=0.01)
    print(color('Formato de casillas:', 'bold'))
    for index in range(1, 10):
        print(color(str(index), 'yellow'), end=' ')
        if index % 3 == 0:
            print()
    print()
    time.sleep(1)


def main() -> None:
    show_welcome()
    mode = prompt_mode()
    symbols = prompt_symbols()
    scores = {'X': 0, 'O': 0, 'EMPATE': 0}

    while True:
        board = [' '] * 9
        winner = play_round(board, mode, symbols)
        if winner == 'EMPATE':
            animated_print(color('¡Nadie ganó esta vez! Empate dinámico.', 'yellow'))
        else:
            animated_print(color(f'¡Ha ganado {winner}!', 'green'))
        scores[winner] += 1
        print(color('Marcador:', 'bold'))
        print(color(f'  {symbols[0]} = {scores[symbols[0]]}', 'cyan'))
        print(color(f'  {symbols[1]} = {scores[symbols[1]]}', 'magenta'))
        print(color(f'  Empates = {scores["EMPATE"]}', 'yellow'))
        if not ask_yes_no('¿Deseas jugar otra partida?'):
            break
    print(color('Gracias por jugar 3 en raya. ¡Hasta pronto!', 'green'))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n' + color('Juego interrumpido. ¡Hasta luego!', 'red'))
