# Retroflag Pi64 Scripts
These are scripts I use with my Raspberry Pi 5 installed in a Retroflag Pi64 case. It runs Batocera and can do almost everything a regular SBC handheld can, including run PortMaster and ports.

Copy the `RetroFlag` folder to the `share/` or `storage/` folder directly. The RetroFlag folder contains a script to handle the power and reset switches on the Pi64.

Copy the `custom.sh` file to `share/system/` or `storage/system/`. This is a startup script that runs the retroflag python script you just copied and also resets the usb drivers on startup in an attempt to re-bind controllers and prevent having to manually unplug and replug on boot.

## Getting the Pi5 on the network
In the event you have trouble booting up Batocera and using the ui to find and connect to your network, you can modify `system/batocera.conf`. Find the following lines:

```
# ------------ B - Network ------------ #

## Set system hostname, accessible via network share.
system.hostname=NAME_HERE
## Wi-Fi country code (00 for World), see https://wiki.batocera.org/wifi_ssid#i_can_t_see_my_ssid_in_the_list_but_i_can_see_my_neighbor_s
#wifi.country=FR
## Activate Wi-Fi (0,1)
wifi.enabled=1
## Wi-Fi SSID (string)
wifi.ssid=SSID_NAME_HERE
## Wi-Fi KEY (string)
## Escape your special chars (# ; $) with a backslash. eg. $ becomes \$
wifi.key=YOUR_KEY_HERE
```

Fill the uncommented parts in with your wifi information, save, and put your sdcard into your Pi5 and boot.

## Other Config Settings
These are some other config settings I have, in case they help you have a better experience:

```
splash.screen.enabled=0
splash.screen.sound=0
splash.screen.subtitle=0
```

```
system.power.switch=RETROFLAG
```