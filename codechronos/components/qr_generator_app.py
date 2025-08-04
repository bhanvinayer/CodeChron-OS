"""
QR Code Generator App - Playground 202X
"""

import reflex as rx
import qrcode
import io
import base64

class QRGenState(rx.State):
    text: str = ""
    qr_image: str = ""
    is_generating: bool = False

    def set_text(self, value: str):
        self.text = value

    def generate_qr(self):
        self.is_generating = True
        if not self.text.strip():
            self.qr_image = ""
            self.is_generating = False
            return
        img = qrcode.make(self.text)
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        img_bytes = buf.getvalue()
        self.qr_image = "data:image/png;base64," + base64.b64encode(img_bytes).decode()
        self.is_generating = False

def qr_generator_app() -> rx.Component:
    return rx.center(
        rx.box(
            rx.vstack(
                rx.center(
                    rx.vstack(
                        rx.text("🔳", font_size="4rem", margin_bottom="0.5rem"),
                        rx.text("QR Code Generator", font_size="3.5rem", font_weight="700", color="#BFC6D0", text_align="center"),
                        rx.text("Create QR codes for any text or link", font_size="1.3rem", color="#7C3AED", text_align="center", font_weight="400"),
                        align="center", spacing="4"
                    ), width="100%", margin_bottom="2rem"
                ),
                rx.center(
                    rx.box(
                        rx.vstack(
                            rx.text("Text or Link", font_weight="600", font_size="1.2rem", color="#1F2937", margin_bottom="0.75rem"),
                            rx.text_area(
                                placeholder="Enter text or URL...",
                                value=QRGenState.text,
                                on_change=QRGenState.set_text,
                                bg="#EFF6EE",
                                height="80px",
                                resize="none",
                                font_size="1.8rem",
                                border_radius="16px",
                                border="2px solid #BFDBFE",
                                padding="1.25rem",
                                color="#000000",
                                line_height="1.6",
                                align="center"
                            ),
                            rx.center(
                                rx.button(
                                    rx.cond(
                                        QRGenState.is_generating,
                                        rx.hstack(rx.spinner(size="1"), rx.text("Generating...", font_size="1.1rem", font_weight="500"), spacing="2"),
                                        rx.text("Generate QR Code", font_size="1.1rem", font_weight="600")
                                    ),
                                    on_click=QRGenState.generate_qr,
                                    color_scheme="blue", size="4", height="3.5rem", padding="0 2rem", border_radius="12px",
                                    box_shadow="0 4px 6px rgba(37, 99, 235, 0.2)", _hover={"box_shadow": "0 6px 20px rgba(37, 99, 235, 0.3)"}
                                ), width="100%", margin_bottom="2rem"
                            ),
                            rx.cond(
                                QRGenState.qr_image,
                                rx.center(
                                    rx.image(src=QRGenState.qr_image, width="200px", height="200px", alt="QR Code"),
                                    margin_top="1.5rem"
                                ),
                                rx.center(
                                    rx.text("No QR code generated yet.", color="#999", font_size="1.1rem", margin_top="1.5rem")
                                )
                            ),
                            width="100%", spacing="0", align="center"
                        ),
                        bg="white", border_radius="32px", padding="3rem",
                        box_shadow="0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)",
                        border="1px solid #F3F4F6", width="500px"
                    )
                ),
                width="100%", spacing="0", align="center", justify="center"
            ),
            width="900px", height="900px", padding="2rem",
            bg="linear-gradient(135deg, #1F2937 0%, #374151 50%, #4B5563 100%)",
            border_radius="48px", align="center", justify="center"
        ),
        width="100vw", height="100vh", align="center", justify="center"
    )
