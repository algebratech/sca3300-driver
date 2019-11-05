# SCA3300 Driver Package
> SCA3300 3-axis accelerometer Linux driver Python3 package.

## Requirements 
- Python 3.5+ (package uses static typing.)
- Linux (i.e Raspberry Pi or [https://github.com/TCAllen07/raspi-device-mocks](Mock))

## Installation 
#### PyPi
[https://pypi.org/project/sca3300/](https://pypi.org/project/sca3300/)  
You can install via
`pip install sca3300`
#### From Source 
* Clone repo `git clone https://github.com/algebratech/sca3300-driver`
* Install `python3 setup.py install --user`

## Usage
```py
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

```
