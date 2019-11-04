# The MIT License (MIT)
#
# Copyright (c) 2019 Orhan Istenhickorkmaz for Algebra Global, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
SCA3300 PCB Module

SCA3300 module is for quickly prototyping accelerometer with filters and
required components. It is known with its very low noise density.
It uses digital SPI interface for Raspberry Pi.
"""

import spidev

from utils.constant import Constant

_STANDARD_GRAVITY = 9.80665  # m/s^2

# 32 bit SPI commands to interact with device
_READ_ACC_X = Constant(0x040000F7)
_READ_ACC_Y = Constant(0x080000FD)
_READ_ACC_Z = Constant(0x0C0000FB)
_SW_RESET = Constant(0xB4002098)
_WHO_AM_I = Constant(0x40000091)
_SELF_TEST = Constant(0x100000E9)
_SUMMARY = Constant(0x180000E5)
_MODE_1 = Constant(0xB400001F)
_MODE_2 = Constant(0xB4000102)
_MODE_3 = Constant(0xB4000225)
_MODE_4 = Constant(0xB4000338)

_MODE_1_SENSITIVITY = Constant(2700)
_MODE_2_SENSITIVITY = Constant(1350)
_MODE_3_SENSITIVITY = Constant(5400)


class Modes:
    """
    There are 4 different modes i.e
    `Mode 1,
     Mode 2,
     Mode 3,
     and Mode 4`
    """

    MODE_1 = Constant(0b00)
    MODE_2 = Constant(0b01)
    MODE_3 = Constant(0b10)
    MODE_4 = Constant(0b11)


class SCA3300:
    """
    SCA300 driver class.
    :param max_speed: SPI maximum frequency rate
    :param bus: On which bus accelerometer connected?
    :param device: Which device is accelerometer?
    """

    def __init__(self, max_speed: int = 7629, bus: int = 0, device: int = 0) -> None:
        self._spi = spidev.SpiDev()
        self._spi.open(bus, device)
        self._spi.max_speed_hz = max_speed
        self._current_mode = _MODE_3
        # Only mode 0 is supported!
        self._spi.mode = 0
        self._spi.xfer2(_MODE_3.value.to_bytes(length=4, byteorder='big'))

    @property
    def mode(self) -> Modes:
        if self._current_mode is _MODE_1:
            return Modes.MODE_1
        elif self._current_mode is _MODE_2:
            return Modes.MODE_2
        elif self._current_mode is _MODE_3:
            return Modes.MODE_3
        else:
            return Modes.MODE_4

    @mode.setter
    def mode(self, mode: Modes) -> None:
        """
        Set sensor's working mode i.e max gravity
        :param mode:
        """
        if mode is Modes.MODE_2:
            self._current_mode = _MODE_2
        elif mode is Modes.MODE_1:
            self._current_mode = _MODE_1
        elif mode is Modes.MODE_3:
            self._current_mode = _MODE_3
        else:
            self._current_mode = _MODE_4
        self._spi.xfer2(self._current_mode.value.to_bytes(length=4, byteorder='big'))

    @property
    def acceleration(self) -> tuple:
        """
        Here we return X, Y and Z data.
        It sends current request's response in next SPI frame. Therefore, the order
        is different.
        :return: float list as three axis data
        """
        result_x = self._spi.xfer2(_READ_ACC_Y.value.to_bytes(length=4, byteorder='big'))
        x = self._convert_acceleration(result_x[1], result_x[2]) * _STANDARD_GRAVITY
        result_y = self._spi.xfer2(_READ_ACC_Z.value.to_bytes(length=4, byteorder='big'))
        y = self._convert_acceleration(result_y[1], result_y[2]) * _STANDARD_GRAVITY
        result_z = self._spi.xfer2(_READ_ACC_X.value.to_bytes(length=4, byteorder='big'))
        z = self._convert_acceleration(result_z[1], result_z[2]) * _STANDARD_GRAVITY
        return x, y, z

    def _convert_acceleration(self, first_byte: str, second_byte: str) -> float:
        overall = hex(int(first_byte) << 8 | int(second_byte))
        signed_value = self.to_signed(int(overall, 16))
        if self._current_mode is _MODE_1:
            return signed_value / _MODE_1_SENSITIVITY.value
        elif self._current_mode is _MODE_2:
            return signed_value / _MODE_2_SENSITIVITY.value
        else:
            return signed_value / _MODE_3_SENSITIVITY.value

    @staticmethod
    def to_signed(value: int) -> int:
        return -(value & 0x8000) | (value & 0x7fff)
