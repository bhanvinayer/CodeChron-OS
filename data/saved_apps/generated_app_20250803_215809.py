from reflex import App, Component, rx, State

class NoteState(State):
    def __init__(self):
        self.notes = []
        self.current_note = ''


class NotesApp(Component):
    state = NoteState()

    def render(self):
        return rx.Main(
            rx.H1('Notes App', _style='text-align: center'),
            rx.Input(_model=self.state.current_note, placeholder='Your note here...', _style='width: 100%; margin-top: 20px'),
            rx.Button('Add Note', _style='margin-top: 10px; width: 100%', _on_click=self.add_note),
            rx.Div(
                [
                    rx.P(note, _style='margin-top: 10px; border: 1px solid #ccc; padding: 10px') 
                    for note in self.state.notes
                ], 
                _style='margin-top: 20px'
            )
        )

    def add_note(self):
        if self.state.current_note.strip() != '':
            self.state.notes.append(self.state.current_note.strip())
            self.state.current_note = ''


if __name__ == '__main__':
    app = App(NotesApp)
    app.run()
```
This code creates a simple notes app using the Reflex framework. The app has an input field for writing a note, a button to add the note to a list of notes, and a display area for the list of notes. The notes are stored in the app's state, so they persist even when the component re-renders. The add_note method adds the current note to the list of notes, but only if the note isn't just empty space. After adding the note, it clears the input field.