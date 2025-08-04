"""
Password Generator App - Secure Passwords for Playground 202X
"""

import reflex as rx
import random
import string

class PasswordGenState(rx.State):
    password: str = ""
    length: int = 16
    use_upper: bool = True
    use_lower: bool = True
    use_digits: bool = True
    use_symbols: bool = True
    is_generating: bool = False

    def set_length(self, value):
        # Reflex slider passes a list, extract the first value
        if isinstance(value, list) and value:
            self.length = value[0]
        elif isinstance(value, int):
            self.length = value

    def toggle_upper(self):
        self.use_upper = not self.use_upper

    def toggle_lower(self):
        self.use_lower = not self.use_lower

    def toggle_digits(self):
        self.use_digits = not self.use_digits

    def toggle_symbols(self):
        self.use_symbols = not self.use_symbols

    def generate_password(self):
        self.is_generating = True
        chars = ""
        if self.use_upper:
            chars += string.ascii_uppercase
        if self.use_lower:
            chars += string.ascii_lowercase
        if self.use_digits:
            chars += string.digits
        if self.use_symbols:
            chars += string.punctuation
        if not chars:
            self.password = "Select at least one character set!"
        else:
            self.password = ''.join(random.choice(chars) for _ in range(self.length))
        self.is_generating = False

def password_generator_app() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.center(
                rx.vstack(
                    rx.text("🔒", font_size="4rem", margin_bottom="0.5rem"),
                    rx.text("Password Generator", font_size="3.5rem", font_weight="700", color="#BFC6D0", text_align="center"),
                    rx.text("Generate secure passwords instantly", font_size="1.3rem", color="#7C3AED", text_align="center", font_weight="400"),
                    align="center", spacing="4"
                ), width="100%", margin_bottom="3rem"
            ),
            rx.box(
                rx.vstack(
                    rx.text("Password Length", font_weight="600", font_size="1.2rem", color="#1F2937", margin_bottom="0.75rem"),
                    rx.slider(
                        min=6, max=32, step=1, value=[PasswordGenState.length],
                        on_change=PasswordGenState.set_length,
                        width="100%"
                    ),
                    rx.text(f"{PasswordGenState.length} characters", font_size="1.1rem", color="#1F2937", margin_bottom="1.5rem"),
                    rx.hstack(
                        rx.checkbox(checked=PasswordGenState.use_upper, on_change=PasswordGenState.toggle_upper, label="Uppercase", color_scheme="blue", font_size="1.1rem"),
                        rx.checkbox(checked=PasswordGenState.use_lower, on_change=PasswordGenState.toggle_lower, label="Lowercase", color_scheme="blue", font_size="1.1rem"),
                        rx.checkbox(checked=PasswordGenState.use_digits, on_change=PasswordGenState.toggle_digits, label="Digits", color_scheme="blue", font_size="1.1rem"),
                        rx.checkbox(checked=PasswordGenState.use_symbols, on_change=PasswordGenState.toggle_symbols, label="Symbols", color_scheme="blue", font_size="1.1rem"),
                        spacing="4", justify="center", width="100%"
                    ),
                    rx.center(
                        rx.button(
                            rx.cond(
                                PasswordGenState.is_generating,
                                rx.hstack(rx.spinner(size="1"), rx.text("Generating...", font_size="1.1rem", font_weight="500"), spacing="2"),
                                rx.text("Generate Password", font_size="1.1rem", font_weight="600")
                            ),
                            on_click=PasswordGenState.generate_password,
                            color_scheme="blue", size="4", height="3.5rem", padding="0 2rem", border_radius="12px",
                            box_shadow="0 4px 6px rgba(37, 99, 235, 0.2)", _hover={"box_shadow": "0 6px 20px rgba(37, 99, 235, 0.3)"}
                        ), width="100%", margin_bottom="2rem"
                    ),
                    rx.text("Your Password:", font_weight="600", font_size="1.2rem", color="#1F2937", margin_bottom="0.5rem"),
                    rx.text_area(
                        value=PasswordGenState.password,
                        height="80px", is_read_only=True, bg="#F9FAFB", font_size="1.8rem", border_radius="16px",
                        border="2px solid #BFDBFE", padding="1.25rem", color="#000000"
                    ),
                    width="100%", spacing="0"
                ),
                bg="white", border_radius="24px", padding="3rem",
                box_shadow="0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)",
                margin_bottom="3rem", border="1px solid #F3F4F6"
            ),
            width="900px", height="900px", padding="2rem",
            bg="linear-gradient(135deg, #1F2937 0%, #374151 50%, #4B5563 100%)",
            border_radius="48px", align="center", justify="center"
        ),
        width="100vw", height="100vh", align="center", justify="center"
    )

