import os

from player import play


def main():
    path = os.getcwd()
    print(path)
    file = f"{path}/src/test.mp3"
    play(file)


if __name__ == "__main__":
    main()
