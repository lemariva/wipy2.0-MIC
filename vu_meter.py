#Copyright [2017] [Mauro Riva <lemariva@mail.com> <lemariva.com>]

#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at

#http://www.apache.org/licenses/LICENSE-2.0

#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

#The above copyright notice and this permission notice shall be
#included in all copies or substantial portions of the Software.  

import math as m
import utime

from machine import ADC
from ws2812 import WS2812

class vu_meter:    
    ledsColors = []
    
    def __init__(self, ledNumber=144, ledPower = 100, adcWindow = 1500, adcMax = 100, adcPin = 'P13', pinLEDs = 'P22'):
        self.ledPower = ledPower
        self.ledNumber = ledNumber    
        self.pinLeds = pinLEDs
        self.adcPin = adcPin        
        self.adcWindow = adcWindow
        self.ledsColors = []      
        self.adcIn = 0.0
        self.adcMax = adcMax
        self.adcMaxDynamic = False        
        # inizialize ADC
        self.init_adc()
        self.init_leds()

    def init_adc(self):
        self.adc = ADC(0)
        self.adcUnit = self.adc.channel(pin=self.adcPin)
        self.adcMean = 0
        
    def init_leds(self):
        self.ledsColors = []        
        for x in range(0, self.ledNumber):
            color = self.color_vu_meter (x)
            self.ledsColors.append(color)
                                
        self.ledChain = WS2812( ledNumber=self.ledNumber, brightness=self.ledPower, dataPin=self.pinLeds ) # dataPin is for LoPy board only                        
        self.ledChain.show( self.ledsColors )        
        
    def test_leds(self):
        testData = self.ledsColors
        for x in range(0, self.ledNumber):
            testData = testData[1:] + testData[0:1]
            self.ledChain.show( testData )     
        self.ledChain.show([])     
    
    def lighter(self, color, percent):
        percent = percent / 100
        if(percent == 1):
            return color
        if(percent == 0):
            return ([0, 0, 0])	
        #if(percent < 0.65):		# driver not working ok with percent under 0.65 
        #   percent = 0.65

        rcolor = color[0] - color[0] * (1-percent)
        gcolor = color[1] - color[1] * (1-percent)
        bcolor = color[2] - color[2] * (1-percent)
        newcolor = ([(rcolor), (gcolor), (bcolor)])
        return newcolor		

    def color_vu_meter(self, position):
        rcolor = (255 * position) / self.ledNumber
        gcolor = (255 * (self.ledNumber - position)) / self.ledNumber 
        bcolor= 0
        newcolor = self.lighter([(rcolor), (gcolor), (bcolor)], self.ledPower)
        return newcolor
    
    def adc_max_dynamic(self, state = True, adcMax = 100):        
        self.adcMaxDynamic = state
        self.adcMax = adcMax
        return self.adcMaxDynamic
    
    def adc_max(self):
        return self.adcMax
        
    def zero_calibration(self):
        self.adcMean = 0        
        for y in range(0,  self.adcWindow): 
            self.adcMean = self.adcMean + self.adcUnit.value()
        self.adcMean = self.adcMean / self.adcWindow           
        return self.adcMean
        
    def update_rms(self):
        t1 = utime.ticks_ms()         
        power = 0
        self.audioPower = 0
        for x in range(0, self.adcWindow):    
            adc_value = self.adcUnit.value() - self.adcMean
            power = power + m.pow(adc_value, 2) 
            
        power = (m.sqrt(power / self.adcWindow))
        self.audioPower = power  
        
        t2 = utime.ticks_ms()
        time_elapsed =  t2 - t1    
        
        if(self.adcMaxDynamic):
            if(self.adcMax < power):
                self.adcMax = power
                
        self.normalizedPower = power / self.adcMax
        #20 * log10(sqrt(sum / count))
        
        if(self.normalizedPower > 1):
            self.normalizedPower = 1            
            
        return [time_elapsed, power]
            
    def update_leds(self):        
        leds_count = m.floor(self.normalizedPower * self.ledNumber)                
        self.ledChain.show( self.ledsColors[1:leds_count] )
