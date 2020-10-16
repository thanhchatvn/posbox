#### Technical guide rebuild posbox 
    - POSBox image you can download from: https://nightly.odoo.com/master/posbox/posbox-image-latest.zip
    - Open your terminal (linux, ubuntu terminal ...)
    $      ssh pi@[Your Ip Address of POSBOX]
    - With Password: raspberry
    $      sudo su
    $      mount -o remount,rw / && cd /home/pi/odoo/addons
    $      rm -rf hw_escpos && cd ..
    $      rm -rf 20.06.* && rm -rf posbox-*
    $      wget https://github.com/thanhchatvn/posbox/archive/20.06.posbus.zip
    $      unzip 20.06.posbus.zip && cd posbox-20.06.posbus
    $      cp -R hw_escpos /home/pi/odoo/addons && cd /home/pi/odoo && chown pi.pi -R addons && cd /home/pi/odoo && chown pi.pi -R addons
    $      sudo reboot now