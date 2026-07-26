import random

import streamlit as st

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


def is_draw(board):
    return ' ' not in board and check_winner(board) is None


def init_state():
    st.set_page_config(page_title='3 en Raya', page_icon='🎮', layout='centered')
    st.session_state.setdefault('board', [' '] * 9)
    st.session_state.setdefault('current_symbol', 'X')
    st.session_state.setdefault('game_over', False)
    st.session_state.setdefault('message', 'Toca una casilla para comenzar.')
    st.session_state.setdefault('score_x', 0)
    st.session_state.setdefault('score_o', 0)
    st.session_state.setdefault('score_draw', 0)
    st.session_state.setdefault('mode', 'Jugador vs Jugador')
    st.session_state.setdefault('player_symbol', 'X')


def human_symbol():
    return st.session_state.player_symbol


def cpu_symbol():
    return 'O' if human_symbol() == 'X' else 'X'


def set_result(result):
    st.session_state.game_over = True
    if result == 'EMPATE':
        st.session_state.message = 'Empate. ¡Buena partida!'
        st.session_state.score_draw += 1
    else:
        st.session_state.message = f'¡Victoria! El jugador {result} ganó.'
        if result == 'X':
            st.session_state.score_x += 1
        else:
            st.session_state.score_o += 1


def evaluate_board():
    winner = check_winner(st.session_state.board)
    if winner:
        set_result(winner)
        return True
    if is_draw(st.session_state.board):
        set_result('EMPATE')
        return True
    return False


def cpu_turn():
    if st.session_state.game_over:
        return

    move = cpu_best_move(
        st.session_state.board,
        cpu_symbol(),
        human_symbol(),
    )
    st.session_state.board[move] = st.session_state.current_symbol
    if evaluate_board():
        return

    st.session_state.current_symbol = human_symbol()
    st.session_state.message = 'Toca tu turno.'


def make_move(index):
    if st.session_state.game_over:
        return
    if st.session_state.board[index] != ' ':
        return
    if st.session_state.mode == 'Jugador vs CPU' and st.session_state.current_symbol == cpu_symbol():
        return

    st.session_state.board[index] = st.session_state.current_symbol
    if evaluate_board():
        return

    st.session_state.current_symbol = 'O' if st.session_state.current_symbol == 'X' else 'X'
    if st.session_state.mode == 'Jugador vs CPU' and st.session_state.current_symbol == cpu_symbol():
        cpu_turn()
    else:
        st.session_state.message = f'Toca {st.session_state.current_symbol}. '


def restart():
    st.session_state.board = [' '] * 9
    st.session_state.current_symbol = 'X'
    st.session_state.game_over = False
    st.session_state.message = 'Toca una casilla para comenzar.'
    if st.session_state.mode == 'Jugador vs CPU' and st.session_state.current_symbol == cpu_symbol():
        cpu_turn()


def render_board():
    button_labels = [cell if cell != ' ' else ' ' for cell in st.session_state.board]
    for row in range(3):
        cols = st.columns(3)
        for col, idx in zip(cols, range(row * 3, row * 3 + 3)):
            disabled = (
                st.session_state.board[idx] != ' '
                or st.session_state.game_over
                or (st.session_state.mode == 'Jugador vs CPU' and st.session_state.current_symbol == cpu_symbol())
            )
            if col.button(button_labels[idx], key=f'cell_{idx}', disabled=disabled, use_container_width=True):
                make_move(idx)


init_state()

st.title('3 en Raya')
st.write('Disfruta una versión moderna con CPU, puntuación y tablero interactivo.')

col1, col2 = st.columns([2, 1])
with col1:
    st.selectbox(
        'Modo',
        ['Jugador vs Jugador', 'Jugador vs CPU'],
        key='mode',
        on_change=restart,
    )
    st.selectbox(
        'Tu símbolo',
        ['X', 'O'],
        key='player_symbol',
        on_change=restart,
    )
with col2:
    st.button('Reiniciar partida', on_click=restart)

st.markdown('### Marcador')
score_cols = st.columns(3)
score_cols[0].metric('X', st.session_state.score_x)
score_cols[1].metric('O', st.session_state.score_o)
score_cols[2].metric('Empates', st.session_state.score_draw)

st.markdown('### Tablero')
render_board()

if st.session_state.game_over:
    st.success(st.session_state.message)
else:
    st.info(st.session_state.message)
