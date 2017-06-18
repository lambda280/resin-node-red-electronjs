# *
# * SHT1x Library
# *
# * Copyright 2009 Jonathan Oxer <jon@oxer.com.au> / <www.practicalarduino.com>
# *
# *

from machine import Pin
import time

# * ================  Public methods ================ */
#  Reads the current temperature in degrees Celsius

class SHT15:
    """SHT15 Sensor I/O Library using I2C'ish"""
    def __init__(self, dataPin, clockPin):
        self.dataPin = Pin(dataPin, mode=Pin.OUT)
        self.clockPin = Pin(clockPin, mode=Pin.IN)
    
    def readTemperatureC(self):
        D1 = -40.0
        D2 = 0.01
        val = self._readTemperatureRaw()
        temperature = (val * D2) + D1
        return temperature
    
    def readTemperatureF(self):
        D1 = -40.0
        D2 = 0.018
        val = self._readTemperatureRaw()
        temperature = (val * D2) + D1
        return temperature
    
    def readHumidity(self):
        C1 = -4.0
        C2 = 0.0405
        C3 = -0.0000028
        T1 = 0.01
        T2 = 0.00008

        gHumidCmd = 0b00000101

        self._sendCommandSHT(gHumidCmd)
        self._waitForResultSHT()
        val = self._getData16SHT()
        self._skipCrcSHT()

        linearHumidity = C1 + C2 * _val + C3 * val * val
        temperature = self.readTemperatureC()
        correctedHumidity = (temperature - 25.0 ) * (T1 +T2 * val) + linearHumidity
        return correctedHumidity

# ================  Private methods ================ */

    def _readTemperatureRaw(self):

        gTempCmd = 0b00000011

        self._sendCommandSHT(gTempCmd)
        self._waitForResultSHT()
        val = _getData16SHT()
        self._skipCrcSHT()
        return val

    def _shiftIn(self, numBits):
        # commands for reading/sending data to a SHTx sensor

        for i in range(numBits):
            self.clockPin(1)
            time.sleep(0.01)
            ret = ret * 2 + self.dataPin()
            self.clockPin(0)

        return ret

    def _sendCommandSHT(self, command):

        self.dataPin.mode(Pin.OUT)
        self.clockPin.mode(Pin.OUT)

        self.dataPin(1)
        self.clockPin(1)
        self.dataPin(0)
        self.clockPin(0)
        self.clockPin(1)
        self.dataPin(1)
        self.clockPin(0)

        self._shiftOut(MSBFIRST, command)

        self.clockPin(1)
        self.dataPin.mode(Pin.IN)
        ack = self.dataPin()
        if ack == 0:
            #Serial.println("Ack Error 8")
            pass
        self.clockPin(0)
        ack = self.dataPin
        if ack != 1:
            #Serial.println("Ack Error 1")
            pass

    def _waitForResultSHT(self):

        self.dataPin.mode(Pin.IN)
        for i in range(100):
            time.sleep(0.01)
            ack = self.dataPin()

            if ack == 0:
                break

        if ack == 1:
            #Serial.println("Ack Error 2")
            pass

    def _getData16SHT(self):

        self.dataPin.mode(Pin.IN)
        self.clockPin.mod(Pin.OUT)
        val = _shiftIn(8)
        val *= 256

        self.dataPin.mode(Pin.OUT)
        self.dataPin(1)
        self.dataPin(0)
        self.dataPin(1)
        self.dataPin(0)

        self.dataPin.mode(Pin.IN)
        val |= _shiftIn(8)

        return val

    def _skipCrcSHT(self):

        self.dataPin.mode(Pin.OUT)
        self.clockPin.mode(Pin.OUT)

        self.dataPin(1)
        self.clockPin(1)
        self.clockPin(0)
