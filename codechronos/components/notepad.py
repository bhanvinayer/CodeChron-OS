"""
Notepad - Simple text editor component
"""

import reflex as rx

class NotepadState(rx.State):
    """Notepad state management"""
    content: str = "Welcome to MacPad!\n\nType your text here..."
    filename: str = "Untitled"
    is_modified: bool = False
    font_size: int = 12
    
    def update_content(self, new_content: str):
        """Update text content"""
        self.content = new_content
        self.is_modified = True
    
    def new_file(self):
        """Create new file"""
        self.content = ""
        self.filename = "Untitled"
        self.is_modified = False
    
    def save_file(self):
        """Save current file"""
        # In a real implementation, this would save to filesystem
        self.is_modified = False
    
    def change_font_size(self, size: int):
        """Change font size"""
        self.font_size = size

def notepad_menu() -> rx.Component:
    """Notepad menu bar"""
    return rx.hstack(
        rx.menu.root(
            rx.menu.trigger(
                rx.button("File", variant="ghost", size="2")
            ),
            rx.menu.content(
                rx.menu.item("New", on_click=NotepadState.new_file),
                rx.menu.item("Save", on_click=NotepadState.save_file),
                rx.menu.separator(),
                rx.menu.item("Exit")
            )
        ),
        rx.menu.root(
            rx.menu.trigger(
                rx.button("Format", variant="ghost", size="2")
            ),
            rx.menu.content(
                rx.menu.item("Font Size 10", on_click=lambda: NotepadState.change_font_size(10)),
                rx.menu.item("Font Size 12", on_click=lambda: NotepadState.change_font_size(12)),
                rx.menu.item("Font Size 14", on_click=lambda: NotepadState.change_font_size(14)),
                rx.menu.item("Font Size 16", on_click=lambda: NotepadState.change_font_size(16))
            )
        ),
        spacing="2",
        width="100%",
        padding="0.5rem",
        bg=rx.color("gray", 2),
        border_bottom=f"1px solid {rx.color('gray', 6)}"
    )

def notepad_status_bar() -> rx.Component:
    """Status bar showing file info"""
    return rx.hstack(
        rx.text(
            NotepadState.filename + rx.cond(NotepadState.is_modified, "*", ""),
            size="1",
            color=rx.color("gray", 10)
        ),
        rx.spacer(),
        rx.text(
            f"Font: {NotepadState.font_size}px",
            size="1", 
            color=rx.color("black", 12)
        ),
        width="100%",
        padding="0.5rem",
        bg=rx.color("gray", 2),
        border_top=f"1px solid {rx.color('gray', 6)}"
    )

def notepad_component() -> rx.Component:
    """Complete notepad component"""
    return rx.vstack(
        notepad_menu(),
        rx.text_area(
            value=NotepadState.content,
            on_change=NotepadState.update_content,
            placeholder="Start typing...",
            width="100%",
            height="420px",
            font_family="'VT323', monospace",
            font_size=f"{NotepadState.font_size}px",
            color="#111",
            resize="none",
            style={
                "background": "white",
                "border": "1px solid #ccc",
                "padding": "1rem",
                "color": "#111",
                "caretColor": "#111"
            },
            _placeholder={"color": "#111"}
        ),
        notepad_status_bar(),
        spacing="0",
        width="100%",
        height="100%",
        bg="white"
    )
