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
        if (this.state.xIsNext) {
            let request = new XMLHttpRequest();
            request.open('POST', 'http://localhost:5000/tictactoe/move', true);
            request.onload = function () {
                console.log(this.response);
            };

            let data = new FormData();
            data.append('pos', index);
            data.append('player', 'X');
            data.append('board', this.state.squares.join(''));
            request.send(data);

        }
        squares[index] = this.getPlayerValue();
        this.setState({
                squares: squares,
                xIsNext: !this.state.xIsNext
            }
        );


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
