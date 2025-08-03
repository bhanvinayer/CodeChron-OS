"""
Interface Builder - Visual Mac App Designer for MacCode 1984
"""

import reflex as rx
from typing import Dict, List, Any, Optional

class InterfaceBuilderState(rx.State):
    """State for Interface Builder application"""
    current_project: str = "My App"
    selected_element_id: Optional[str] = None
    active_tab: str = "interface"  # interface or code
    is_running: bool = False  # True when app is running, False when in design mode
    
    # UI Elements on canvas
    ui_elements: List[Dict[str, Any]] = [
        {
            "id": "button-1754238948158",
            "type": "button",
            "text": "Click Me",
            "x": 145,
            "y": 114,
            "width": 80,
            "height": 24,
            "selected": True
        }
    ]
    
    # Design canvas properties
    canvas_width: int = 400
    canvas_height: int = 300
    
    def select_element(self, element_id: str):
        """Select an element for editing"""
        # Deselect all elements first
        for element in self.ui_elements:
            element["selected"] = False
        
        # Select the clicked element
        for element in self.ui_elements:
            if element["id"] == element_id:
                element["selected"] = True
                self.selected_element_id = element_id
                break
    
    def add_element(self, element_type: str):
        """Add a new UI element to the canvas"""
        import time
        element_id = f"{element_type}-{int(time.time() * 1000)}"
        
        new_element = {
            "id": element_id,
            "type": element_type,
            "text": f"New {element_type.title()}",
            "x": 50,
            "y": 50,
            "width": 100 if element_type == "button" else 150,
            "height": 24 if element_type == "button" else 20,
            "selected": False
        }
        
        # Deselect all existing elements
        for element in self.ui_elements:
            element["selected"] = False
            
        # Add and select new element
        new_element["selected"] = True
        self.ui_elements.append(new_element)
        self.selected_element_id = element_id
    
    def update_element_property(self, property_name: str, value: Any):
        """Update a property of the selected element"""
        if not self.selected_element_id:
            return
            
        for element in self.ui_elements:
            if element["id"] == self.selected_element_id:
                if property_name in ["x", "y", "width", "height"]:
                    try:
                        element[property_name] = int(value)
                    except (ValueError, TypeError):
                        pass
                else:
                    element[property_name] = value
                break
    
    def delete_selected_element(self):
        """Delete the currently selected element"""
        if not self.selected_element_id:
            return
            
        self.ui_elements = [
            element for element in self.ui_elements 
            if element["id"] != self.selected_element_id
        ]
        self.selected_element_id = None
    
    def set_active_tab(self, tab: str):
        """Switch between interface and code tabs"""
        self.active_tab = tab
    
    def build_and_run(self):
        """Switch to run mode to show the built app"""
        self.is_running = True
        # Deselect all elements when running
        for element in self.ui_elements:
            element["selected"] = False
        self.selected_element_id = None
    
    def stop_app(self):
        """Return to design mode"""
        self.is_running = False
    
    def get_selected_element(self) -> Optional[Dict[str, Any]]:
        """Get the currently selected element"""
        if not self.selected_element_id:
            return None
            
        for element in self.ui_elements:
            if element["id"] == self.selected_element_id:
                return element
        return None
    
    @rx.var
    def selected_element_text(self) -> str:
        """Get the text of the selected element"""
        selected = self.get_selected_element()
        return selected["text"] if selected else ""
    
    @rx.var 
    def selected_element_x(self) -> str:
        """Get the X position of the selected element"""
        selected = self.get_selected_element()
        return str(selected["x"]) if selected else "0"
    
    @rx.var
    def selected_element_y(self) -> str:
        """Get the Y position of the selected element"""
        selected = self.get_selected_element()
        return str(selected["y"]) if selected else "0"
    
    @rx.var
    def selected_element_width(self) -> str:
        """Get the width of the selected element"""
        selected = self.get_selected_element()
        return str(selected["width"]) if selected else "0"
    
    @rx.var
    def selected_element_height(self) -> str:
        """Get the height of the selected element"""
        selected = self.get_selected_element()
        return str(selected["height"]) if selected else "0"
    
    @rx.var
    def canvas_width_px(self) -> str:
        """Get canvas width as px string"""
        return str(self.canvas_width) + "px"
    
    @rx.var
    def canvas_height_px(self) -> str:
        """Get canvas height as px string"""
        return str(self.canvas_height) + "px"

def title_bar() -> rx.Component:
    """Render the title bar with project name and build button"""
    return rx.hstack(
        rx.text("MacCode 1984", size="4", weight="bold", color="black"),
        rx.spacer(),
        rx.cond(
            InterfaceBuilderState.is_running,
            rx.button(
                "◀ Back to Design",
                variant="solid",
                color_scheme="blue",
                size="2",
                on_click=InterfaceBuilderState.stop_app
            ),
            rx.button(
                "▶ Build & Run",
                variant="solid",
                color_scheme="green",
                size="2",
                on_click=InterfaceBuilderState.build_and_run
            )
        ),
        width="100%",
        padding="0.5rem",
        background="linear-gradient(to bottom, #f0f0f0, #d0d0d0)",
        border_bottom="1px solid #999",
        align="center"
    )

def left_sidebar() -> rx.Component:
    """Render the left sidebar with project files and UI elements"""
    return rx.vstack(
        # Project Files Section
        rx.vstack(
            rx.text("Project Files", size="2", weight="bold", color="black"),
            rx.vstack(
                rx.hstack(
                    rx.text("📄", size="2"),
                    rx.text("App.mac", size="2", color="black"),
                    spacing="1"
                ),
                rx.hstack(
                    rx.text("🖥️", size="2"),
                    rx.text("Interface.mac", size="2", color="black"),
                    spacing="1"
                ),
                spacing="1",
                padding_left="0.5rem",
                align="start"
            ),
            spacing="2",
            align="start"
        ),
        
        # UI Elements Section
        rx.vstack(
            rx.text("UI Elements", size="2", weight="bold", color="black"),
            rx.vstack(
                rx.button(
                    rx.hstack(
                        rx.text("🔘", size="2"),
                        rx.text("Button", size="2"),
                        spacing="1"
                    ),
                    variant="ghost",
                    size="1",
                    width="100%",
                    justify="start",
                    on_click=InterfaceBuilderState.add_element("button")
                ),
                rx.button(
                    rx.hstack(
                        rx.text("📝", size="2"),
                        rx.text("Text", size="2"),
                        spacing="1"
                    ),
                    variant="ghost",
                    size="1",
                    width="100%",
                    justify="start",
                    on_click=InterfaceBuilderState.add_element("text")
                ),
                rx.button(
                    rx.hstack(
                        rx.text("📥", size="2"),
                        rx.text("Input", size="2"),
                        spacing="1"
                    ),
                    variant="ghost",
                    size="1",
                    width="100%",
                    justify="start",
                    on_click=InterfaceBuilderState.add_element("input")
                ),
                spacing="1",
                width="100%",
                align="start"
            ),
            spacing="2",
            align="start"
        ),
        
        width="200px",
        height="100%",
        padding="1rem",
        background="#f8f8f8",
        border_right="1px solid #ccc",
        spacing="4",
        align="start"
    )

def properties_panel() -> rx.Component:
    """Render the properties panel for the selected element"""
    
    return rx.cond(
        InterfaceBuilderState.selected_element_id,
        rx.vstack(
            rx.text("Properties", size="2", weight="bold", color="black"),
            
            # Text property
            rx.vstack(
                rx.text("Text:", size="1", color="black"),
                rx.input(
                    value=InterfaceBuilderState.selected_element_text,
                    on_change=lambda value: InterfaceBuilderState.update_element_property("text", value),
                    size="1"
                ),
                spacing="1",
                align="start"
            ),
            
            # Position properties
            rx.hstack(
                rx.vstack(
                    rx.text("X:", size="1", color="black"),
                    rx.input(
                        value=InterfaceBuilderState.selected_element_x,
                        on_change=lambda value: InterfaceBuilderState.update_element_property("x", value),
                        size="1",
                        width="60px"
                    ),
                    spacing="1",
                    align="start"
                ),
                rx.vstack(
                    rx.text("Y:", size="1", color="black"),
                    rx.input(
                        value=InterfaceBuilderState.selected_element_y,
                        on_change=lambda value: InterfaceBuilderState.update_element_property("y", value),
                        size="1",
                        width="60px"
                    ),
                    spacing="1",
                    align="start"
                ),
                spacing="2"
            ),
            
            # Size properties
            rx.hstack(
                rx.vstack(
                    rx.text("Width:", size="1", color="black"),
                    rx.input(
                        value=InterfaceBuilderState.selected_element_width,
                        on_change=lambda value: InterfaceBuilderState.update_element_property("width", value),
                        size="1",
                        width="60px"
                    ),
                    spacing="1",
                    align="start"
                ),
                rx.vstack(
                    rx.text("Height:", size="1", color="black"),
                    rx.input(
                        value=InterfaceBuilderState.selected_element_height,
                        on_change=lambda value: InterfaceBuilderState.update_element_property("height", value),
                        size="1",
                        width="60px"
                    ),
                    spacing="1",
                    align="start"
                ),
                spacing="2"
            ),
            
            # Delete button
            rx.button(
                "❌ Delete",
                variant="outline",
                color_scheme="red",
                size="1",
                on_click=InterfaceBuilderState.delete_selected_element
            ),
            
            spacing="3",
            align="start",
            width="100%"
        ),
        rx.vstack(
            rx.text("Properties", size="2", weight="bold", color="black"),
            rx.text("No element selected", size="1", color="gray"),
            spacing="2",
            align="start"
        )
    )

def design_canvas() -> rx.Component:
    """Render the main design canvas with UI elements"""
    return rx.box(
        # Window chrome
        rx.vstack(
            # Title bar of the app being designed
            rx.hstack(
                rx.text(InterfaceBuilderState.current_project, size="2", weight="bold", color="black"),
                rx.spacer(),
                rx.text("●●●", size="1", color="#666"),
                width="100%",
                padding="0.3rem 0.5rem",
                background="linear-gradient(to bottom, #e0e0e0, #c0c0c0)",
                border="1px solid #999",
                align="center"
            ),
            
            # Content area with UI elements
            rx.box(
                rx.foreach(
                    InterfaceBuilderState.ui_elements,
                    lambda element: rx.box(
                        rx.cond(
                            element["type"] == "button",
                            rx.button(
                                element["text"],
                                size="1",
                                variant="outline"
                            ),
                            rx.cond(
                                element["type"] == "text",
                                rx.text(element["text"], size="2", color="black"),
                                rx.input(
                                    placeholder=element["text"],
                                    size="1"
                                )
                            )
                        ),
                        position="absolute",
                        left=element["x"],
                        top=element["y"],
                        border=rx.cond(
                            element["selected"],
                            "2px dashed red",
                            "1px solid transparent"
                        ),
                        cursor="pointer",
                        on_click=InterfaceBuilderState.select_element(element["id"])
                    )
                ),
                position="relative",
                width=InterfaceBuilderState.canvas_width_px,
                height=InterfaceBuilderState.canvas_height_px,
                background="white",
                border="1px solid #999",
                overflow="hidden"
            ),
            
            spacing="0",
            width="fit-content"
        ),
        
        padding="2rem",
        width="100%",
        height="100%",
        background="#f0f0f0",
        overflow="auto"
    )

def tab_bar() -> rx.Component:
    """Render the tab bar for switching between interface and code views"""
    return rx.hstack(
        rx.button(
            "Interface Builder",
            variant=rx.cond(InterfaceBuilderState.active_tab == "interface", "solid", "ghost"),
            size="2",
            on_click=InterfaceBuilderState.set_active_tab("interface")
        ),
        rx.button(
            "Code Editor",
            variant=rx.cond(InterfaceBuilderState.active_tab == "code", "solid", "ghost"),
            size="2",
            on_click=InterfaceBuilderState.set_active_tab("code")
        ),
        spacing="1",
        padding="0.5rem",
        background="#e8e8e8",
        border_bottom="1px solid #ccc"
    )

def status_bar() -> rx.Component:
    """Render the status bar with current mode and selected element info"""
    return rx.hstack(
        rx.text("Design Mode – Click elements to select, drag to move", size="1", color="black"),
        rx.spacer(),
        rx.cond(
            InterfaceBuilderState.selected_element_id,
            rx.text(f"Selected: {InterfaceBuilderState.selected_element_id}", size="1", color="blue"),
            rx.text("No selection", size="1", color="gray")
        ),
        width="100%",
        padding="0.5rem",
        background="linear-gradient(to bottom, #f0f0f0, #d0d0d0)",
        border_top="1px solid #999",
        align="center"
    )

def code_editor() -> rx.Component:
    """Render the code editor view"""
    return rx.vstack(
        rx.text("Code Editor", size="4", weight="bold", text_align="center"),
        rx.box(
            rx.html(
                """
                <textarea 
                    style="
                        width: 100%; 
                        height: 400px; 
                        font-family: 'Monaco', 'Courier New', monospace; 
                        font-size: 12px;
                        background: #1e1e1e;
                        color: #d4d4d4;
                        border: 1px solid #3c3c3c;
                        padding: 10px;
                        resize: none;
                    "
                    readonly
                >// Generated Mac Application Code
// Project: My App

Window "My App" {
    Width: 400
    Height: 300
    
    Button "Click Me" {
        X: 145
        Y: 114
        Width: 80
        Height: 24
        OnClick: HandleButtonClick
    }
}

Function HandleButtonClick() {
    ShowMessage("Button was clicked!");
}</textarea>
                """
            ),
            width="100%"
        ),
        spacing="3",
        width="100%",
        height="100%",
        padding="2rem"
    )

def running_app() -> rx.Component:
    """Render the running application (what the user built)"""
    return rx.center(
        rx.vstack(
            # Mac-style window chrome
            rx.hstack(
                rx.text(InterfaceBuilderState.current_project, size="2", weight="bold", color="black"),
                rx.spacer(),
                rx.text("●●●", size="1", color="#666"),
                width="100%",
                padding="0.3rem 0.5rem",
                background="linear-gradient(to bottom, #e0e0e0, #c0c0c0)",
                border="1px solid #999",
                align="center"
            ),
            
            # Content area with functioning UI elements
            rx.box(
                rx.foreach(
                    InterfaceBuilderState.ui_elements,
                    lambda element: rx.box(
                        rx.cond(
                            element["type"] == "button",
                            rx.button(
                                element["text"],
                                size="1",
                                variant="solid",
                                color_scheme="gray",
                                on_click=rx.window_alert(f"Button '{element['text']}' clicked!")
                            ),
                            rx.cond(
                                element["type"] == "text",
                                rx.text(element["text"], size="2", color="black"),
                                rx.input(
                                    placeholder=element["text"],
                                    size="1"
                                )
                            )
                        ),
                        position="absolute",
                        left=element["x"],
                        top=element["y"]
                    )
                ),
                position="relative",
                width=InterfaceBuilderState.canvas_width_px,
                height=InterfaceBuilderState.canvas_height_px,
                background="white",
                border="1px solid #999",
                overflow="hidden"
            ),
            
            spacing="0",
            width="fit-content",
            border="2px solid #666",
            border_radius="4px",
            box_shadow="0 4px 8px rgba(0,0,0,0.3)"
        ),
        width="100%",
        height="100%",
        background="#d0d0d0",
        padding="2rem"
    )

def interface_builder() -> rx.Component:
    """Main Interface Builder component"""
    return rx.cond(
        InterfaceBuilderState.is_running,
        # Running app view - show only the built app
        rx.vstack(
            title_bar(),
            running_app(),
            width="100%",
            height="100vh",
            spacing="0",
            background="#d0d0d0"
        ),
        # Design mode - show full Interface Builder
        rx.vstack(
            title_bar(),
            
            rx.hstack(
                left_sidebar(),
                
                # Main content area
                rx.vstack(
                    tab_bar(),
                    
                    rx.cond(
                        InterfaceBuilderState.active_tab == "interface",
                        design_canvas(),
                        code_editor()
                    ),
                    
                    flex="1",
                    width="100%"
                ),
                
                # Right properties panel
                rx.box(
                    properties_panel(),
                    width="200px",
                    height="100%",
                    padding="1rem",
                    background="#f8f8f8",
                    border_left="1px solid #ccc"
                ),
                
                width="100%",
                height="calc(100vh - 100px)",
                spacing="0"
            ),
            
            status_bar(),
            
            width="100%",
            height="100vh",
            spacing="0",
            background="#f0f0f0"
        )
    )
