from flask import Flask, request

app = Flask(__name__)

import logging
LOGGER = logging.getLogger(__name__)


@app.route('/tictactoe/', methods=['GET'])
def hello_world():
    return 'Welcome to tictactoe'


@app.route('/tictactoe/new', methods=['GET'])
def new_game():
    return 'Ok'


@app.route('/tictactoe/move', methods=['POST'])
def move():
    LOGGER.info('hit!!')
    board = 'Ok' + str(request.form['pos']) + ' Turn: ' + str(request.form['player']) + 'Board : ' + request.form[
        'board']
    return board
    #TODO return the move proposed based in the player






if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
