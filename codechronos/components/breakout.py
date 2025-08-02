"""
Breakout Game - Classic arcade game component
"""

import reflex as rx
from typing import List, Dict, Any

class BreakoutState(rx.State):
    """Breakout game state"""
    game_started: bool = False
    score: int = 0
    lives: int = 3
    ball_x: int = 150  # Centered in canvas
    ball_y: int = 200  # Safe starting position
    ball_dx: int = 3  # Ball velocity X
    ball_dy: int = -3  # Ball velocity Y
    paddle_x: int = 110  # Centered paddle
    paddle_width: int = 80
    bricks_left: int = 40
    game_over: bool = False
    auto_play: bool = False  # Auto-play mode
    
    # Brick grid (5 rows x 8 cols)
    bricks: List[List[bool]] = [[True for _ in range(8)] for _ in range(5)]
    
    # Scaled positions for display
    @rx.var
    def scaled_ball_x(self) -> int:
        return int(self.ball_x * 0.9)  # Less scaling for bigger game
    
    @rx.var
    def scaled_ball_y(self) -> int:
        return int(self.ball_y * 0.8)  # Less scaling for bigger game
    
    @rx.var
    def scaled_paddle_x(self) -> int:
        return int(self.paddle_x * 0.9)  # Less scaling for bigger game
    
    @rx.var
    def scaled_paddle_width(self) -> int:
        return int(self.paddle_width * 0.9)  # Less scaling for bigger game
    
    def start_game(self):
        """Start new game"""
        self.game_started = True
        self.score = 0
        self.lives = 3
        self.ball_x = 150  # Center of 300px canvas
        self.ball_y = 200  # Safe starting position
        self.ball_dx = 5  # Faster ball speed
        self.ball_dy = -5  # Faster ball speed
        self.paddle_x = 110  # Center paddle (150 - 40)
        self.game_over = False
        self.bricks_left = 40
        self.auto_play = True  # Start auto-play automatically
        # Reset all bricks
        self.bricks = [[True for _ in range(8)] for _ in range(5)]
    
    def toggle_auto_play(self):
        """Toggle auto-play mode"""
        self.auto_play = not self.auto_play
    
    def update_ball(self):
        """Update ball position and handle collisions - scaled for compact view"""
        if not self.game_started or self.game_over:
            return
            
        # Move ball
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy
        
        # Wall collisions (adjusted for canvas: 300x280)
        # Side walls - bounce back (traditional breakout)
        if self.ball_x <= 10 or self.ball_x >= 290:
            self.ball_dx = -self.ball_dx
            
        # Top wall - bounce back
        if self.ball_y <= 10:
            self.ball_dy = -self.ball_dy
            
        # Bottom wall (lose life)
        if self.ball_y >= 270:
            self.lose_life()
            return
            
        # Paddle collision - adjusted for canvas size  
        if (self.ball_y >= 240 and self.ball_y <= 260 and 
            self.ball_x >= self.paddle_x and self.ball_x <= self.paddle_x + self.paddle_width):
            self.ball_dy = -abs(self.ball_dy)  # Always bounce up
            
        # Brick collisions - scaled
        brick_row = int((self.ball_y - 30) / 16)  # Adjusted for smaller bricks
        brick_col = int((self.ball_x - 5) / 40)   # Adjusted spacing
        
        if (0 <= brick_row < 5 and 0 <= brick_col < 8 and 
            self.bricks[brick_row][brick_col]):
            self.hit_brick(brick_row, brick_col)
            self.ball_dy = -self.ball_dy
    
    def move_paddle_left(self):
        """Move paddle left"""
        if self.paddle_x > 0:
            self.paddle_x = max(0, self.paddle_x - 30)
    
    def move_paddle_right(self):
        """Move paddle right"""
        if self.paddle_x < 220:  # Adjusted for new canvas width (300 - paddle_width)
            self.paddle_x = min(220, self.paddle_x + 30)
    
    def hit_brick(self, row: int, col: int):
        """Hit a brick"""
        if self.bricks[row][col]:
            self.bricks[row][col] = False
            self.score += (5 - row) * 10  # Higher rows worth more
            self.bricks_left -= 1
            if self.bricks_left == 0:
                self.level_complete()
    
    def level_complete(self):
        """Complete current level"""
        self.score += 100
        # Reset bricks for next level
        self.bricks = [[True for _ in range(8)] for _ in range(5)]
        self.bricks_left = 40
    
    def lose_life(self):
        """Lose a life"""
        self.lives -= 1
        if self.lives <= 0:
            self.game_over = True
        else:
            # Reset ball position to center of canvas
            self.ball_x = 150  # Center of 300px width
            self.ball_y = 200  # Safe position in 280px height
    
    def reset_game(self):
        """Reset game to initial state"""
        self.game_started = False
        self.game_over = False
        self.score = 0
        self.lives = 3

def game_controls() -> rx.Component:
    """Game control buttons"""
    return rx.hstack(
        rx.cond(
            ~BreakoutState.game_started | BreakoutState.game_over,
            rx.button(
                "Start Game",
                on_click=BreakoutState.start_game,
                bg="green",
                color="white",
                size="3"
            ),
            rx.hstack(
                rx.button(
                    "◀ Left",
                    on_click=BreakoutState.move_paddle_left,
                    bg="blue",
                    color="white",
                    size="2"
                ),
                rx.button(
                    "Right ▶", 
                    on_click=BreakoutState.move_paddle_right,
                    bg="blue",
                    color="white",
                    size="2"
                ),
                rx.button(
                    rx.cond(
                        BreakoutState.auto_play,
                        "⏸️ Pause",
                        "▶️ Auto"
                    ),
                    on_click=BreakoutState.toggle_auto_play,
                    bg="purple",
                    color="white",
                    size="2"
                ),
                rx.button(
                    "Move Ball",
                    on_click=BreakoutState.update_ball,
                    bg="cyan",
                    color="black",
                    size="2"
                ),
                rx.button(
                    "Miss Ball",
                    on_click=BreakoutState.lose_life,
                    bg="orange",
                    color="white",
                    size="2"
                ),
                rx.button(
                    "Reset",
                    on_click=BreakoutState.reset_game,
                    bg="red",
                    color="white",
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
        rx.text(f"Score: {BreakoutState.score}", size="3", weight="bold", color="white"),
        rx.text(f"Lives: {BreakoutState.lives}", size="3", weight="bold", color="white"),
        rx.text(f"Bricks: {BreakoutState.bricks_left}", size="3", weight="bold", color="white"),
        justify="between",
        width="100%",
        padding="1rem",
        bg="black"
    )

def game_canvas() -> rx.Component:
    """Game canvas using Reflex components"""
    return rx.box(
        # Game area
        rx.box(
            # Bricks
            rx.vstack(
                *[
                    rx.hstack(
                        *[
                            rx.cond(
                                BreakoutState.bricks[row][col],
                                rx.box(
                                    width="45px",
                                    height="15px",
                                    bg=["red", "orange", "yellow", "green", "blue"][row],
                                    border="1px solid white",
                                    cursor="pointer",
                                    on_click=lambda r=row, c=col: BreakoutState.hit_brick(r, c)
                                ),
                                rx.box(width="45px", height="15px")  # Empty space
                            )
                            for col in range(8)
                        ],
                        spacing="1"
                    )
                    for row in range(5)
                ],
                spacing="1",
                align="center"
            ),
            
            # Ball (represented as a dot)
            rx.box(
                "●",
                position="absolute",
                left=f"{BreakoutState.ball_x}px",
                top=f"{BreakoutState.ball_y}px",
                color="white",
                font_size="20px",
                z_index="10"
            ),
            
            # Paddle
            rx.box(
                width=f"{BreakoutState.paddle_width}px",
                height="10px",
                bg="white",
                position="absolute",
                left=f"{BreakoutState.paddle_x}px",
                bottom="20px",
                border_radius="2px"
            ),
            
            position="relative",
            width="400px",
            height="400px",
            bg="black",
            border="2px solid white",
            margin="0 auto",
            padding="20px"
        ),
        display="flex",
        justify_content="center",
        padding="1rem"
    )

def breakout_component() -> rx.Component:
    """Complete Breakout game component with auto-moving ball - compact for Mac window"""
    return rx.vstack(
        # Compact header
        rx.text("BREAKOUT", size="4", weight="bold", color="white", text_align="center"),
        
        # Compact status (smaller)
        rx.cond(
            BreakoutState.auto_play,
            rx.text("🟢 AUTO", color="lime", size="1", text_align="center"),
            rx.text("🔴 MANUAL", color="red", size="1", text_align="center")
        ),
        
        # Larger stats
        rx.hstack(
            rx.text(f"Score: {BreakoutState.score}", size="2", color="white", weight="bold"),
            rx.text(f"Lives: {BreakoutState.lives}", size="2", color="white", weight="bold"), 
            rx.text(f"Bricks: {BreakoutState.bricks_left}", size="2", color="white", weight="bold"),
            justify="between",
            width="100%",
            padding="0.8rem"
        ),
        
        # Larger game canvas
        rx.box(
            rx.box(
                # Larger bricks
                rx.vstack(
                    *[
                        rx.hstack(
                            *[
                                rx.cond(
                                    BreakoutState.bricks[row][col],
                                    rx.box(
                                        width="32px",  # Reduced brick size
                                        height="10px",  # Reduced brick size
                                        bg=["red", "orange", "yellow", "green", "blue"][row],
                                        border="1px solid white",
                                        cursor="pointer",
                                        on_click=lambda r=row, c=col: BreakoutState.hit_brick(r, c)
                                    ),
                                    rx.box(width="35px", height="10px")
                                )
                                for col in range(8)
                            ],
                            spacing="1"
                        )
                        for row in range(5)
                    ],
                    spacing="1",
                    align="center"
                ),
                
                # Ball
                rx.box(
                    "●",
                    position="absolute",
                    left=f"{BreakoutState.scaled_ball_x}px",
                    top=f"{BreakoutState.scaled_ball_y}px",
                    color="white",
                    font_size="16px",  # Bigger ball
                    z_index="10"
                ),
                
                # Paddle
                rx.box(
                    width=f"{BreakoutState.scaled_paddle_width}px",
                    height="8px",  # Bigger paddle
                    bg="white",
                    position="absolute",
                    left=f"{BreakoutState.scaled_paddle_x}px",
                    bottom="20px",
                    border_radius="2px"
                ),
                
                position="relative",
                width="300px",  # Reduced width for better fit
                height="280px",  # Much larger canvas
                bg="black",
                border="2px solid white",
                margin="0 auto"
            ),
            padding="0.5rem"
        ),
        
        # Larger controls
        rx.cond(
            ~BreakoutState.game_started | BreakoutState.game_over,
            rx.button(
                "Start Game",
                on_click=BreakoutState.start_game,
                bg="green",
                color="white",
                size="3",
                width="120px"
            ),
            rx.hstack(
                rx.button("◀ Left", on_click=BreakoutState.move_paddle_left, bg="blue", color="white", size="2"),
                rx.button("Right ▶", on_click=BreakoutState.move_paddle_right, bg="blue", color="white", size="2"),
                rx.button(
                    rx.cond(BreakoutState.auto_play, "⏸️ Pause", "▶️ Auto"),
                    on_click=BreakoutState.toggle_auto_play,
                    bg="purple", color="white", size="2"
                ),
                rx.button("Move Ball", on_click=BreakoutState.update_ball, bg="cyan", color="black", size="2"),
                rx.button("Reset", on_click=BreakoutState.reset_game, bg="red", color="white", size="2"),
                spacing="2",
                justify="center"
            )
        ),
        
        # Auto-play mechanism (same as before)
        rx.cond(
            BreakoutState.auto_play & BreakoutState.game_started & ~BreakoutState.game_over,
            rx.box(
                rx.script("""
                    setTimeout(function autoMove() {
                        const moveButton = document.querySelector('[data-auto-move="true"]');
                        if (moveButton && moveButton.getAttribute('data-auto-play') === 'true') {
                            moveButton.click();
                            setTimeout(autoMove, 120); // Faster auto-play for bigger game
                        }
                    }, 120);
                """),
                rx.button(
                    "",
                    on_click=BreakoutState.update_ball,
                    style={"display": "none"},
                    **{
                        "data-auto-move": "true",
                        "data-auto-play": rx.cond(BreakoutState.auto_play, "true", "false")
                    }
                )
            ),
            rx.box()
        ),
        
        # Larger game over/complete messages
        rx.cond(
            BreakoutState.game_over,
            rx.text("GAME OVER!", size="4", weight="bold", color="red", text_align="center"),
            rx.box()
        ),
        rx.cond(
            BreakoutState.bricks_left == 0,
            rx.text("LEVEL COMPLETE!", size="4", weight="bold", color="green", text_align="center"),
            rx.box()
        ),
        
        spacing="3",
        width="100%",
        align="center",
        bg="black",
        color="white",
        padding="15px",
        border_radius="6px",
        max_height="400px",  # Larger to fit bigger game
        overflow="auto"  # Scrollable if needed
    )
