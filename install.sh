#!/bin/bash
sudo su
echo "mount disk"
mount -o remount,rw / && cd /home/pi/odoo/addons
echo "remove hw_escpos modules"
rm -rf hw_escpos && cd ..
rm -rf 21.04.* && rm -rf posbox-*
echo "cloning source"
wget https://github.com/thanhchatvn/posbox/archive/21.04.zip
unzip 21.04.zip && cd posbox-21.04
echo "replace old source"
cp -R hw_escpos /home/pi/odoo/addons
echo "grant permission new source"
cd /home/pi/odoo && chown pi.pi -R addons && cd /home/pi/odoo && chown pi.pi -R addons
echo "booting"
sudo reboot now