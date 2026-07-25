const boardButtons = Array.from(document.querySelectorAll('.cell'));
const modeSelect = document.getElementById('modeSelect');
const playerSymbolSelect = document.getElementById('playerSymbol');
const restartBtn = document.getElementById('restartBtn');
const turnLabel = document.getElementById('turnLabel');
const messageText = document.getElementById('message');
const scoreX = document.getElementById('scoreX');
const scoreO = document.getElementById('scoreO');
const scoreDraw = document.getElementById('scoreDraw');

const WIN_PATTERNS = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
];

let board = Array(9).fill(' ');
let currentSymbol = 'X';
let scores = { X: 0, O: 0, EMPATE: 0 };
let gameOver = false;

function clearHighlights() {
    boardButtons.forEach(button => button.classList.remove('win-line'));
}

function renderBoard() {
    boardButtons.forEach((button, index) => {
        button.textContent = board[index] === ' ' ? '' : board[index];
        button.disabled = board[index] !== ' ' || gameOver || (modeSelect.value === 'cpu' && currentSymbol === cpuSymbol());
    });
}

function updateStatus(text) {
    turnLabel.textContent = `Turno: ${currentSymbol}`;
    messageText.textContent = text;
}

function findWinningLine() {
    for (const pattern of WIN_PATTERNS) {
        const [a, b, c] = pattern;
        if (board[a] !== ' ' && board[a] === board[b] && board[b] === board[c]) {
            return pattern;
        }
    }
    return null;
}

function highlightWinningLine(pattern) {
    clearHighlights();
    if (!pattern) return;
    pattern.forEach(index => {
        boardButtons[index].classList.add('win-line');
    });
}

function checkWinner() {
    const winner = findWinningLine();
    return winner ? board[winner[0]] : null;
}

function isDraw() {
    return board.every(cell => cell !== ' ') && !checkWinner();
}

function setResult(result) {
    gameOver = true;
    if (result === 'EMPATE') {
        clearHighlights();
        messageText.textContent = 'Empate. ¡Buena partida!';
        scores.EMPATE += 1;
    } else {
        const line = findWinningLine();
        highlightWinningLine(line);
        messageText.textContent = `¡VICTORIA EFICAZ! El jugador ${result} ganó con una línea perfecta.`;
        scores[result] += 1;
    }
    scoreX.textContent = scores.X;
    scoreO.textContent = scores.O;
    scoreDraw.textContent = scores.EMPATE;
    boardButtons.forEach(button => button.disabled = true);
    messageText.classList.add('celebrate');
    setTimeout(() => messageText.classList.remove('celebrate'), 2600);
}

async function requestCpuMove() {
    const response = await fetch('/api/cpu-move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ board, cpuSymbol: cpuSymbol(), humanSymbol: humanSymbol() }),
    });
    const data = await response.json();
    return data.move;
}

function cpuSymbol() {
    return playerSymbolSelect.value === 'X' ? 'O' : 'X';
}

function humanSymbol() {
    return playerSymbolSelect.value;
}

async function makeMove(index) {
    if (board[index] !== ' ' || gameOver || (modeSelect.value === 'cpu' && currentSymbol !== humanSymbol())) return;
    board[index] = currentSymbol;
    renderBoard();
    const winner = checkWinner();
    if (winner) {
        setResult(winner);
        return;
    }
    if (isDraw()) {
        setResult('EMPATE');
        return;
    }
    currentSymbol = currentSymbol === 'X' ? 'O' : 'X';
    updateStatus(`Toca ${currentSymbol}`);

    if (modeSelect.value === 'cpu' && currentSymbol === cpuSymbol() && !gameOver) {
        await performCpuTurn();
    }
}

async function performCpuTurn() {
    messageText.textContent = 'CPU pensando...';
    renderBoard();
    const cpuMove = await requestCpuMove();
    board[cpuMove] = currentSymbol;
    renderBoard();
    const cpuWinner = checkWinner();
    if (cpuWinner) {
        setResult(cpuWinner);
        return;
    }
    if (isDraw()) {
        setResult('EMPATE');
        return;
    }
    currentSymbol = humanSymbol();
    updateStatus('Toca tu turno');
    renderBoard();
}

function restartGame() {
    board = Array(9).fill(' ');
    currentSymbol = 'X';
    gameOver = false;
    clearHighlights();
    renderBoard();
    updateStatus(`Toca ${currentSymbol}`);
    messageText.textContent = 'Empieza una nueva partida.';
    messageText.classList.remove('celebrate');

    if (modeSelect.value === 'cpu' && currentSymbol === cpuSymbol()) {
        performCpuTurn();
    }
}

boardButtons.forEach(button => {
    button.addEventListener('click', () => {
        const index = Number(button.dataset.index);
        makeMove(index);
    });
});

restartBtn.addEventListener('click', restartGame);
modeSelect.addEventListener('change', () => {
    restartGame();
});
playerSymbolSelect.addEventListener('change', () => {
    restartGame();
});

restartGame();
