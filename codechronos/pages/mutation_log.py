"""
Mutation Log Page - Change history and rollback system
"""

import reflex as rx
import json
from datetime import datetime
from typing import List, Dict, Any

class Mutation(rx.Base):
    """Model for a mutation entry"""
    id: int
    timestamp: str
    type: str
    description: str
    author: str
    changes: str
    era: str

class MutationLogState(rx.State):
    """State for mutation log viewer"""
    mutations: List[Mutation] = []
    selected_mutation: Dict[str, Any] = {}
    filter_type: str = "all"  # all, code, ui, ai
    
    def load_mutations(self):
        """Load mutation history from data file"""
        # Sample mutation data
        self.mutations = [
            Mutation(
                id=1,
                timestamp="2025-08-02T14:30:00",
                type="code",
                description="Added calculator function",
                author="User",
                changes="+15 lines, -2 lines",
                era="vibe2025"
            ),
            Mutation(
                id=2,
                timestamp="2025-08-02T14:25:00", 
                type="ui",
                description="Modified button layout",
                author="AI Assistant",
                changes="+8 lines, -5 lines",
                era="block2015"
            ),
            Mutation(
                id=3,
                timestamp="2025-08-02T14:20:00",
                type="ai",
                description="Generated todo list component",
                author="GPT-4",
                changes="+45 lines",
                era="vibe2025"
            )
        ]
    
    def set_filter(self, filter_type: str):
        """Set mutation filter"""
        self.filter_type = filter_type
    
    def select_mutation(self, mutation: dict):
        """Select a mutation to view details"""
        self.selected_mutation = mutation
    
    def rollback_to_mutation(self, mutation_id: int):
        """Rollback to a specific mutation"""
        # Implementation would restore code state
        pass

def mutation_filters() -> rx.Component:
    """Filter controls for mutations"""
    return rx.hstack(
        rx.text("Filter by:", font_size="14px", color="gray"),
        rx.hstack(
            rx.button(
                "All",
                on_click=lambda: MutationLogState.set_filter("all"),
                variant=rx.cond(MutationLogState.filter_type == "all", "soft", "outline"),
                size="2"
            ),
            rx.button(
                "Code",
                on_click=lambda: MutationLogState.set_filter("code"),
                variant=rx.cond(MutationLogState.filter_type == "code", "soft", "outline"),
                color_scheme="blue",
                size="2"
            ),
            rx.button(
                "UI",
                on_click=lambda: MutationLogState.set_filter("ui"),
                variant=rx.cond(MutationLogState.filter_type == "ui", "soft", "outline"),
                color_scheme="green",
                size="2"
            ),
            rx.button(
                "AI",
                on_click=lambda: MutationLogState.set_filter("ai"),
                variant=rx.cond(MutationLogState.filter_type == "ai", "soft", "outline"),
                color_scheme="purple",
                size="2"
            ),
            spacing="2"
        ),
        align="center",
        spacing="3"
    )

def mutation_item(mutation: Mutation) -> rx.Component:
    """Individual mutation log item"""
    return rx.box(
        rx.hstack(
            rx.box(
                rx.text(
                    rx.cond(
                        mutation.type == "code", "🔧",
                        rx.cond(
                            mutation.type == "ui", "🎨", 
                            "🤖"
                        )
                    ),
                    font_size="20px"
                ),
                width="40px",
                display="flex",
                align_items="center",
                justify_content="center"
            ),
            rx.vstack(
                rx.hstack(
                    rx.text(
                        mutation.description,
                        font_size="16px",
                        font_weight="bold"
                    ),
                    rx.spacer(),
                    rx.text(
                        mutation.changes,
                        font_size="12px",
                        color="gray"
                    ),
                    width="100%"
                ),
                rx.hstack(
                    rx.text(
                        f"by {mutation.author}",
                        font_size="12px",
                        color="gray"
                    ),
                    rx.text("•", font_size="12px", color="gray"),
                    rx.text(
                        mutation.timestamp.split("T")[1][:5],
                        font_size="12px",
                        color="gray"
                    ),
                    rx.text("•", font_size="12px", color="gray"),
                    rx.badge(
                        mutation.era,
                        color_scheme=rx.cond(
                            mutation.era.contains("vibe"), "purple",
                            rx.cond(
                                mutation.era.contains("block"), "blue", 
                                "gray"
                            )
                        )
                    ),
                    spacing="2"
                ),
                align="start",
                width="100%",
                spacing="1"
            ),
            rx.hstack(
                rx.button(
                    "View",
                    on_click=lambda: MutationLogState.select_mutation(mutation),
                    size="1",
                    variant="outline"
                ),
                rx.button(
                    "Rollback",
                    on_click=lambda: MutationLogState.rollback_to_mutation(mutation.id),
                    size="1",
                    color_scheme="red",
                    variant="outline"
                ),
                spacing="2"
            ),
            align="center",
            width="100%",
            spacing="3"
        ),
        padding="1rem",
        border="1px solid #e5e7eb",
        border_radius="8px",
        margin_bottom="0.5rem",
        cursor="pointer",
        style={
            "&:hover": {
                "background": "#f9fafb"
            }
        }
    )

def mutation_list() -> rx.Component:
    """List of mutations"""
    return rx.vstack(
        rx.text("Recent Changes", font_size="20px", font_weight="bold"),
        mutation_filters(),
        rx.box(
            rx.foreach(
                MutationLogState.mutations,
                mutation_item
            ),
            max_height="500px",
            overflow_y="auto",
            width="100%"
        ),
        spacing="3",
        width="100%"
    )

def mutation_details() -> rx.Component:
    """Detailed view of selected mutation"""
    return rx.vstack(
        rx.text("Mutation Details", font_size="20px", font_weight="bold"),
        rx.cond(
            MutationLogState.selected_mutation,
            rx.vstack(
                rx.hstack(
                    rx.text("ID:", font_weight="bold"),
                    rx.text(MutationLogState.selected_mutation.get("id", "")),
                    width="100%"
                ),
                rx.hstack(
                    rx.text("Type:", font_weight="bold"),
                    rx.badge(MutationLogState.selected_mutation.get("type", "")),
                    width="100%"
                ),
                rx.hstack(
                    rx.text("Description:", font_weight="bold"),
                    rx.text(MutationLogState.selected_mutation.get("description", "")),
                    width="100%"
                ),
                rx.hstack(
                    rx.text("Author:", font_weight="bold"),
                    rx.text(MutationLogState.selected_mutation.get("author", "")),
                    width="100%"
                ),
                rx.hstack(
                    rx.text("Changes:", font_weight="bold"),
                    rx.text(MutationLogState.selected_mutation.get("changes", "")),
                    width="100%"
                ),
                rx.hstack(
                    rx.text("Era:", font_weight="bold"),
                    rx.badge(MutationLogState.selected_mutation.get("era", "")),
                    width="100%"
                ),
                rx.code_block(
                    "// Code diff would appear here\n+ function addNumbers(a, b) {\n+   return a + b;\n+ }",
                    language="javascript",
                    width="100%"
                ),
                spacing="2",
                align="start",
                width="100%"
            ),
            rx.text(
                "Select a mutation to view details",
                color="gray",
                text_align="center"
            )
        ),
        spacing="3",
        width="100%"
    )

def stats_panel() -> rx.Component:
    """Statistics panel"""
    return rx.vstack(
        rx.text("Statistics", font_size="20px", font_weight="bold"),
        rx.grid(
            rx.box(
                rx.text("12", font_size="24px", font_weight="bold", color="blue"),
                rx.text("Total Changes", font_size="12px", color="gray"),
                text_align="center",
                padding="1rem",
                border="1px solid #e5e7eb",
                border_radius="8px"
            ),
            rx.box(
                rx.text("3", font_size="24px", font_weight="bold", color="green"),
                rx.text("Code Changes", font_size="12px", color="gray"),
                text_align="center",
                padding="1rem",
                border="1px solid #e5e7eb",
                border_radius="8px"
            ),
            rx.box(
                rx.text("5", font_size="24px", font_weight="bold", color="purple"),
                rx.text("AI Generated", font_size="12px", color="gray"),
                text_align="center",
                padding="1rem",
                border="1px solid #e5e7eb",
                border_radius="8px"
            ),
            rx.box(
                rx.text("4", font_size="24px", font_weight="bold", color="orange"),
                rx.text("UI Changes", font_size="12px", color="gray"),
                text_align="center",
                padding="1rem",
                border="1px solid #e5e7eb",
                border_radius="8px"
            ),
            columns="2",
            spacing="2"
        ),
        spacing="3",
        width="100%"
    )

def mutation_log_page() -> rx.Component:
    """Complete mutation log interface"""
    return rx.box(
        rx.vstack(
            rx.text(
                "Mutation Log",
                font_size="32px",
                font_weight="bold",
                text_align="center",
                margin_bottom="2rem"
            ),
            rx.grid(
                mutation_list(),
                mutation_details(),
                stats_panel(),
                columns="2",
                spacing="4",
                width="100%"
            ),
            padding="2rem",
            max_width="1200px",
            margin="0 auto"
        ),
        on_mount=MutationLogState.load_mutations,
        width="100vw",
        min_height="100vh",
        bg="#f9fafb"
    )
