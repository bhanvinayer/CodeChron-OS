"""
Todo List App - Task Management for Playground 202X
"""

import reflex as rx
from typing import List, Dict, Any
import datetime

class TodoState(rx.State):
    """State for Todo List App"""
    tasks: List[Dict[str, Any]] = []
    new_task: str = ""
    filter_mode: str = "all"  # all, active, completed
    
    def add_task(self):
        """Add a new task"""
        if self.new_task.strip():
            task = {
                "id": len(self.tasks) + 1,
                "text": self.new_task.strip(),
                "completed": False,
                "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                "priority": "normal"  # low, normal, high
            }
            self.tasks.append(task)
            self.new_task = ""
    
    def set_new_task(self, value: str):
        """Set the new task input value"""
        self.new_task = value
    
    def toggle_task(self, task_id: int):
        """Toggle task completion status"""
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = not task["completed"]
                break
    
    def delete_task(self, task_id: int):
        """Delete a task"""
        self.tasks = [task for task in self.tasks if task["id"] != task_id]
    
    def set_priority(self, task_id: int, priority: str):
        """Set task priority"""
        for task in self.tasks:
            if task["id"] == task_id:
                task["priority"] = priority
                break
    
    def clear_completed(self):
        """Remove all completed tasks"""
        self.tasks = [task for task in self.tasks if not task["completed"]]
    
    def set_filter(self, filter_mode: str):
        """Set task filter mode"""
        self.filter_mode = filter_mode
    
    @rx.var
    def filtered_tasks(self) -> List[Dict[str, Any]]:
        """Get filtered tasks based on current filter mode"""
        if self.filter_mode == "active":
            return [task for task in self.tasks if not task["completed"]]
        elif self.filter_mode == "completed":
            return [task for task in self.tasks if task["completed"]]
        else:
            return self.tasks
    
    @rx.var
    def active_tasks_count(self) -> int:
        """Get count of active tasks"""
        return len([task for task in self.tasks if not task.get("completed", False)])
    
    @rx.var  
    def completed_tasks_count(self) -> int:
        """Get count of completed tasks"""
        return len([task for task in self.tasks if task.get("completed", False)])
    
    @rx.var
    def total_tasks_count(self) -> int:
        """Get total count of tasks"""
        return len(self.tasks)

def priority_badge(priority: str) -> rx.Component:
    """Priority badge component"""
    colors = {
        "low": "#4CAF50",
        "normal": "#2196F3", 
        "high": "#F44336"
    }
    
    return rx.badge(
        rx.cond(
            priority == "low",
            "Low",
            rx.cond(
                priority == "normal", 
                "Normal",
                "High"
            )
        ),
        bg=rx.cond(
            priority == "low",
            "#4CAF50",
            rx.cond(
                priority == "normal",
                "#2196F3", 
                "#F44336"
            )
        ),
        color="white",
        font_size="0.7rem"
    )

def task_item(task: Dict[str, Any]) -> rx.Component:
    """Individual task item component"""
    return rx.box(
        rx.hstack(
            # Checkbox
            rx.checkbox(
                checked=task["completed"],
                on_change=lambda _: TodoState.toggle_task(task["id"]),
                color_scheme="green"
            ),
            
            # Task content
            rx.vstack(
                rx.hstack(
                    rx.text(
                        task["text"],
                        font_size="1rem",
                        color=rx.cond(task["completed"], "#666", "#333"),
                        text_decoration=rx.cond(task["completed"], "line-through", "none"),
                        flex="1"
                    ),
                    priority_badge(task["priority"]),
                    align="center"
                ),
                rx.text(
                    f"Created: {task['created_at']}",
                    font_size="0.8rem",
                    color="#999"
                ),
                align="start",
                spacing="1",
                flex="1"
            ),
            
            # Priority selector
            rx.select(
                ["low", "normal", "high"],
                value=task["priority"],
                on_change=lambda value: TodoState.set_priority(task["id"], value),
                size="1",
                width="80px"
            ),
            
            # Delete button
            rx.button(
                "🗑️",
                on_click=lambda: TodoState.delete_task(task["id"]),
                variant="ghost",
                size="1",
                color_scheme="red",
                _hover={"bg": "#ffebee"}
            ),
            
            justify="between",
            align="center",
            width="100%"
        ),
        
        bg=rx.cond(task["completed"], "#f8f9fa", "white"),
        border="1px solid #e0e0e0",
        border_radius="8px",
        padding="1rem",
        margin_bottom="0.5rem",
        _hover={"box_shadow": "0 2px 8px rgba(0,0,0,0.1)"},
        transition="all 0.2s ease"
    )

def todo_app() -> rx.Component:
    """Todo List application"""
    return rx.vstack(
        # Header
        rx.hstack(
            rx.text(
                "📝 Todo List",
                font_size="2rem",
                font_weight="bold",
                color="#1976D2"
            ),
            rx.spacer(),
            rx.hstack(
                rx.vstack(
                    rx.text(TodoState.active_tasks_count, font_size="2rem", font_weight="bold", color="#2196F3"),
                    rx.text("Active", font_size="0.9rem", color="#666"),
                    rx.text("📋", font_size="1.2rem"),
                    align="center"
                ),
                rx.vstack(
                    rx.text(TodoState.completed_tasks_count, font_size="2rem", font_weight="bold", color="#4CAF50"),
                    rx.text("Done", font_size="0.9rem", color="#666"),
                    rx.text("✅", font_size="1.2rem"),
                    align="center"
                ),
                rx.vstack(
                    rx.text(TodoState.total_tasks_count, font_size="2rem", font_weight="bold", color="#FF9800"),
                    rx.text("Total", font_size="0.9rem", color="#666"),
                    rx.text("📊", font_size="1.2rem"),
                    align="center"
                ),
                spacing="8"
            ),
            width="100%",
            margin_bottom="2rem"
        ),
        
        # Add new task
        rx.box(
            rx.vstack(
                rx.text("Add New Task", font_weight="bold", margin_bottom="0.5rem"),
                rx.hstack(
                    rx.input(
                        placeholder="Enter a new task...",
                        value=TodoState.new_task,
                        on_change=TodoState.set_new_task,
                        flex="1",
                        size="3"
                    ),
                    rx.button(
                        "Add Task",
                        on_click=TodoState.add_task,
                        color_scheme="blue",
                        size="3"
                    ),
                    width="100%"
                ),
                align="start"
            ),
            bg="white",
            border="1px solid #e0e0e0",
            border_radius="12px",
            padding="1.5rem",
            margin_bottom="2rem",
            box_shadow="0 2px 4px rgba(0,0,0,0.05)"
        ),
        
        # Filter buttons
        rx.hstack(
            rx.hstack(
                rx.button(
                    "All",
                    on_click=lambda: TodoState.set_filter("all"),
                    variant=rx.cond(TodoState.filter_mode == "all", "solid", "outline"),
                    color_scheme="blue"
                ),
                rx.button(
                    "Active",
                    on_click=lambda: TodoState.set_filter("active"),
                    variant=rx.cond(TodoState.filter_mode == "active", "solid", "outline"),
                    color_scheme="blue"
                ),
                rx.button(
                    "Completed",
                    on_click=lambda: TodoState.set_filter("completed"),
                    variant=rx.cond(TodoState.filter_mode == "completed", "solid", "outline"),
                    color_scheme="blue"
                ),
                spacing="0"
            ),
            rx.spacer(),
            rx.button(
                "Clear Completed",
                on_click=TodoState.clear_completed,
                variant="outline",
                color_scheme="red",
                size="1"
            ),
            width="100%",
            margin_bottom="1rem"
        ),
        
        # Tasks list
        rx.box(
            rx.cond(
                TodoState.total_tasks_count > 0,
                rx.vstack(
                    rx.foreach(
                        TodoState.filtered_tasks.to(rx.Var[list]),
                        task_item
                    ),
                    width="100%"
                ),
                rx.center(
                    rx.vstack(
                        rx.text("📝", font_size="4rem", color="#ddd"),
                        rx.text(
                            "No tasks yet!",
                            font_size="1.2rem",
                            color="#999"
                        ),
                        rx.text(
                            "Add your first task above to get started!",
                            color="#666"
                        ),
                        spacing="3",
                        align="center"
                    ),
                    height="200px"
                )
            ),
            width="100%",
            min_height="300px"
        ),
        
        # Productivity tip
        rx.box(
            rx.hstack(
                rx.text("💡", font_size="1.5rem"),
                rx.vstack(
                    rx.text("Productivity Tip:", font_weight="bold", color="#1976D2"),
                    rx.text(
                        "Set priorities for your tasks and tackle high-priority items first. Break large tasks into smaller, manageable steps!",
                        color="#666",
                        font_size="0.9rem"
                    ),
                    align="start"
                ),
                align="start",
                spacing="3"
            ),
            bg="linear-gradient(135deg, #E3F2FD, #F3E5F5)",
            border="1px solid #BBDEFB",
            border_radius="12px",
            padding="1rem",
            margin_top="2rem"
        ),
        
        width="100%",
        max_width="800px",
        margin="0 auto",
        padding="2rem",
        bg="linear-gradient(135deg, #F8F9FA 0%, #E9ECEF 100%)",
        min_height="100vh"
    )
