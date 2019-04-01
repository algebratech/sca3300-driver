import time

from sca3300 import SCA3300, Modes


def main():
    sca = SCA3300()
    sca.mode = Modes.MODE_3
    while True:
        print(sca.acceleration)
        time.sleep(0.02)


if __name__ == '__main__':
    main()
