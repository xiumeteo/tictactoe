import os

from flask import Flask, request, send_from_directory, jsonify
from game import Minimax, Game, computer, Move

app = Flask(__name__, static_folder='tictactoe-react/build')

import logging
LOGGER = logging.getLogger(__name__)

@app.route('/static', defaults={'path': ''})
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('tictactoe-react/build/static/', path)


@app.route('/tictactoe')
def serve():
    return send_from_directory('tictactoe-react/build/', 'index.html')


@app.route('/tictactoe/new', methods=['GET'])
def new_game():
    return 'Ok'


@app.route('/tictactoe/move', methods=['POST'])
def move():
    LOGGER.info('hit!!')

    pos = request.form['pos']
    board = request.form['board']
    print(board)
    game = Game(list(board))
    print(game)
    choice = Minimax(game, computer).get_best_choice()

    response = {
        "pos" : choice.move.move_initiated.pos,
        #TODO message
    }

    return jsonify(response)






if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
