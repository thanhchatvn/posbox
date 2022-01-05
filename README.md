#### Technical guide rebuild posbox
    - POSBox image you can download from: https://nightly.odoo.com/master/posbox/posbox-image-latest.zip
    - Open your terminal (linux, ubuntu terminal ...)
    $      ssh pi@{Your Ip Address of POSBOX}
    - With Password: raspberry
    1. Step by step
    $      sudo su
    $      mount -o remount,rw / && cd /home/pi/odoo/addons
    $      rm -rf hw_escpos && cd ..
    $      rm -rf 21.04.* && rm -rf posbox-*
    $      wget https://github.com/thanhchatvn/posbox/archive/21.04.zip --no-check-certificate
    $      unzip 21.04.zip && cd posbox-21.04
    $      cp -R hw_escpos /home/pi/odoo/addons
    $      cd /home/pi/odoo && chown pi.pi -R addons && cd /home/pi/odoo && chown pi.pi -R addons
    $      sudo reboot now
    2. Copy all lines of file install.sh and paste to terminal console of your raspi

vim /home/pi/odoo/addons/point_of_sale/tools/posbox/configuration/odoo.conf
change log_level = error to info

sudo su
mount -o remount,rw /
cd /home/pi/odoo/addons && rm -rf hw_escpos && cd .. && rm -rf 21.04.* && rm -rf posbox-*
wget https://github.com/thanhchatvn/posbox/archive/21.04.zip --no-check-certificate && unzip 21.04.zip && cd posbox-21.04
cp -R hw_escpos /home/pi/odoo/addons && cd /home/pi/odoo && chown pi.pi -R addons && cd /home/pi/odoo && chown pi.pi -R addons && sudo reboot now

