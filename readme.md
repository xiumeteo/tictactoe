# Minimax Tictactoe

This is a tiny project to demonstrate the implementation of minimax algorithm to create a virtually 
unbeatable tic-tact-toe

## How to run it?
The code runs on Python3+ and dev env used Python3.6+ in particular.

Once downloaded, you can simply run tictactoe.py and it will start.

## How to run tests?
Tests run on top of py.test for simplicity reasons. `requirements` for pip is provided.
Specifically the tests are contained inside `board_test.py` so you can simply run
`py.test board_test.py`

### How to run the web?
The server is merely experimental, if you want to use it :
1. compile the react app at `tictactoe-react` using `npm run build` 
2. start the `Flask` server with `python app.py`
3. Go to [http://0.0.0.0:5000/tictactoe](http://0.0.0.0:5000/tictactoe)
4. Enjoy (remember that the first move is really slow on the machine side, we're working on this, so please wait for the machine response...)


