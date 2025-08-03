"""
BlockCode 2015 Interface - Exact implementation from user prompt
"""

import reflex as rx

# Utility function for a block type label
def block_category(name: str, color: str, icon: str) -> rx.Component:
    return rx.box(
        rx.text(f"{icon} {name} +", font_size="0.95em", font_weight="500"),
        bg=color,
        p="0.6em",
        border_radius="8px",
        mb="0.5em",
        cursor="pointer",
        border="1px solid rgba(0,0,0,0.1)",
        _hover={"opacity": "0.85", "transform": "translateY(-1px)"},
    )

def block_editor() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            # Sidebar with block types
            rx.box(
                rx.text("🧱 Code Blocks", font_weight="bold", font_size="1.2em", mb="1em"),
                block_category("Action", "#B8E6B8", "⚡"),  # Pastel green
                block_category("If/Then", "#FFE4B5", "🔀"),  # Pastel peach
                block_category("Repeat", "#F0C8C8", "🔁"),  # Pastel pink
                block_category("Variable", "#D8BFD8", "🔣"),  # Pastel purple
                width="200px",
                p="1em",
                bg="white",
                border_right="1px solid #ccc",
                height="100%",
            ),
            # Canvas for dragging blocks
            rx.box(
                rx.text("BlockCode 2015", font_size="1.2em", font_weight="bold", mb="1em"),
                rx.box(
                    # Start block - more compact and block-like
                    rx.box(
                        rx.text("🚀 Start App", font_size="0.9em", font_weight="500", color="white"),
                        bg="#4CAF50",  # Solid green
                        p="0.8em 1.2em",
                        border_radius="6px",
                        box_shadow="0 2px 4px rgba(0,0,0,0.2)",
                        width="120px",
                        text_align="center",
                        mb="1em",
                        cursor="pointer",
                        _hover={"transform": "translateY(-1px)", "box_shadow": "0 3px 6px rgba(0,0,0,0.3)"}
                    ),
                    # Sample blocks in canvas
                    rx.box(
                        rx.text("⚡ Move Forward", font_size="0.85em", font_weight="500", color="white"),
                        bg="#66BB6A",  # Pastel action green
                        p="0.6em 1em",
                        border_radius="6px",
                        box_shadow="0 2px 4px rgba(0,0,0,0.15)",
                        width="140px",
                        text_align="center",
                        mb="0.5em",
                        cursor="pointer",
                        _hover={"transform": "translateY(-1px)"}
                    ),
                    rx.box(
                        rx.text("🔀 If touching edge", font_size="0.85em", font_weight="500", color="#333"),
                        bg="#FFE0B2",  # Pastel if/then orange
                        p="0.6em 1em",
                        border_radius="6px",
                        box_shadow="0 2px 4px rgba(0,0,0,0.15)",
                        width="150px",
                        text_align="center",
                        mb="0.5em",
                        cursor="pointer",
                        _hover={"transform": "translateY(-1px)"}
                    ),
                    rx.box(
                        rx.text("🔁 Repeat 10", font_size="0.85em", font_weight="500", color="#333"),
                        bg="#F8BBD9",  # Pastel repeat pink
                        p="0.6em 1em",
                        border_radius="6px",
                        box_shadow="0 2px 4px rgba(0,0,0,0.15)",
                        width="110px",
                        text_align="center",
                        cursor="pointer",
                        _hover={"transform": "translateY(-1px)"}
                    ),
                    bg="#f9f9ff",
                    border="1px solid #ccc",
                    border_radius="12px",
                    height="500px",
                    width="600px",
                    p="2em"
                ),
                width="80%",
                p="1em"
            ),
        ),
        # Run button footer
        rx.box(
            rx.text("▶ Run Blocks", font_size="1em", font_weight="500", color="white", bg="#2E7D32", p="0.8em 1.5em", border_radius="8px", width="fit-content", cursor="pointer", _hover={"bg": "#1B5E20"}),
            align="end",
            p="1em"
        ),
        width="100vw",
        height="100vh",
        bg="#eef0f8",
        spacing="0",
    )
