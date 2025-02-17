from flask import Flask, render_template, jsonify

app = Flask(__name__)

board = [['' for _ in range(3)] for _ in range(3)]
current_player = 'X'
status = "Player X's turn"


@app.route('/')
def index():
    return render_template('index.html', board=board, status=status)


@app.route('/move/<int:i>/<int:j>')
def move(i, j):
    global current_player, status

    if board[i][j] == '':
        board[i][j] = current_player
        if check_winner():
            status = f"Player {current_player} wins!"
        elif all(cell for row in board for cell in row):
            status = "It's a draw!"
        else:
            current_player = 'O' if current_player == 'X' else 'X'
            status = f"Player {current_player}'s turn"

    board_html = render_template('board.html', board=board)
    return jsonify({'board_html': board_html, 'status': status})


@app.route('/reset')
def reset():
    global board, current_player, status
    board = [['' for _ in range(3)] for _ in range(3)]
    current_player = 'X'
    status = "Player X's turn"

    board_html = render_template('board.html', board=board)
    return jsonify({'board_html': board_html, 'status': status})


def check_winner():
    for row in board:
        if row[0] == row[1] == row[2] != '':
            return True

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != '':
            return True

    if board[0][0] == board[1][1] == board[2][2] != '' or board[0][2] == board[1][1] == board[2][0] != '':
        return True

    return False


if __name__ == '__main__':
    app.run(debug=True)
