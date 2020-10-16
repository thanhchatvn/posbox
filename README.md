# posbox
POSBOX Source Codes

============ TECHNICAL GUIDE INSTALL BASE ON POSBOX VERSION 17 =============
[ x ] POSBox image you can download from: https://nightly.odoo.com/master/posbox/posbox_image_v17.zip
[x] Open your terminal (linux, ubuntu terminal ...)
[x] ssh pi@[Your Ip Address of POSBOX]
[x] With Password: raspberry
[x] sudo su
[x] mount -o remount,rw / && cd /home/pi/odoo/addons
[x] rm -rf hw_escpos && rm -rf hw_screen && cd ..
[x] rm -rf 17.* && rm -rf posbox-*
wget https://github.com/thanhchatvn/posbox/archive/17.posbus.zip
unzip 17.posbus.zip && cd posbox-17.posbus
cp -R hw_escpos /home/pi/odoo/addons && cp -R hw_screen /home/pi/odoo/addons
cd /home/pi/odoo && chown pi.pi -R addons
sudo reboot now

============ Successfuly ==============
