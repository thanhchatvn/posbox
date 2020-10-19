#!/bin/bash
sudo su
echo "mount disk"
mount -o remount,rw / && cd /home/pi/odoo/addons
echo "remove 2 modules"
rm -rf hw_escpos && rm -rf hw_drivers && cd ..
rm -rf 20.06.* && rm -rf posbox-*
echo "cloning source"
wget https://github.com/thanhchatvn/posbox/archive/20.06.zip
unzip 20.06.zip && cd posbox-20.06
echo "replace old source"
cp -R hw_escpos /home/pi/odoo/addons && cp -R hw_drivers /home/pi/odoo/addons
echo "grant permission new source"
cd /home/pi/odoo && chown pi.pi -R addons && cd /home/pi/odoo && chown pi.pi -R addons
echo "booting"
sudo reboot now