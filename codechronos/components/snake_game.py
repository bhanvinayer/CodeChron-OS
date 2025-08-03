"""
Snake Game - Classic Snake Game for Playground 202X
"""

import asyncio
import random
from typing import Dict

import reflex as rx
from reflex.constants.colors import Color
from reflex.event import EventSpec
from reflex.utils.imports import ImportDict

N = 19  # There is a N*N grid for ground of snake
GRID_EMPTY = 0
GRID_SNAKE = 1
GRID_FOOD = 2
GRID_DEAD = 3
# Tuples representing the directions the snake head can move
HEAD_U = (0, -1)
HEAD_D = (0, 1)
HEAD_L = (-1, 0)
HEAD_R = (1, 0)
INITIAL_SNAKE = [  # all (X,Y) for snake's body
    (-1, -1),
    (-1, -1),
    (-1, -1),
    (-1, -1),
    (-1, -1),
    (10, 15),  # Starting head position
]
INITIAL_FOOD = (5, 5)  # X, Y of food


def get_new_head(old_head: tuple[int, int], dir: tuple[int, int]) -> tuple[int, int]:
    """Calculate the new head position based on the given direction."""
    x, y = old_head
    return (x + dir[0] + N) % N, (y + dir[1] + N) % N


def to_cell_index(x: int, y: int) -> int:
    """Calculate the index into the game board for the given (X, Y)."""
    return x + N * y


class SnakeColors(rx.State):
    """Colors of different grid square types for frontend rendering"""

    # Why is this not just a global? Because we index into the dict with state
    # vars in an rx.foreach, so this dict needs to be accessible in the compiled
    # frontend.
    c: dict[int, Color] = {
        GRID_EMPTY: rx.color("gray", 5),
        GRID_SNAKE: rx.color("grass", 9),
        GRID_FOOD: rx.color("blue", 9),
        GRID_DEAD: rx.color("red", 9),
    }


class SnakeGameState(rx.State):
    """Snake Game state management"""
    dir: tuple[int, int] = HEAD_R  # Direction the snake head is facing currently
    moves: list[tuple[int, int]] = []  # Queue of moves based on user input
    snake: list[tuple[int, int]] = INITIAL_SNAKE  # Body of snake
    food: tuple[int, int] = INITIAL_FOOD  # X, Y location of food
    cells: list[int] = (N * N) * [GRID_EMPTY]  # The game board to be rendered
    score: int = 0  # Player score
    magic: int = 1  # Number of points per food eaten
    rate: int = 10  # 5 divide by rate determines tick period
    died: bool = False  # If the snake is dead (game over)
    tick_cnt: int = 1  # How long the game has been running
    running: bool = False
    _n_tasks: int = 0

    @rx.event
    def reset_game(self):
        """Reset the game to initial state"""
        self.dir = HEAD_R
        self.moves = []
        self.snake = INITIAL_SNAKE.copy()
        self.food = INITIAL_FOOD
        self.cells = (N * N) * [GRID_EMPTY]
        self.score = 0
        self.magic = 1
        self.rate = 10
        self.died = False
        self.tick_cnt = 1
        self.running = False
        self._n_tasks = 0
        # Set initial game board
        for x, y in self.snake:
            if x >= 0 and y >= 0:  # Skip invalid positions
                self.cells[to_cell_index(x, y)] = GRID_SNAKE
        self.cells[to_cell_index(*self.food)] = GRID_FOOD

    @rx.event
    def play(self):
        """Start / resume the game."""
        if not self.running:
            if self.died:
                # If the player is dead, reset game state before beginning.
                self.reset_game()
            self.running = True
            return SnakeGameState.loop

    @rx.event
    def pause(self):
        """Signal the game to pause."""
        self.running = False

    @rx.event
    def flip_switch(self, start):
        """Toggle whether the game is running or paused."""
        if start:
            return SnakeGameState.play
        else:
            return SnakeGameState.pause

    def _next_move(self):
        """Returns the next direction the snake head should move in."""
        return self.moves[0] if self.moves else self.dir

    def _last_move(self):
        """Returns the last queued direction the snake head should move in."""
        return self.moves[-1] if self.moves else self.dir

    @rx.event(background=True)
    async def loop(self):
        """The main game loop, implemented as a singleton background task.

        Responsible for updating the game state on each tick.
        """
        async with self:
            if self._n_tasks > 0:
                # Only start one loop task at a time.
                return
            self._n_tasks += 1

        while self.running:
            # Sleep based on the current rate
            await asyncio.sleep(5 / self.rate)
            async with self:
                # Which direction will the snake move?
                self.dir = self._next_move()
                if self.moves:
                    # Remove the processed next move from the queue
                    del self.moves[0]

                # Calculate new head position
                head = get_new_head(self.snake[-1], dir=self.dir)
                if head in self.snake:
                    # New head position crashes into snake body, Game Over
                    self.running = False
                    self.died = True
                    self.cells[to_cell_index(*head)] = GRID_DEAD
                    break

                # Move the snake
                self.snake.append(head)
                self.cells[to_cell_index(*head)] = GRID_SNAKE
                food_eaten = False
                while self.food in self.snake:
                    food_eaten = True
                    self.food = (random.randint(0, N - 1), random.randint(0, N - 1))
                self.cells[to_cell_index(*self.food)] = GRID_FOOD
                if not food_eaten:
                    # Advance the snake
                    self.cells[to_cell_index(*self.snake[0])] = GRID_EMPTY
                    del self.snake[0]
                else:
                    # Grow the snake (and the score)
                    self.score += self.magic
                    self.magic += 1
                    self.rate = 10 + self.magic
                self.tick_cnt += 1

        async with self:
            # Decrement task counter, since we're about to return
            self._n_tasks -= 1

    @rx.event
    def arrow_up(self):
        """Queue a move up."""
        if self._last_move() != HEAD_D:
            self.moves.append(HEAD_U)

    @rx.event
    def arrow_left(self):
        """Queue a move left."""
        if self._last_move() != HEAD_R:
            self.moves.append(HEAD_L)

    @rx.event
    def arrow_right(self):
        """Queue a move right."""
        if self._last_move() != HEAD_L:
            self.moves.append(HEAD_R)

    @rx.event
    def arrow_down(self):
        """Queue a move down."""
        if self._last_move() != HEAD_U:
            self.moves.append(HEAD_D)

    @rx.event
    def arrow_rel_left(self):
        """Queue a move left relative to the current direction."""
        last_move = self._last_move()
        if last_move == HEAD_U:
            self.arrow_left()
        elif last_move == HEAD_L:
            self.arrow_down()
        elif last_move == HEAD_D:
            self.arrow_right()
        elif last_move == HEAD_R:
            self.arrow_up()

    @rx.event
    def arrow_rel_right(self):
        """Queue a move right relative to the current direction."""
        last_move = self._last_move()
        if last_move == HEAD_U:
            self.arrow_right()
        elif last_move == HEAD_L:
            self.arrow_up()
        elif last_move == HEAD_D:
            self.arrow_left()
        elif last_move == HEAD_R:
            self.arrow_down()


class GlobalKeyWatcher(rx.Fragment):
    """A component that attaches a keydown handler to the document.

    The handler only calls the backend function if the pressed key is one of the
    specified keys in the key_map.

    Requires custom javascript to support this functionality at the moment.
    """

    # List of keys to trigger on
    key_map: Dict[str, EventSpec] = {}

    def add_imports(self) -> ImportDict:
        return {"react": "useEffect"}

    def add_hooks(self) -> list[str | rx.Var[str]]:
        key_map = rx.Var.create(
            {
                key: rx.EventChain.create(args_spec=rx.event.key_event, value=handler)
                for key, handler in self.key_map.items()
            }
        )

        return [
            rx.Var(f"const key_map = {key_map}"),
            """
            useEffect(() => {
                const handle_key = (event) => key_map[event.key]?.(event)
                document.addEventListener("keydown", handle_key, false);
                return () => {
                    document.removeEventListener("keydown", handle_key, false);
                }
            })
            """,
        ]

    def render(self) -> dict:
        # This component has no visual element.
        return {}



# --- THEME COLORS ---
colors = {
    "bg": "linear-gradient(135deg, #dfe9f3 0%, #f0c4f3 100%)",
    "card": "#ffffff22",
    "highlight": "#81ecec",
    "grid_border": "#dfe6e9",
    "text": "#2d3436",
    "stat_bg": "#fffbe6",
    "stat_text": "#1a1a1a",  # Darker text for better contrast
    "stat_label": "#636e72",  # Gray for labels
    "button_pause": "#74b9ff",
    "button_run": "#55efc4",
    "heading": "#2d3436",  # Explicit heading color
    "link": "#2980b9",  # Link color
}

def colored_box(grid_square_type: int):
    """One square of the game grid."""
    return rx.box(
        bg=SnakeColors.c[grid_square_type],
        width="2em",
        height="2em",
        border=f"1px solid {colors['grid_border']}",
        border_radius="md",
        box_shadow="sm",
        margin="0",
    )


def stat_box(label, value):
    """Modern stat card."""
    return rx.box(
        rx.text(label, font_size="0.9em", color=colors["stat_label"], font_weight="bold", margin_bottom="0.2em"),
        rx.heading(value, font_size="1.5em", color=colors["stat_text"], font_weight="bold"),
        bg=colors["stat_bg"],
        border_radius="lg",
        box_shadow="md",
        padding="1em",
        min_width="5em",
        align="center",
        text_align="center",
        border=f"1px solid {colors['grid_border']}",
    )


def control_button(label, on_click):
    """Modern arrow button."""
    return rx.icon_button(
        rx.icon(tag=label),
        on_click=on_click,
        color_scheme="gray",
        border_radius="full",
        width="3em",
        height="3em",
        size="3",
        bg="#fff",
        box_shadow="md",
        _hover={"bg": colors["highlight"]},
    )


def padding_button():
    """A button that is used for padding in the controls panel."""
    return rx.button(
        border_radius="1em",
        font_size="2em",
        visibility="hidden",
    )


def controls_panel():
    """The controls panel of arrow buttons."""
    return rx.hstack(
        GlobalKeyWatcher.create(
            key_map={
                "ArrowUp": SnakeGameState.arrow_up(),
                "ArrowLeft": SnakeGameState.arrow_left(),
                "ArrowRight": SnakeGameState.arrow_right(),
                "ArrowDown": SnakeGameState.arrow_down(),
                ",": SnakeGameState.arrow_rel_left(),
                ".": SnakeGameState.arrow_rel_right(),
                "h": SnakeGameState.arrow_left(),
                "j": SnakeGameState.arrow_down(),
                "k": SnakeGameState.arrow_up(),
                "l": SnakeGameState.arrow_right(),
                "Escape": SnakeGameState.flip_switch(~SnakeGameState.running),  # type: ignore
            },
        ),
        rx.vstack(
            padding_button(),
            control_button(
                "arrow_left",
                on_click=SnakeGameState.arrow_left,
            ),
        ),
        rx.vstack(
            control_button(
                "arrow_up",
                on_click=SnakeGameState.arrow_up,
            ),
            control_button(
                "arrow_down",
                on_click=SnakeGameState.arrow_down,
            ),
        ),
        rx.vstack(
            padding_button(),
            control_button(
                "arrow_right",
                on_click=SnakeGameState.arrow_right,
            ),
        ),
        align="end",
    )



def snake_game():
    """Modern, responsive Snake game UI for Playground 202X."""
    return rx.box(
        # Sticky top navigation
        rx.box(
            rx.hstack(
                rx.link("← Back to Playground", href="/playground", font_size="1em", color=colors["link"], _hover={"text_decoration": "underline"}),
                rx.spacer(),
                rx.tooltip(
                    rx.icon_button(rx.icon("settings"), on_click=rx.noop, color_scheme="gray", size="2"),
                    label="Settings (coming soon)",
                    placement="bottom-end"
                ),
                width="100%",
                padding_x="2em",
                padding_y="1em",
            ),
            position="sticky",
            top="0",
            z_index="10",
            bg=colors["bg"],
            box_shadow="sm",
            font_family="'Quicksand', 'Poppins', 'Baloo 2', sans-serif",
        ),
        rx.flex(
            # Game grid area
            rx.box(
                rx.grid(
                    rx.foreach(
                        SnakeGameState.cells,
                        colored_box,
                    ),
                    columns=f"{N}",
                    gap="2px",
                    width="auto",
                    margin="0 auto",
                    align="center",
                ),
                bg=colors["card"],
                border_radius="xl",
                box_shadow="lg",
                padding="2em 1.5em 2em 1.5em",
                margin_bottom="1.5em",
                border=f"1px solid {colors['grid_border']}",
                font_family="'Quicksand', 'Poppins', 'Baloo 2', sans-serif",
            ),
            # Right panel: stats, controls
            rx.vstack(
                # Pause/Run controls
                rx.hstack(
                    rx.tooltip(
                        rx.button(
                            "PAUSE",
                            on_click=SnakeGameState.pause,
                            bg=colors["button_pause"],
                            color="#ffffff",
                            border_radius="full",
                            width="5em",
                            height="2.5em",
                            font_weight="bold",
                            box_shadow="md",
                        ),
                        label="Pause the game",
                        placement="bottom"
                    ),
                    rx.tooltip(
                        rx.button(
                            "RUN",
                            on_click=SnakeGameState.play,
                            bg=colors["button_run"],
                            color="#1a1a1a",
                            border_radius="full",
                            width="5em",
                            height="2.5em",
                            font_weight="bold",
                            box_shadow="md",
                        ),
                        label="Start/Resume the game",
                        placement="bottom"
                    ),
                    rx.tooltip(
                        rx.switch(checked=SnakeGameState.running, on_change=SnakeGameState.flip_switch),
                        label="Toggle auto-run",
                        placement="bottom"
                    ),
                    spacing="4",
                    margin_bottom="1em",
                ),
                # Stat cards
                rx.hstack(
                    stat_box("RATE", SnakeGameState.rate),
                    stat_box("SCORE", SnakeGameState.score),
                    stat_box("MAGIC", SnakeGameState.magic),
                    spacing="4",
                    margin_bottom="1em",
                ),
                # Game over message
                rx.cond(SnakeGameState.died, rx.heading("Game Over 🐍", color="#d63031", font_size="1.5em", margin_bottom="1em", font_family="'Baloo 2', cursive", font_weight="bold")),
                # Controls
                rx.box(
                    controls_panel(),
                    margin_top="1.5em",
                    padding="1em",
                    bg="rgba(255,255,255,0.12)",
                    border_radius="lg",
                    box_shadow="sm",
                ),
                align="center",
                spacing="2",
                font_family="'Quicksand', 'Poppins', 'Baloo 2', sans-serif",
            ),
            direction="row",
            justify="center",
            align="start",
            spacing="4",
            wrap="wrap",
            width="100vw",
            min_height="90vh",
            padding="2em",
        ),
        bg=colors["bg"],
        color=colors["text"],
        min_height="100vh",
        width="100vw",
        font_family="'Quicksand', 'Poppins', 'Baloo 2', sans-serif",
    )