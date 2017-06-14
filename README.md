Vu-meter using a WiPy 2.0, some WS2812B and a SPW2430
------------------------------------------------
This project is about connecting a **Wipy 2.0** with a **SPW2430** MEMS microphone and **WS2812B** led strip. The **Wipy 2.0** measures the MEMS output and calculate the RMS of the signal on a defined time window and switches on the led strip proportional to this value simulating a vu-meter.

Hardware
----------------
* Wipy 2.0
* SPW2430 MEMS microphone
* W2812B ledstrip

Check the blog article for more information:  http://lemariva.com/blog/2017/06/wipy2-0-vu-meter-using-ws2812b-and-spw2430

Wiring 
---------------

|		|		|		|
|:-----:|:-----:|:-----:|
|**Wipy 2.0**|**W2812B**|**SPW2430**|
| `3.3v`| `VCC` | `VIN`|
| `GND` | `GND` | `GND`|
| `P11`(`G22`) | `GREEN CABLE`  |	   |
| `P13`(`G5`) | | `DC`  |


Preview
--------------------


Changelog
-------------------
* Revision 0.1b

More info & help:
-----------
* Blog article: http://lemariva.com/blog/2017/06/wipy2-0-vu-meter-using-ws2812b-and-spw2430
* Wipy2.0: https://docs.pycom.io/pycom_esp32/pycom_esp32/wipy2.html
* WS2812B: https://cdn-shop.adafruit.com/datasheets/WS2812B.pdf

Library
--------------------
* WS2812B: 	https://goo.gl/AnPIij

License:
---------------
* Apache 2.0
