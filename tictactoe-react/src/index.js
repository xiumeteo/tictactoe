import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

function Square(props) {
    return (
        <button className="square" onClick={props.onClick}>
            {props.value}
        </button>
    );
}

class Board extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            squares: Array(9).fill('_'),
            xIsNext: false,
        };
    }

    handleClick(index) {
        const squares = this.state.squares.slice();
        squares[index] = this.getPlayerValue();
        this.setState({
                squares: squares,
                xIsNext: this.state.xIsNext
            }
        );

        if (!this.state.xIsNext) {
            let request = new XMLHttpRequest();
            request.open('POST', 'http://0.0.0.0:5000/tictactoe/move', true);
            let that = this;
            request.onload = function () {
                let move = JSON.parse(this.response);
                squares[move.pos] = 'X';
                that.setState({
                        squares: squares,
                        xIsNext: false
                    }
                );
                if (move.end) {
                    if (move.winner === 'X') {
                        alert("Computer will always win!");
                    }
                    if (move.winner === 'O') {
                        alert("Humans win this time, there must be an error on my program!");
                    }
                    if (move.winner === '_') {
                        alert("Good match!");
                    }


                }
            };

            let data = new FormData();
            data.append('pos', index);
            data.append('player', 'X');
            let board = squares.join('');
            console.log(board);
            data.append('board', board);
            request.send(data);

        }


    }


    getPlayerValue() {
        return this.state.xIsNext ? 'X' : 'O';
    }

    renderSquare(index) {
        return <Square value={this.state.squares[index]}
                       onClick={() => this.handleClick(index)}/>;
    }

    render() {
        const status = 'Next player: ' + (this.getPlayerValue());

        return (
            <div>
                <div className="status">{status}</div>
                <div className="board-row">
                    {this.renderSquare(0)}
                    {this.renderSquare(1)}
                    {this.renderSquare(2)}
                </div>
                <div className="board-row">
                    {this.renderSquare(3)}
                    {this.renderSquare(4)}
                    {this.renderSquare(5)}
                </div>
                <div className="board-row">
                    {this.renderSquare(6)}
                    {this.renderSquare(7)}
                    {this.renderSquare(8)}
                </div>
            </div>
        );
    }
}

class Game extends React.Component {
    render() {
        return (
            <div className="game">
                <div className="game-board">
                    <Board/>
                </div>
                <div className="game-info">
                    <div>{/* status */}</div>
                    <ol>{/* TODO */}</ol>
                </div>
            </div>
        );
    }
}

// ========================================

ReactDOM.render(
    <Game/>,
    document.getElementById('root')
);
