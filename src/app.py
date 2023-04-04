import os

from pynput import keyboard

from player import play


def on_press(key):
    path = os.getcwd()
    file = f"{path}/src/test2.mp3"
    play(file)
    try:
        print("alphanumeric key {0} pressed".format(key.char))
    except AttributeError:
        print("special key {0} pressed".format(key))


def main():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == "__main__":
    main()
