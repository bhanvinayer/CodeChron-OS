"""
Calculator - 1984 Mac-style calculator
"""

import reflex as rx

class CalculatorState(rx.State):
    """Calculator state management"""
    display: str = "0"
    previous_value: float = 0.0
    operation: str = ""
    waiting_for_operand: bool = False
    last_input: str = ""
    last_value: float = 0.0

    def input_digit(self, digit: str):
        """Input a digit"""
        if self.waiting_for_operand:
            self.display = digit
            self.waiting_for_operand = False
        else:
            self.display = self.display + digit if self.display != "0" else digit
        self.last_input = "digit"

    def input_decimal(self):
        """Input decimal point"""
        if self.waiting_for_operand:
            self.display = "0."
            self.waiting_for_operand = False
        elif "." not in self.display:
            self.display += "."
        self.last_input = "decimal"

    def clear(self):
        """Clear calculator"""
        self.display = "0"
        self.previous_value = 0.0
        self.operation = ""
        self.waiting_for_operand = False
        self.last_input = ""
        self.last_value = 0.0

    def toggle_sign(self):
        """Toggle positive/negative sign"""
        if self.display != "0":
            if self.display.startswith("-"):
                self.display = self.display[1:]
            else:
                self.display = "-" + self.display
        self.last_input = "sign"

    def calculate_percentage(self):
        """Calculate percentage"""
        try:
            value = float(self.display)
            self.display = str(value / 100)
            self.waiting_for_operand = True
        except Exception:
            self.display = "Error"
            self.waiting_for_operand = True
        self.last_input = "%"

    def perform_operation(self, next_operation: str):
        """Perform calculation"""
        try:
            input_value = float(self.display)
        except Exception:
            self.display = "Error"
            self.waiting_for_operand = True
            self.operation = next_operation
            return

        if self.operation and not self.waiting_for_operand:
            # Complete the previous operation
            try:
                result = self._calculate(self.previous_value, input_value, self.operation)
                self.display = str(result)
                self.previous_value = result
            except Exception:
                self.display = "Error"
                self.previous_value = 0.0
        else:
            self.previous_value = input_value

        self.operation = next_operation
        self.waiting_for_operand = True
        self.last_input = "op"
        self.last_value = input_value

    def equals(self):
        """Perform calculation on the current and previous operand"""
        try:
            input_value = float(self.display)
        except Exception:
            self.display = "Error"
            self.waiting_for_operand = True
            return

        if self.operation:
            if self.last_input == "equals":
                # Repeat last operation
                left = input_value
                right = self.last_value
            else:
                left = self.previous_value
                right = input_value
                self.last_value = input_value
            try:
                result = self._calculate(left, right, self.operation)
                self.display = str(result)
                self.previous_value = result
            except Exception:
                self.display = "Error"
                self.previous_value = 0.0
            self.waiting_for_operand = True
            self.last_input = "equals"

    def _calculate(self, left, right, op):
        """Internal method to perform calculation"""
        if op == "+":
            return left + right
        elif op == "-":
            return left - right
        elif op == "×":
            return left * right
        elif op == "÷":
            if right == 0:
                raise ZeroDivisionError
            return left / right
        return right

def calculator_button(label: str, on_click, btn_type: str = "num") -> rx.Component:
    """Create a calculator button with modern style"""
    # Button color logic
    if btn_type == "func":  # C, ±
        bg = "#c0c5ce"
        color = "#1a2233"
        border = "1.5px solid #222"
    elif btn_type == "op":  # operators
        bg = "#f7cfa4"
        color = "#222"
        border = "2px solid #b97b1e"
    else:  # num, dot
        bg = "#fff"
        color = "#111"
        border = "1.5px solid #222"
    return rx.button(
        label,
        on_click=on_click,
        width="60px",
        height="60px",
        font_size="1.5rem",
        font_family="'Press Start 2P', monospace",
        bg=bg,
        color=color,
        border=border,
        box_shadow="0 2px 6px rgba(0,0,0,0.07)",
        _hover={"bg": "#e6e6e6" if btn_type=="num" else bg},
        transition="all 0.15s"
    )

def calculator_component() -> rx.Component:
    """Modern calculator layout and style"""
    return rx.center(
        rx.center(
            rx.vstack(
                # Display
                rx.box(
                    rx.text(
                        CalculatorState.display,
                        size="7",
                        weight="bold",
                        text_align="right",
                        font_family="'VT323', monospace",
                        color="#111"
                    ),
                    width="100%",
                    height="80px",
                    padding="1.2rem",
                    bg="#fff",
                    border="2.5px solid #111",
                    border_radius="12px",
                    margin_bottom="1.2rem",
                    box_shadow="0 2px 10px rgba(0,0,0,0.07)",
                    display="flex",
                    align_items="center",
                    justify_content="flex-end"
                ),
                # Button grid
                rx.vstack(
                    # Row 1
                rx.hstack(
                    calculator_button("C", CalculatorState.clear, "func"),
                    calculator_button("±", CalculatorState.toggle_sign, "func"),
                    calculator_button("%", CalculatorState.calculate_percentage, "func"),
                    calculator_button("÷", lambda: CalculatorState.perform_operation("÷"), "op"),
                    spacing="2"
                ),
                    # Row 2
                rx.hstack(
                    calculator_button("7", lambda: CalculatorState.input_digit("7"), "num"),
                    calculator_button("8", lambda: CalculatorState.input_digit("8"), "num"),
                    calculator_button("9", lambda: CalculatorState.input_digit("9"), "num"),
                    calculator_button("×", lambda: CalculatorState.perform_operation("×"), "op"),
                    spacing="2"
                ),
                    # Row 3
                rx.hstack(
                    calculator_button("4", lambda: CalculatorState.input_digit("4"), "num"),
                    calculator_button("5", lambda: CalculatorState.input_digit("5"), "num"),
                    calculator_button("6", lambda: CalculatorState.input_digit("6"), "num"),
                    calculator_button("-", lambda: CalculatorState.perform_operation("-"), "op"),
                    spacing="2"
                ),
                    # Row 4
                rx.hstack(
                    calculator_button("1", lambda: CalculatorState.input_digit("1"), "num"),
                    calculator_button("2", lambda: CalculatorState.input_digit("2"), "num"),
                    calculator_button("3", lambda: CalculatorState.input_digit("3"), "num"),
                    calculator_button("+", lambda: CalculatorState.perform_operation("+"), "op"),
                    spacing="2"
                ),
                    # Row 5
                rx.hstack(
                    rx.button(
                        "0",
                        on_click=lambda: CalculatorState.input_digit("0"),
                        width="128px",  # Double width
                        height="60px",
                        font_size="1.5rem",
                        font_family="'Press Start 2P', monospace",
                        bg="#fff",
                        color="#111",
                        border="1.5px solid #222",
                        box_shadow="0 2px 6px rgba(0,0,0,0.07)",
                        _hover={"bg": "#e6e6e6"},
                        transition="all 0.15s"
                    ),
                    calculator_button(".", CalculatorState.input_decimal, "num"),
                    calculator_button("=", CalculatorState.equals, "op"),
                    spacing="2"
                ),
                spacing="2"
                ),
                spacing="2",
                bg="#f8f9fa",
                border="2px solid #111",
                border_radius="18px",
                padding="1.5rem 1.2rem 1.2rem 1.2rem",
                box_shadow="0 4px 18px rgba(0,0,0,0.09)"
            ),
            bg="#f4f5f7",
            padding="2.5rem",
            border_radius="24px",
            border="2.5px solid #111",
            box_shadow="0 8px 32px rgba(0,0,0,0.10)",
            min_width="340px",
            max_width="380px",
        ),
        width="100vw",
        height="100vh",
        align="center",
        justify="center"
    )
