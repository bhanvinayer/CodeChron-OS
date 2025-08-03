"""
Memory Game - Visual Memory Challenge for Playground 202X
"""

import reflex as rx
from typing import List, Dict, Any
import random

class MemoryGameState(rx.State):
    """State for Memory Game"""
    cards: List[Dict[str, Any]] = []
    moves: int = 0
    score: int = 0
    game_started: bool = False
    game_completed: bool = False
    timer: int = 0
    difficulty: str = "medium"  # easy, medium, hard
    theme: str = "animals"  # animals, fruits, shapes, numbers
    
    # Card themes
    themes = {
        "animals": ["🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐯", "🦁", "🐸", "🐵"],
        "fruits": ["🍎", "🍊", "🍋", "🍌", "🍇", "🍓", "🥝", "🍑", "🍒", "🥭", "🍍", "🥥"],
        "shapes": ["⭐", "💎", "🔷", "🔸", "🔺", "🔻", "⚡", "💫", "✨", "🌟", "⭕", "🔥"],
        "numbers": ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟", "0️⃣", "🆕"]
    }
    
    # Difficulty settings
    difficulty_settings = {
        "easy": {"pairs": 6, "grid": (3, 4), "time_bonus": 5},
        "medium": {"pairs": 8, "grid": (4, 4), "time_bonus": 3}, 
        "hard": {"pairs": 12, "grid": (4, 6), "time_bonus": 2}
    }
    
    def set_difficulty(self, difficulty: str):
        """Set game difficulty"""
        self.difficulty = difficulty
        if self.game_started:
            self.reset_game()
    
    def set_theme(self, theme: str):
        """Set card theme"""
        self.theme = theme
        if self.game_started:
            self.reset_game()
    
    def start_game(self):
        """Initialize and start new game"""
        self.game_started = True
        self.game_completed = False
        self.moves = 0
        self.score = 0
        self.timer = 0
        
        # Get difficulty settings
        settings = self.difficulty_settings[self.difficulty]
        pairs_count = settings["pairs"]
        
        # Select random emojis for this game
        available_emojis = self.themes[self.theme]
        selected_emojis = random.sample(available_emojis, pairs_count)
        
        # Create pairs and shuffle
        card_values = selected_emojis * 2
        random.shuffle(card_values)
        
        # Create card objects
        self.cards = [
            {
                "id": i,
                "value": card_values[i],
                "flipped": False,
                "matched": False
            }
            for i in range(len(card_values))
        ]
    
    def flip_card(self, card_id: int):
        """Flip a card"""
        # Find the card and check if it can be flipped
        target_card = None
        flipped_count = 0
        
        for card in self.cards:
            if card["id"] == card_id:
                target_card = card
            if card["flipped"] and not card["matched"]:
                flipped_count += 1
        
        if (target_card is None or 
            target_card["flipped"] or 
            target_card["matched"] or 
            flipped_count >= 2 or
            not self.game_started or 
            self.game_completed):
            return
        
        # Flip the card
        target_card["flipped"] = True
        
        # Check for match when two cards are flipped
        flipped_cards = [card for card in self.cards if card["flipped"] and not card["matched"]]
        if len(flipped_cards) == 2:
            self.check_match()
    
    def check_match(self):
        """Check if flipped cards match"""
        flipped_cards = [card for card in self.cards if card["flipped"] and not card["matched"]]
        
        if len(flipped_cards) != 2:
            return
            
        card1, card2 = flipped_cards
        self.moves += 1
        
        if card1["value"] == card2["value"]:
            # Match found
            card1["matched"] = True
            card2["matched"] = True
            card1["flipped"] = False  # Matched cards don't need to show as flipped
            card2["flipped"] = False
            
            self.score += 100 + (self.difficulty_settings[self.difficulty]["time_bonus"] * max(0, 60 - self.timer))
            
            # Check if game is completed
            matched_count = len([card for card in self.cards if card["matched"]])
            if matched_count == len(self.cards):
                self.complete_game()
        else:
            # No match - cards will flip back after delay
            # For now, immediately flip them back
            card1["flipped"] = False
            card2["flipped"] = False
    
    def complete_game(self):
        """Complete the game"""
        self.game_completed = True
        bonus_score = max(0, 1000 - (self.moves * 10) - (self.timer * 5))
        self.score += bonus_score
    
    def reset_game(self):
        """Reset game to initial state"""
        self.game_started = False
        self.game_completed = False
        self.cards = []
        self.moves = 0
        self.score = 0
        self.timer = 0
    
    def increment_timer(self):
        """Increment game timer"""
        if self.game_started and not self.game_completed:
            self.timer += 1
    
    @rx.var
    def grid_columns(self) -> int:
        """Get number of grid columns for current difficulty"""
        return self.difficulty_settings[self.difficulty]["grid"][1]
    
    @rx.var 
    def grid_rows(self) -> int:
        """Get number of grid rows for current difficulty"""
        return self.difficulty_settings[self.difficulty]["grid"][0]
    
    @rx.var
    def completion_percentage(self) -> int:
        """Get game completion percentage"""
        if not self.cards:
            return 0
        matched_count = len([card for card in self.cards if card.get("matched", False)])
        return int((matched_count / len(self.cards)) * 100)

def memory_card(card: Dict[str, Any]) -> rx.Component:
    """Individual memory card component"""
    card_id = card["id"]
    
    # Simplify the flipped/matched logic using rx.cond
    is_flipped = rx.cond(
        card_id == 0,  # Placeholder condition - will be handled by state
        True,
        False
    )
    
    is_matched = rx.cond(
        card_id == 0,  # Placeholder condition - will be handled by state  
        True,
        False
    )
    
    return rx.box(
        rx.center(
            rx.cond(
                card["flipped"] | card["matched"],
                # Front of card (showing emoji)
                rx.text(
                    card["value"],
                    font_size="4.5rem",
                    opacity=rx.cond(card["matched"], "0.7", "1.0")
                ),
                # Back of card
                rx.text(
                    "❓",
                    font_size="4.5rem",
                    color="#ffffffcc",
                    opacity="0.9"
                )
            ),
            width="100%",
            height="100%"
        ),
        width="120px",
        height="120px",
        border_radius="16px",
        cursor="pointer",
        transition="all 0.3s ease",
        flex_shrink="0",
        bg=rx.cond(
            card["matched"],
            "rgba(16, 185, 129, 0.2)",
            rx.cond(
                card["flipped"],
                "rgba(255, 255, 255, 0.15)",
                "rgba(255, 255, 255, 0.1)"
            )
        ),
        backdrop_filter="blur(10px)",
        box_shadow=rx.cond(
            card["matched"],
            "0 8px 32px rgba(16, 185, 129, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.2)",
            "0 8px 32px rgba(255, 255, 255, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.2)"
        ),
        border="1px solid rgba(255, 255, 255, 0.2)",
        on_click=lambda: MemoryGameState.flip_card(card["id"]),
        _hover={
            "transform": "translateY(-8px) scale(1.05)",
            "box_shadow": "0 12px 40px rgba(155, 89, 182, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.3)",
            "backdrop_filter": "blur(15px)"
        }
    )

def game_controls() -> rx.Component:
    """Game control panel"""
    return rx.vstack(
        # Header
        rx.text(
            "🧠 Memory Challenge",
            font_size="2.5rem",
            font_weight="bold",
            text_align="center",
            color="#f1c40f",
            margin_bottom="1rem",
            font_family="'Poppins', sans-serif",
            text_shadow="0 2px 4px rgba(0, 0, 0, 0.3)"
        ),
        
        # Game stats
        rx.box(
            rx.hstack(
                rx.vstack(
                    rx.text(MemoryGameState.moves, font_size="2rem", font_weight="bold", color="#ffffff"),
                    rx.text("Moves", font_size="0.9rem", color="#ffffffaa"),
                    rx.text("🎯", font_size="1.5rem"),
                    align="center",
                    spacing="1"
                ),
                rx.vstack(
                    rx.text(MemoryGameState.score, font_size="2rem", font_weight="bold", color="#ffffff"),
                    rx.text("Score", font_size="0.9rem", color="#ffffffaa"), 
                    rx.text("⭐", font_size="1.5rem"),
                    align="center",
                    spacing="1"
                ),
                rx.vstack(
                    rx.text(MemoryGameState.timer, font_size="2rem", font_weight="bold", color="#ffffff"),
                    rx.text("Time", font_size="0.9rem", color="#ffffffaa"),
                    rx.text("⏱️", font_size="1.5rem"),
                    align="center",
                    spacing="1"
                ),
                rx.vstack(
                    rx.text(f"{MemoryGameState.completion_percentage}%", font_size="2rem", font_weight="bold", color="#ffffff"),
                    rx.text("Complete", font_size="0.9rem", color="#ffffffaa"),
                    rx.text("📊", font_size="1.5rem"),
                    align="center",
                    spacing="1"
                ),
                spacing="6",
                justify="center"
            ),
            bg="rgba(255, 255, 255, 0.1)",
            backdrop_filter="blur(10px)",
            border_radius="16px",
            padding="1.5rem",
            border="1px solid rgba(255, 255, 255, 0.2)",
            margin_bottom="1.5rem"
        ),
        
        # Progress bar
        rx.box(
            rx.box(
                width=f"{MemoryGameState.completion_percentage}%",
                height="100%",
                bg="linear-gradient(90deg, #f1c40f, #f39c12)",
                border_radius="8px",
                transition="width 0.5s ease",
                box_shadow="0 0 20px rgba(241, 196, 15, 0.5)"
            ),
            width="100%",
            height="8px",
            bg="rgba(255, 255, 255, 0.2)",
            border_radius="8px",
            margin_bottom="1.5rem",
            backdrop_filter="blur(5px)"
        ),
        
        # Controls
        rx.box(
            rx.hstack(
                # Difficulty selector
                rx.vstack(
                    rx.hstack(
                        rx.text("🧠", font_size="1.2rem"),
                        rx.text("Difficulty", font_weight="bold", color="#ffffff"),
                        spacing="2",
                        align="center"
                    ),
                    rx.select(
                        ["easy", "medium", "hard"],
                        value=MemoryGameState.difficulty,
                        on_change=MemoryGameState.set_difficulty,
                        size="2"
                    ),
                    align="center"
                ),
                
                # Theme selector
                rx.vstack(
                    rx.hstack(
                        rx.text("🎨", font_size="1.2rem"),
                        rx.text("Theme", font_weight="bold", color="#ffffff"),
                        spacing="2",
                        align="center"
                    ),
                    rx.select(
                        ["animals", "fruits", "shapes", "numbers"],
                        value=MemoryGameState.theme,
                        on_change=MemoryGameState.set_theme,
                        size="2"
                    ),
                    align="center"
                ),
                
                # Action buttons
                rx.vstack(
                    rx.button(
                        rx.cond(
                            MemoryGameState.game_started,
                            "🎮 New Game",
                            "🚀 Start Game"
                        ),
                        on_click=MemoryGameState.start_game,
                        color_scheme="yellow",
                        size="3",
                        font_weight="bold"
                    ),
                    rx.cond(
                        MemoryGameState.game_started,
                        rx.button(
                            "🔄 Reset",
                            on_click=MemoryGameState.reset_game,
                            variant="outline",
                            color_scheme="red",
                            size="2"
                        ),
                        rx.box()
                    ),
                    align="center"
                ),
                
                spacing="6",
                justify="center"
            ),
            bg="rgba(255, 255, 255, 0.1)",
            backdrop_filter="blur(10px)",
            border_radius="16px",
            padding="1.5rem",
            border="1px solid rgba(255, 255, 255, 0.2)",
            margin_bottom="1rem"
        ),
        
        align="center",
        width="100%"
    )

def game_board() -> rx.Component:
    """Game board with memory cards"""
    return rx.cond(
        MemoryGameState.game_started,
        rx.center(
            rx.grid(
                rx.foreach(
                    MemoryGameState.cards.to(rx.Var[list]),
                    memory_card
                ),
                columns=rx.cond(
                    MemoryGameState.difficulty == "hard", 
                    "6", 
                    "4"
                ),
                spacing="5",
                width="fit-content",
                justify="center"
            ),
            width="100%",
            margin_bottom="2rem"
        ),
        rx.flex(
            rx.box(
                rx.vstack(
                    rx.text("🎮", font_size="4rem", margin_bottom="0.5rem"),
                    rx.text(
                        "Ready to challenge your memory?",
                        font_size="1.6rem",
                        font_weight="bold",
                        color="#ffffff",
                        text_align="center",
                        margin_bottom="0.5rem"
                    ),
                    rx.text(
                        "Select your difficulty and theme, then click Start Game!",
                        color="#ffffffcc",
                        text_align="center",
                        font_size="1.1rem",
                        line_height="1.4"
                    ),
                    spacing="2",
                    align="center"
                ),
                bg="rgba(255, 255, 255, 0.12)",
                backdrop_filter="blur(15px)",
                border_radius="24px",
                padding="3rem 2.5rem",
                border="1px solid rgba(255, 255, 255, 0.25)",
                box_shadow="0 8px 32px rgba(0, 0, 0, 0.1)",
                min_width="400px",
                max_width="500px",
                _hover={
                    "transform": "translateY(-2px)",
                    "box_shadow": "0 12px 40px rgba(0, 0, 0, 0.15)"
                },
                transition="all 0.3s ease",
                margin="2rem auto 2rem 23%"  # Added top and bottom margins
            ),
            width="100%",
            height="350px",  # Increased height to accommodate margins
            align="center",
            justify="center"
        )
    )

def victory_modal() -> rx.Component:
    """Victory celebration modal"""
    return rx.cond(
        MemoryGameState.game_completed,
        rx.box(
            rx.center(
                rx.box(
                    rx.vstack(
                        rx.text("🎉", font_size="5rem"),
                        rx.text(
                            "Congratulations!",
                            font_size="2.5rem",
                            font_weight="bold",
                            color="#10B981",
                            text_align="center"
                        ),
                        rx.text(
                            "You completed the memory challenge!",
                            font_size="1.2rem",
                            color="#6B7280",
                            text_align="center"
                        ),
                        
                        # Final stats
                        rx.hstack(
                            rx.vstack(
                                rx.text("Final Score", font_weight="bold", color="#374151"),
                                rx.text(MemoryGameState.score, font_size="1.8rem", color="#10B981"),
                                align="center"
                            ),
                            rx.vstack(
                                rx.text("Total Moves", font_weight="bold", color="#374151"),
                                rx.text(MemoryGameState.moves, font_size="1.8rem", color="#3B82F6"),
                                align="center"
                            ),
                            rx.vstack(
                                rx.text("Time Taken", font_weight="bold", color="#374151"),
                                rx.text(f"{MemoryGameState.timer}s", font_size="1.8rem", color="#F59E0B"),
                                align="center"
                            ),
                            spacing="4",
                            margin="2rem 0"
                        ),
                        
                        rx.button(
                            "Play Again",
                            on_click=MemoryGameState.start_game,
                            color_scheme="purple",
                            size="3",
                            font_weight="bold"
                        ),
                        
                        spacing="4",
                        align="center"
                    ),
                    bg="rgba(255, 255, 255, 0.95)",
                    backdrop_filter="blur(20px)",
                    border_radius="20px",
                    padding="3rem",
                    box_shadow="0 25px 50px rgba(0, 0, 0, 0.25)",
                    border="2px solid rgba(255, 255, 255, 0.3)",
                    max_width="500px"
                ),
                width="100vw",
                height="100vh"
            ),
            position="fixed",
            top="0",
            left="0",
            bg="rgba(0, 0, 0, 0.8)",
            backdrop_filter="blur(10px)",
            z_index="1000"
        ),
        rx.box()
    )

def memory_game() -> rx.Component:
    """Memory Game application"""
    return rx.box(
        rx.vstack(
            game_controls(),
            game_board(),
            
            # Tips section
            rx.box(
                rx.hstack(
                    rx.text("💡", font_size="1.5rem"),
                    rx.vstack(
                        rx.text("Memory Tips:", font_weight="bold", color="#ffffff"),
                        rx.text(
                            "• Focus on card positions and patterns • Use mental associations • Practice regularly to improve • Take breaks to stay sharp",
                            color="#ffffffcc",
                            font_size="0.9rem"
                        ),
                        align="start"
                    ),
                    align="start",
                    spacing="3"
                ),
                bg="rgba(255, 255, 255, 0.1)",
                backdrop_filter="blur(10px)",
                border="1px solid rgba(255, 255, 255, 0.2)",
                border_radius="16px", 
                padding="1.5rem",
                margin_top="1rem"
            ),
            
            width="100%",
            max_width="1000px",
            margin="0 auto",
            padding="2rem",
            spacing="2"
        ),
        
        victory_modal(),
        
        width="100%",
        min_height="100vh",
        bg="linear-gradient(135deg, #2c3e50 0%, #4ca1af 100%)",
        position="relative"
    )
