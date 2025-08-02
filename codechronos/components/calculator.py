"""
Calculator - 1984 Mac-style calculator
"""

import reflex as rx

class CalculatorState(rx.State):
    """Calculator state management"""
    display: str = "0"
    previous_value: float = 0
    operation: str = ""
    waiting_for_operand: bool = False
    
    def input_digit(self, digit: str):
        """Input a digit"""
        if self.waiting_for_operand:
            self.display = digit
            self.waiting_for_operand = False
        else:
            self.display = self.display + digit if self.display != "0" else digit
    
    def input_decimal(self):
        """Input decimal point"""
        if self.waiting_for_operand:
            self.display = "0."
            self.waiting_for_operand = False
        elif "." not in self.display:
            self.display += "."
    
    def clear(self):
        """Clear calculator"""
        self.display = "0"
        self.previous_value = 0
        self.operation = ""
        self.waiting_for_operand = False
    
    def toggle_sign(self):
        """Toggle positive/negative sign"""
        if self.display != "0":
            if self.display.startswith("-"):
                self.display = self.display[1:]
            else:
                self.display = "-" + self.display
    
    def calculate_percentage(self):
        """Calculate percentage"""
        value = float(self.display)
        self.display = str(value / 100)
        self.waiting_for_operand = True
    
    def perform_operation(self, next_operation: str):
        """Perform calculation"""
        input_value = float(self.display)
        
        if self.previous_value == 0:
            self.previous_value = input_value
        elif self.operation:
            current_value = self.previous_value
            
            if self.operation == "+":
                result = current_value + input_value
            elif self.operation == "-":
                result = current_value - input_value
            elif self.operation == "×":
                result = current_value * input_value
            elif self.operation == "÷":
                result = current_value / input_value if input_value != 0 else 0
            else:
                result = input_value
            
            self.display = str(result)
            self.previous_value = result
        
        self.waiting_for_operand = True
        self.operation = next_operation

def calculator_button(label: str, on_click, color_scheme: str = "gray") -> rx.Component:
    """Create a calculator button"""
    return rx.button(
        label,
        on_click=on_click,
        width="60px",
        height="60px",
        font_size="18px",
        font_family="'Press Start 2P', monospace",
        color_scheme=color_scheme,
        variant="solid"
    )

def calculator_component() -> rx.Component:
    """Mac-style calculator component"""
    return rx.vstack(
        # Display
        rx.box(
            rx.text(
                CalculatorState.display,
                size="6",
                weight="bold",
                text_align="right",
                font_family="'VT323', monospace"
            ),
            width="100%",
            height="80px",
            padding="1rem",
            bg="black",
            color="green",
            border="2px inset #ccc",
            display="flex",
            align_items="center",
            justify_content="flex-end"
        ),
        
        # Button grid
        rx.vstack(
            # Row 1
            rx.hstack(
                calculator_button("C", CalculatorState.clear, "red"),
                calculator_button("±", CalculatorState.toggle_sign),
                calculator_button("%", CalculatorState.calculate_percentage), 
                calculator_button("÷", lambda: CalculatorState.perform_operation("÷"), "orange"),
                spacing="2"
            ),
            # Row 2
            rx.hstack(
                calculator_button("7", lambda: CalculatorState.input_digit("7")),
                calculator_button("8", lambda: CalculatorState.input_digit("8")),
                calculator_button("9", lambda: CalculatorState.input_digit("9")),
                calculator_button("×", lambda: CalculatorState.perform_operation("×"), "orange"),
                spacing="2"
            ),
            # Row 3
            rx.hstack(
                calculator_button("4", lambda: CalculatorState.input_digit("4")),
                calculator_button("5", lambda: CalculatorState.input_digit("5")),
                calculator_button("6", lambda: CalculatorState.input_digit("6")),
                calculator_button("-", lambda: CalculatorState.perform_operation("-"), "orange"),
                spacing="2"
            ),
            # Row 4
            rx.hstack(
                calculator_button("1", lambda: CalculatorState.input_digit("1")),
                calculator_button("2", lambda: CalculatorState.input_digit("2")),
                calculator_button("3", lambda: CalculatorState.input_digit("3")),
                calculator_button("+", lambda: CalculatorState.perform_operation("+"), "orange"),
                spacing="2"
            ),
            # Row 5
            rx.hstack(
                rx.button(
                    "0",
                    on_click=lambda: CalculatorState.input_digit("0"),
                    width="128px",  # Double width
                    height="60px",
                    font_size="18px",
                    font_family="'Press Start 2P', monospace"
                ),
                calculator_button(".", CalculatorState.input_decimal),
                calculator_button("=", lambda: CalculatorState.perform_operation(""), "orange"),
                spacing="2"
            ),
            spacing="2"
        ),
        spacing="3",
        align="center",
        bg=rx.color("gray", 2),
        padding="1rem",
        border_radius="8px",
        border="2px solid #666"
    )
