import reflex as rx

class TextEditorState(rx.State):
    content: str = ""
    filename: str = "Untitled.txt"
    is_modified: bool = False
    font_size: int = 16
    dark_mode: bool = False

    def update_content(self, new_content: str):
        self.content = new_content
        self.is_modified = True

    def new_file(self):
        self.content = ""
        self.filename = "Untitled.txt"
        self.is_modified = False

    def save_file(self):
        # In a real app, save to disk
        self.is_modified = False

    def set_font_size(self, size: str):
        self.font_size = int(size)

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode


def text_editor_menu() -> rx.Component:
    return rx.hstack(
        rx.button("New", on_click=TextEditorState.new_file, size="2", variant="ghost"),
        rx.button("Save", on_click=TextEditorState.save_file, size="2", variant="ghost"),
        rx.button(
            rx.cond(
                TextEditorState.dark_mode,
                rx.icon("sun", size=18),
                rx.icon("moon", size=18)
            ),
            on_click=TextEditorState.toggle_dark_mode,
            size="2",
            variant="ghost"
        ),
        rx.spacer(),
        rx.text(
            TextEditorState.filename + rx.cond(TextEditorState.is_modified, "*", ""),
            size="2",
            color=rx.cond(TextEditorState.dark_mode, "#F9FAFB", "#222")
        ),
        rx.spacer(),
        rx.text("Font Size:", size="2",color="#0F0F0F"),
        rx.select(
            ["12", "14", "16", "18", "20", "24"],
            value=str(TextEditorState.font_size),
            on_change=TextEditorState.set_font_size,
            width="60px"
        ),
        width="100%",
        padding="8px 16px",
        bg=rx.cond(TextEditorState.dark_mode, "#23272F", "#F3F4F6"),
        border_bottom="1px solid #E5E7EB"
    )

def text_editor_component() -> rx.Component:
    return rx.center(
        rx.box(
            rx.vstack(
                text_editor_menu(),
                rx.text_area(
                    value=TextEditorState.content,
                    on_change=TextEditorState.update_content,
                    placeholder="Start typing...",
                    width="100%",
                    height="400px",
                    font_size=f"{TextEditorState.font_size}px",
                    font_family="'JetBrains Mono', 'Fira Mono', 'Consolas', monospace",
                    color=rx.cond(TextEditorState.dark_mode, "#F9FAFB", "#111827"),
                    bg=rx.cond(TextEditorState.dark_mode, "#18181B", "white"),
                    border="none",
                    border_radius="0 0 8px 8px",
                    padding="20px",
                    resize="vertical",
                    _placeholder={"color": rx.cond(TextEditorState.dark_mode, "#4F4F52", "#6B7280")},
                    style={"outline": "none"}
                ),
                width="100%",
                spacing="0"
            ),
            width="900px",
            max_width="95vw",
            padding="2rem",
            bg=rx.cond(TextEditorState.dark_mode, "#23272F", "white"),
            border_radius="32px",
            box_shadow="0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)",
            border=rx.cond(TextEditorState.dark_mode, "1px solid #374151", "1px solid #E5E7EB")
        ),
        width="100vw", height="100vh", align="center", justify="center"
    )
