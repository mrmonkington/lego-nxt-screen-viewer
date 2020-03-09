from PIL import Image
import nxt.locator
import nxt.brick
from struct import unpack, pack
#from optparse import OptionParser
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, GLib, GObject
import sys

# Thoses are extracted from firmware sources.
DISPLAY_MODULE_ID = 0x000a0001
DISPLAY_SCREEN_OFFSET = 119
DISPLAY_WIDTH = 100
DISPLAY_HEIGHT = 64

# Read no more than 32 bytes per request.
IOM_CHUNK = 32

def screenshot (b):
    """Take a screenshot, return a PIL image."""
    # Read pixels.
    pixels = []
    for i in xrange (0, DISPLAY_WIDTH * DISPLAY_HEIGHT / 8, IOM_CHUNK):
        mod_id, n_bytes, contents = b.read_io_map (DISPLAY_MODULE_ID,
                DISPLAY_SCREEN_OFFSET + i, IOM_CHUNK)
        pixels += unpack ('32B', contents)
    # Transform to a PIL format.
    pilpixels = []
    bit = 1
    linebase = 0
    for y in xrange (0, DISPLAY_HEIGHT):
        for x in xrange (0, DISPLAY_WIDTH):
            if pixels[linebase + x] & bit:
                pilpixels.append (0)
            else:
                pilpixels.append (255)
        bit <<= 1
        # When 8 lines have been read, go on with the next byte line.
        if bit == (1 << 8):
            bit = 1
            linebase += DISPLAY_WIDTH
    # Return a PIL image.
    pilbuffer = pack ('%dB' % DISPLAY_WIDTH * DISPLAY_HEIGHT, *pilpixels)
    pilimage = Image.frombuffer ('L', (DISPLAY_WIDTH, DISPLAY_HEIGHT),
            pilbuffer, 'raw', 'L', 0, 1)
    pilimage = pilimage.convert(mode="RGB").resize((400, 256))
    return pilimage

def init_win():
    topgtkwindow = Gtk.Window( title = "Lego reader" )
    topgtkwindow.connect( "destroy", Gtk.main_quit )
    gtkimage = Gtk.Image()
    topgtkwindow.add( gtkimage )
    topgtkwindow.show_all()
    return gtkimage


def update_image( gtkimage, sock ):
    pillowimage = screenshot(sock)
    glibbytes = GLib.Bytes.new( pillowimage.tobytes() )
    gdkpixbuf = GdkPixbuf.Pixbuf.new_from_data(
        glibbytes.get_data(),
        GdkPixbuf.Colorspace.RGB,
        False,
        8,
        pillowimage.width,
        pillowimage.height,
        len( pillowimage.getbands() )*pillowimage.width,
        None,
        None
    )
    gtkimage.set_from_pixbuf( gdkpixbuf )
    return True

def init_sock():
    # Find the brick and take the screenshot.
    sock = nxt.locator.find_one_brick ()
    if not sock:
        #print("Can't open NXT", file=sys.stderr)
        print >> sys.stderr, "Can't open NXT"
        sys.exit(1)
    return sock

def init():
    sock = init_sock()
    gtkimage = init_win()
    GObject.timeout_add(250, update_image, gtkimage, sock)

if __name__ == "__main__":
    init()
    Gtk.main()

