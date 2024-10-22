from flask import Flask, render_template_string

# Flaskのインスタンスを作成
app = Flask(__name__)

# HTMLテンプレート
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pong Game</title>
    <style>
        canvas {
            display: block;
            margin: 0 auto;
            background: #000;
        }
        #message {
            text-align: center;
            font-size: 24px;
            color: white;
        }
        #restart {
            display: block;
            margin: 20px auto;
            padding: 10px 20px;
            font-size: 16px;
        }
    </style>
</head>
<body>
    <div id="message"></div>
    <canvas id="pong" width="800" height="400"></canvas>
    <button id="restart" onclick="startGame()">Restart</button>
    <script>
        const canvas = document.getElementById('pong');
        const context = canvas.getContext('2d');
        const message = document.getElementById('message');
        const restartButton = document.getElementById('restart');

        const paddleWidth = 10, paddleHeight = 100;
        const ballSize = 10;

        let player, computer, ball, gameOver;

        function init() {
            player = {
                x: 0,
                y: canvas.height / 2 - paddleHeight / 2,
                width: paddleWidth,
                height: paddleHeight,
                color: 'blue',
                dy: 0
            };

            computer = {
                x: canvas.width - paddleWidth,
                y: canvas.height / 2 - paddleHeight / 2,
                width: paddleWidth,
                height: paddleHeight,
                color: 'red',
                dy: 4
            };

            ball = {
                x: canvas.width / 2 - ballSize / 2,
                y: canvas.height / 2 - ballSize / 2,
                width: ballSize,
                height: ballSize,
                color: 'white',
                dx: 4,
                dy: 4
            };

            gameOver = false;
            message.textContent = '';
            restartButton.style.display = 'none';
        }

        function drawRect(x, y, w, h, color) {
            context.fillStyle = color;
            context.fillRect(x, y, w, h);
        }

        function drawBall(x, y, w, h, color) {
            context.fillStyle = color;
            context.fillRect(x, y, w, h);
        }

        function movePaddle(paddle) {
            paddle.y += paddle.dy;

            if (paddle.y < 0) {
                paddle.y = 0;
            } else if (paddle.y + paddle.height > canvas.height) {
                paddle.y = canvas.height - paddle.height;
            }
        }

        function moveBall() {
            ball.x += ball.dx;
            ball.y += ball.dy;

            if (ball.y < 0 || ball.y + ball.height > canvas.height) {
                ball.dy *= -1;
            }

            if (ball.x < 0) {
                gameOver = true;
                message.textContent = 'LOSE';
                message.style.color = 'red';
                restartButton.style.display = 'block';
            } else if (ball.x + ball.width > canvas.width) {
                gameOver = true;
                message.textContent = 'WIN';
                message.style.color = 'blue';
                restartButton.style.display = 'block';
            }

            // Check for collision with paddles
            if (ball.x < player.x + player.width && ball.y + ball.height > player.y && ball.y < player.y + player.height) {
                ball.dx *= -1;
            } else if (ball.x + ball.width > computer.x && ball.y + ball.height > computer.y && ball.y < computer.y + computer.height) {
                ball.dx *= -1;
            }
        }

        function update() {
            if (!gameOver) {
                movePaddle(player);
                movePaddle(computer);
                moveBall();

                // Random movement for computer paddle
                if (Math.random() > 0.5) {
                    computer.dy = 4;
                } else {
                    computer.dy = -4;
                }
            }
        }

        function render() {
            drawRect(0, 0, canvas.width, canvas.height, '#000');
            drawRect(player.x, player.y, player.width, player.height, player.color);
            drawRect(computer.x, computer.y, computer.width, computer.height, computer.color);
            drawBall(ball.x, ball.y, ball.width, ball.height, ball.color);
        }

        function gameLoop() {
            update();
            render();
            if (!gameOver) {
                requestAnimationFrame(gameLoop);
            }
        }

        function startGame() {
            init();
            gameLoop();
        }

        // Player control
        document.addEventListener('keydown', event => {
            switch(event.key) {
                case 'ArrowUp':
                    player.dy = -4;
                    break;
                case 'ArrowDown':
                    player.dy = 4;
                    break;
            }
        });

        document.addEventListener('keyup', event => {
            switch(event.key) {
                case 'ArrowUp':
                case 'ArrowDown':
                    player.dy = 0;
                    break;
            }
        });

        startGame();
    </script>
<font size=3 color="black"><center><B>PONG! TENNIS GAME</B><BR></center>このテニスゲームは生成AIのみで作成されています<BR>
使うキーは「↑」と「↓」のみです。ゲーム画面をクリックし、プレイしてください。プレイヤーは左側です。</font>
</body>
</html>
"""

# ルーティングの指定
@app.route('/')
def index():
    return render_template_string(html_template)

# 実行する
if __name__ == '__main__':
    app.run(host='0.0.0.0')
