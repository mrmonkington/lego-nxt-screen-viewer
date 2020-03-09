# NXT Screen Mirror for Linux

This is a simple way to mirror the screen on an old Lego mindstorms NXT brick - ideal if the screen on yours is broken (very common as these things are ancient now!)

![image](https://user-images.githubusercontent.com/778856/76262590-a9934f80-6254-11ea-8358-8dccfda6ff05.png)

Updates @ 4fps.

Unfortunately uses Python2 due to `python-nxt` not having a stable Python 3 port.

## Quickstart

On Ubuntu 18.04 (LTS), use python2.7 due to lack of python3 port of `python-nxt`:

```
sudo apt install python2.7 python-gi python-nxt python-pil
python main.py
```

If libnxt can't see or connect to your NXT brick, even though you can see udev pick it up in your syslog, e.g.: 

```
[56021.604291] usb 1-1.1: New USB device found, idVendor=0694, idProduct=0002
```

Then try unloading your `cdc_acm` kernel module (which implements an abstract serial emulation over USB that I *think* `libnxt` would rather handle itself):

```
sudo rmmod cdc_acm
```

## Credits:

Thanks to Nicolas Schodet for the sample code to get the NXT screen: http://ni.fr.eu.org/lego/nxt_screenshot/



