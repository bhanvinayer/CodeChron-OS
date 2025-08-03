Here's a simple timer app using Reflex. It has a start/stop button and a field to enter the number of seconds. When the timer reaches zero, it will display an alert.

```python
from reflex import core
from reflex import state as rx
from reflex import components as c
from reflex.components import vstack, button, text, hstack, textfield
import asyncio

class TimerApp(core.ReflexObject):
    def __init__(self):
        super().__init__()
        self.count = rx.State(0)
        self.timer = None
        self.alert = rx.State('')
        self.running = rx.State(False)

    def start_timer(self):
        self.alert.value = ''
        if self.running.value:
            if self.timer:
                self.timer.cancel()
            self.running.value = False
        else:
            self.running.value = True
            self.timer = asyncio.create_task(self._timer())

    async def _timer(self):
        while self.count.value > 0 and self.running.value:
            await asyncio.sleep(1)
            self.count.value -= 1
        if self.count.value <= 0 and self.running.value:
            self.alert.value = 'Time\'s Up!'
            self.running.value = False

    def render(self):
        return vstack(
            hstack(
                textfield(self.count, placeholder='Enter seconds', type='number'),
                button('Start/Stop', on_click=self.start_timer)
            ),
            text(self.alert, color='red' if self.alert.value else 'black'),
        )

if __name__ == "__main__":
    TimerApp().run()
```

This Reflex app uses asyncio to manage the timer as a separate task, which is cancelled and recreated whenever the start/stop button is pressed. The timer is decremented every second and the 'Time's Up!' alert is shown when the timer reaches zero. The timer stops when it reaches zero or if the start/stop button is pressed. The interface consists of a text field to enter the number of seconds and a start/stop button. The alert is shown in red when it is displayed.