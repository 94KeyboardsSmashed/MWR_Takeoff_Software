# -*- coding: utf-8 -*
# Python Neopixel Libraries Module

"""
Created on Mon Oct 2 12:13:27 2017

@author: Hyun-seok

IMPORTANT: THIS MODULE REQUIRES ROOT ACCESS TO RUN.
Uses indents

Adopted from the Adafruit NeoPixel Libraries Module created by
Tony DiCola (tony@tonydicola.com), Jeremy Garff (jer@jers.net)

"""

import time
import atexit
import _rpi_ws281x as ws


def color_value(red, green, blue, white=0):
    """
    Convert the provided red, green, blue color to a 24-bit color value.

    Parameters
    ----------
    red : int
        The brightness value of red between 0 (lowest) to 255 (highest)
    green : int
        The brightness value of green between 0 (lowest) to 255 (highest)
    blue : int
        The brightness value of blue between 0 (lowest) to 255 (highest)
    white=0 : int
        The whiteness value of the overall color between 0 (lowest) to 255 (highest)

    Returns
    -------
    int
        A 24 bit color value to be used with functions like colorwipe
    """
    return (white << 24) | (green << 16)| (red << 8) | blue

def wheel(pos):
    """
    Generate rainbow colors across 0-255 positions. Used mainly for the class
    function rainbow_cycle().

    Parameters
    ----------
    pos : int
        Cannot really figure this out. Use at your own risk. Maybe the position of
        the light being changed?

    Returns
    -------
    int
        A 24 bit color value for creating a neopixel rainbow

    """
    if pos < 85:
        return color_value(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return color_value(255 - pos * 3, 0, pos * 3)
    # else:
    pos -= 170
    return color_value(0, pos * 3, 255 - pos * 3)


class _LED_Data(object):
    """Wrapper class which makes a SWIG LED color data array look and feel like
    a Python list of integers.
    """
    def __init__(self, channel, size):
        self.size = size
        self.channel = channel

    def __getitem__(self, pos):
        """Return the 24-bit RGB color value at the provided position or slice
        of positions.
        """
        # Handle if a slice of positions are passed in by grabbing all the values
        # and returning them in a list.
        if isinstance(pos, slice):
            return [ws.ws2811_led_get(self.channel, n) for n in range(*pos.indices(self.size))]
        # Else assume the passed in value is a number to the position.
        return ws.ws2811_led_get(self.channel, pos)

    def __setitem__(self, pos, value):
        """Set the 24-bit RGB color value at the provided position or slice of
        positions.
        """
        # Handle if a slice of positions are passed in by setting the appropriate
        # LED data values to the provided values.
        if isinstance(pos, slice):
            index = 0
            for itra in range(*pos.indices(self.size)):
                ws.ws2811_led_set(self.channel, itra, value[index])
                index += 1
        # Else assume the passed in value is a number to the position.
        else:
            return ws.ws2811_led_set(self.channel, pos, value)


class Adafruit_NeoPixel(object):
    """See __init__ docstrings for more info"""
    def __init__(self, num, pin, freq_hz=800000, dma=5, invert=False,
                 brightness=255, channel=0, strip_type=ws.WS2811_STRIP_RGB):
        """Class to represent a NeoPixel/WS281x LED display.  Num should be the
        number of pixels in the display, and pin should be the GPIO pin connected
        to the display signal line (must be a PWM pin like 18!).  Optional
        parameters are freq, the frequency of the display signal in hertz (default
        800khz), dma, the DMA channel to use (default 5), invert, a boolean
        specifying if the signal line should be inverted (default False), and
        channel, the PWM channel to use (defaults to 0).
        """
        # Create ws2811_t structure and fill in parameters.
        self._leds = ws.new_ws2811_t()
        self.brightness = brightness

        # Initialize the channels to zero
        for channum in range(2):
            chan = ws.ws2811_channel_get(self._leds, channum)
            ws.ws2811_channel_t_count_set(chan, 0)
            ws.ws2811_channel_t_gpionum_set(chan, 0)
            ws.ws2811_channel_t_invert_set(chan, 0)
            ws.ws2811_channel_t_brightness_set(chan, 0)

        # Initialize the channel in use
        self._channel = ws.ws2811_channel_get(self._leds, channel)
        ws.ws2811_channel_t_count_set(self._channel, num)
        ws.ws2811_channel_t_gpionum_set(self._channel, pin)
        ws.ws2811_channel_t_invert_set(self._channel, 0 if not invert else 1)
        ws.ws2811_channel_t_brightness_set(self._channel, brightness)
        ws.ws2811_channel_t_strip_type_set(self._channel, strip_type)

        # Initialize the controller
        ws.ws2811_t_freq_set(self._leds, freq_hz)
        ws.ws2811_t_dmanum_set(self._leds, dma)

        # Grab the led data array.
        self._led_data = _LED_Data(self._channel, num)

        # Substitute for __del__, traps an exit condition and cleans up properly
        atexit.register(self._cleanup)

    def __del__(self):
        # Required because Python will complain about memory leaks
        # However there's no guarantee that "ws" will even be set
        # when the __del__ method for this class is reached.
        if ws != None:
            self._cleanup()

    def _cleanup(self):
        # Clean up memory used by the library when not needed anymore.
        if self._leds is not None:
            ws.ws2811_fini(self._leds)
            ws.delete_ws2811_t(self._leds)
            self._leds = None
            self._channel = None
            # Note that ws2811_fini will free the memory used by led_data internally.

    def begin(self):
        """
        Initializes library, must be called once before other functions are called.

        Parameters
        ----------
        self : Function of class Adafruit_Neopixel

        Returns
        -------
        None
        """
        resp = ws.ws2811_init(self._leds)
        if resp != ws.WS2811_SUCCESS:
            message = ws.ws2811_get_return_t_str(resp)
            raise RuntimeError('ws2811_init failed with code {0} ({1})'.format(resp, message))

    def show(self):
        """
        Update the display with the data from the LED buffer.

        Parameters
        ----------
        self : Function of class Adafruit_Neopixel

        Returns
        -------
        None
        """
        resp = ws.ws2811_render(self._leds)
        if resp != ws.WS2811_SUCCESS:
            message = ws.ws2811_get_return_t_str(resp)
            raise RuntimeError('ws2811_render failed with code {0} ({1})'.format(resp, message))

    def set_pixel_color(self, pos, color):
        """
        Set LED at position pos to the provided 24-bit color value.

        Parameters
        ----------
        self : Function of class Adafruit_Neopixel

        pos : int
            The position of the LED on the neopixel that needs its color to be changed

        color : int
            A 24 bit color value that determines what the color will be changed to
        Returns
        -------
        None
        """
        self._led_data[pos] = color

    def set_brightness(self, brightness):
        """
        Scale each LED in the buffer by the provided brightness. A brightness
        of 0 is the darkest and 255 is the brightest.

        Parameters
        ----------
        self : Function of class Adafruit_Neopixel

        brightness : int
            The value to set the brightness of each LED between 0 (lowest) to 255 (highest)

        Returns
        -------
        None
        """
        ws.ws2811_channel_t_brightness_set(self._channel, brightness)

    def num_pixels(self):
        """
        Return the number of pixels in the display

        Parameters
        ----------
        self : Function of class Adafruit_Neopixel

        Returns
        -------
        int
            The number of pixels in in the neopixel ring
        """
        return ws.ws2811_channel_t_count_get(self._channel)

    ##Subset 1. Neopixel based gradient commands:
    def pulsate_neopixel(self, brightness, color):
        """
        Causes the neopixel to pulsate to a certain brightness

        Parameters
        ----------
        self : Function of class Adafruit_Neopixel

        brightness : int
            The value to set the brightness of each LED between 0 (lowest) to 255 (highest)

        color : int
            A 24 bit color value that determines what the color will be.

        Returns
        -------
        None
        """
        for i in range(self.num_pixels()):
            self.set_pixel_color(i, color)
            self.set_brightness(brightness)
            self.show()

    def pulsation(self, color):
        """
        Pulses the Neopixel in a light gradient

        Parameters
        ----------
        self : Function of class Adafruit_Neopixel

        color : int
            A 24 bit color value that determines what the color will be.

        Returns
        -------
        None
        """
        for _time in range(63):
            self.pulsate_neopixel(_time*4, color)
        for _time in range(63):
            negative_time = 63-_time
            self.pulsate_neopixel(negative_time*4, color)

    def color_gradient_rg(self, percentage):
        """
        Puts the Neopixel in a color gradient from red to green based on input percentage
        Red is the highest percentage and green is the lowest percentage.

        Parameters
        ----------
        self : Function of class Adafruit_Neopixel

        percentage : int (or float)
            The percentage to determine the redness of the neopixel ring 0 (lowest) to 100 (highest)

        Returns
        -------
        None
        """
        greeness = 64
        redness = 0
        greeness -= 0.64*percentage
        redness += 0.64*percentage
        if greeness < 0:
            greeness = 0
        if redness > 255:
            redness = 255
        for i in range(self.num_pixels()):
            self.set_pixel_color(i, color_value(int(redness), int(greeness), 0))
            self.show()

    ## instances adapted from functions from Tony DiCola's strandtest (in deprecated files)

    def rainbow_cycle(self, wait_ms=20, iterations=5):
        """
        Draw rainbow that uniformly distributes itself across all pixels.

        Parameters
        ----------
        self : Function of class Adafruit_Neopixel

        wait_ms=20 : int (or float)
            The wait time in miliseconds in between each iteration of rainbowcycle

        iterations : int
            The number of rainbow cycles made

        Returns
        -------
        None
        """
        for j in range(256*iterations):
            for i in range(self.num_pixels()):
                self.set_pixel_color(i, wheel((int(i * 256 / self.num_pixels()) + j) & 255))
            self.show()
            time.sleep(wait_ms/1000.0)

    def color_wipe(self, color, wait_ms=50, iterations=1):
        """
        Wipe color across display a pixel at a time.

        Parameters
        ----------
        self : Function of class Adafruit_Neopixel

        color : int
            Takes a 24 bit color value

        wait_ms=50: int (or float)
            The wait time in miliseconds in between each iteration of color_wipe

        iterations=1 int
            The number of times color_wipe will be executed

        Returns
        -------
        None
        """
        for __ in range(0, iterations):
            for i in range(self.num_pixels()):
                self.set_pixel_color(i, color)
                self.set_brightness(self.brightness)
                self.show()
                time.sleep(wait_ms/1000.0)

    def neopixel_startup(self, boot_col, ok_col, err_col):
        """
        Does a little boot sequence for the neopixel that does some color wipes as well as
        initiate the neopixel.

        Parameters
        ----------
        self : Function of class Adafruit_Neopixel

        boot_color : int
            Takes a 24 bit color value that wipes across the neopixel during startup

        ok_color : int
            Takes a 24 bit color value that wipes across the neopixel if startup goes well

        err_col : int
            Takes a 24 bit color value that wipes across the neopixel if startup has a problem

        Returns
        -------
        None
        """
        try:
            self.begin()
            self.set_brightness(self.brightness)
            self.rainbow_cycle(10, 1)
            time.sleep(0.5)
            self.color_wipe(boot_col, 10)
            time.sleep(1)
            self.color_wipe(ok_col, 10)
        except:
            self.color_wipe(err_col, 10)

    def neopixel_on(self):
        """
        Turns the neopixel brightness to max

        Parameters
        ----------
        self : Function of class Adafruit_Neopixel

        Returns
        -------
        None
        """
        for __ in range(self.num_pixels()):
            self.set_brightness(self.brightness)
            self.show()

    def neopixel_off(self):
        """
        Sets all neopixel brightness to 0 (off)

        Parameters
        ----------
        self : Function of class Adafruit_Neopixel

        Returns
        -------
        None
        """
        for __ in range(self.num_pixels()):
            self.set_brightness(0)
            self.show()

    def neopixel_shutdown(self, error_col):
        """
        Shuts down neopixel ring after a color wipe shutdown

        Parameters
        ----------
        self : Function of class Adafruit_Neopixel

        error_col : int
            Takes a 24 bit color value that wipes across the neopixel during shutdown

        Returns
        -------
        None
        """
        time.sleep(1)
        self.color_wipe(error_col, 100)
        time.sleep(2)
        self.rainbow_cycle(10, 1)
        time.sleep(1)
        self.neopixel_off()
