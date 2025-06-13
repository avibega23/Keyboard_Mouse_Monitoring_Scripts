from pynput import mouse

def on_move(x, y):
    print(f'Pointer moved to {(x, y)}')

def on_click(x, y, button, pressed):
    print(f'{"Pressed" if pressed else "Released"} {button} at {(x, y)}')

def on_scroll(x, y, dx, dy):
    direction = 'down' if dy < 0 else 'up'
    print(f'Scrolled {direction} at {(x, y)}')

# Start the listener in blocking mode (runs until manually terminated)
with mouse.Listener(
    on_move=on_move,
    on_click=on_click,
    on_scroll=on_scroll
) as listener:
    listener.join()
