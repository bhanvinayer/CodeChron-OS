"""
Breakout Game - Classic arcade game component
"""

import reflex as rx
import random

class BreakoutState(rx.State):
    """Breakout game state"""
    game_started: bool = False
    score: int = 0
    lives: int = 3
    level: int = 1
    ball_x: float = 200
    ball_y: float = 300
    ball_dx: float = 3
    ball_dy: float = -3
    paddle_x: float = 175
    paddle_width: int = 50
    bricks: list = []
    game_over: bool = False
    paused: bool = False
    
    def start_game(self):
        """Start new game"""
        self.game_started = True
        self.score = 0
        self.lives = 3
        self.level = 1
        self.ball_x = 200
        self.ball_y = 300
        self.ball_dx = 3
        self.ball_dy = -3
        self.paddle_x = 175
        self.game_over = False
        self.paused = False
        self.init_bricks()
    
    def init_bricks(self):
        """Initialize brick layout"""
        self.bricks = []
        colors = ["red", "orange", "yellow", "green", "blue"]
        for row in range(5):
            for col in range(8):
                self.bricks.append({
                    "x": col * 50 + 5,
                    "y": row * 20 + 50,
                    "width": 45,
                    "height": 15,
                    "color": colors[row],
                    "destroyed": False
                })
    
    def move_paddle_left(self):
        """Move paddle left"""
        if self.paddle_x > 0:
            self.paddle_x = max(0, self.paddle_x - 20)
    
    def move_paddle_right(self):
        """Move paddle right"""
        if self.paddle_x < 350:
            self.paddle_x = min(350, self.paddle_x + 20)
    
    def toggle_pause(self):
        """Toggle game pause"""
        self.paused = not self.paused
    
    def reset_game(self):
        """Reset game to initial state"""
        self.game_started = False
        self.game_over = False
        self.paused = False

def game_controls() -> rx.Component:
    """Game control buttons"""
    return rx.hstack(
        rx.cond(
            ~BreakoutState.game_started,
            rx.button(
                "Start Game",
                on_click=BreakoutState.start_game,
                color_scheme="green",
                size="3"
            ),
            rx.hstack(
                rx.button(
                    "◀",
                    on_click=BreakoutState.move_paddle_left,
                    size="2"
                ),
                rx.button(
                    "▶", 
                    on_click=BreakoutState.move_paddle_right,
                    size="2"
                ),
                rx.button(
                    "⏸️" if not BreakoutState.paused else "▶️",
                    on_click=BreakoutState.toggle_pause,
                    size="2"
                ),
                rx.button(
                    "Reset",
                    on_click=BreakoutState.reset_game,
                    color_scheme="red",
                    size="2"
                ),
                spacing="2"
            )
        ),
        justify="center",
        width="100%",
        padding="1rem"
    )

def game_stats() -> rx.Component:
    """Display game statistics"""
    return rx.hstack(
        rx.text(f"Score: {BreakoutState.score}", size="3", weight="bold"),
        rx.text(f"Lives: {BreakoutState.lives}", size="3", weight="bold"),
        rx.text(f"Level: {BreakoutState.level}", size="3", weight="bold"),
        justify="space-between",
        width="100%",
        padding="1rem",
        bg=rx.color("gray", 2)
    )

def game_canvas() -> rx.Component:
    """Game canvas with HTML5 canvas"""
    return rx.box(
        rx.html(
            f"""
            <canvas 
                id="breakout-canvas" 
                width="400" 
                height="400"
                style="border: 2px solid #333; background: black;"
            ></canvas>
            <script>
                const canvas = document.getElementById('breakout-canvas');
                const ctx = canvas.getContext('2d');
                
                function drawGame() {{
                    // Clear canvas
                    ctx.clearRect(0, 0, 400, 400);
                    
                    // Draw paddle
                    ctx.fillStyle = 'white';
                    ctx.fillRect({BreakoutState.paddle_x}, 350, {BreakoutState.paddle_width}, 10);
                    
                    // Draw ball
                    ctx.beginPath();
                    ctx.arc({BreakoutState.ball_x}, {BreakoutState.ball_y}, 8, 0, Math.PI * 2);
                    ctx.fillStyle = 'white';
                    ctx.fill();
                    
                    // Draw bricks (simplified)
                    for (let row = 0; row < 5; row++) {{
                        for (let col = 0; col < 8; col++) {{
                            const colors = ['red', 'orange', 'yellow', 'green', 'blue'];
                            ctx.fillStyle = colors[row];
                            ctx.fillRect(col * 50 + 5, row * 20 + 50, 45, 15);
                        }}
                    }}
                }}
                
                // Initial draw
                drawGame();
                
                // Simple animation loop
                setInterval(drawGame, 100);
            </script>
            """
        ),
        display="flex",
        justify_content="center",
        padding="1rem"
    )

def breakout_component() -> rx.Component:
    """Complete Breakout game component"""
    return rx.vstack(
        game_stats(),
        game_canvas(),
        game_controls(),
        rx.cond(
            BreakoutState.game_over,
            rx.box(
                rx.text(
                    "GAME OVER",
                    size="8",
                    weight="bold",
                    color="red"
                ),
                padding="2rem",
                text_align="center"
            ),
            rx.box()
        ),
        spacing="0",
        width="100%",
        align="center",
        bg="black",
        color="white",
        border_radius="8px"
    )
