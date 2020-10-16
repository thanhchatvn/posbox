#!/usr/bin/env bash

# init.sh
# this is POSBOX VERSION 17.x
sudo su
mount -o remount,rw / && cd /home/pi/odoo/addons
rm -rf hw_escpos && rm -rf hw_screen && cd ..
rm -rf 17.* && rm -rf posbox-*
wget https://github.com/thanhchatvn/posbox/archive/17.posbus.zip
unzip 17.posbus.zip && cd posbox-17.posbus
cp -R hw_escpos /home/pi/odoo/addons && cp -R hw_screen /home/pi/odoo/addons
cd /home/pi/odoo && chown pi.pi -R addons
sudo reboot now