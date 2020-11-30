#### Technical guide rebuild posbox
    - POSBox image you can download from: https://nightly.odoo.com/master/posbox/posbox-image-latest.zip
    - Open your terminal (linux, ubuntu terminal ...)
    $      ssh pi@{Your Ip Address of POSBOX}
    - With Password: raspberry
    1. Step by step
    $      sudo su
    $      mount -o remount,rw / && cd /home/pi/odoo/addons
    $      rm -rf hw_escpos && cd ..
    $      rm -rf 20.10.* && rm -rf posbox-*
    $      wget https://github.com/thanhchatvn/posbox/archive/20.10.zip
    $      unzip 20.10.zip && cd posbox-20.10
    $      cp -R hw_escpos /home/pi/odoo/addons
    $      cd /home/pi/odoo && chown pi.pi -R addons && cd /home/pi/odoo && chown pi.pi -R addons
    $      sudo reboot now
    2. Copy all lines of file install.sh and paste to terminal console of your raspi
