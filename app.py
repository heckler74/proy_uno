import random
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

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


def check_winner(board):
    for a, b, c in WIN_PATTERNS:
        if board[a] == board[b] == board[c] and board[a] != ' ':
            return board[a]
    return None


def available_moves(board):
    return [i for i, cell in enumerate(board) if cell == ' ']


def cpu_best_move(board, cpu_symbol, human_symbol):
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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/cpu-move', methods=['POST'])
def cpu_move():
    data = request.get_json(force=True)
    board = data.get('board', [])
    cpu_symbol = data.get('cpuSymbol', 'O')
    human_symbol = data.get('humanSymbol', 'X')
    if len(board) != 9 or any(cell not in ['X', 'O', ' '] for cell in board):
        return jsonify({'error': 'Datos de tablero inválidos.'}), 400
    move = cpu_best_move(board, cpu_symbol, human_symbol)
    return jsonify({'move': move})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
