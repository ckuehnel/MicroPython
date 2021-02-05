import time
import picodisplay as display 

width = display.get_width()
height = display.get_height()

display_buffer = bytearray(width * height * 2)  # 2-bytes per pixel (RGB565)
display.init(display_buffer)

display.set_backlight(1)


display.set_pen(0, 0, 0)    # black
display.clear()
display.set_pen(100, 100, 100) # white

#display.circle(100,100,10)
#display.pixel(10,10)
#display.pixel_span(20,20,200) // wagerechte Linie
#display.rectangle(10,10,width-10,height-10)
display.text('01234567890123456789\n',10,10, 0, 2)
display.text('01234567890123456789\n',10,24, 0, 2)
        
display.update()
