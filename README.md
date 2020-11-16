#### Technical guide rebuild posbox
    - Required 1 Raspi 4
    - POSBox image you can download from: https://nightly.odoo.com/master/posbox/posbox-image-latest.zip
    - Install Image just Download to SDCard of Raspi
    - Open your terminal (linux, ubuntu terminal ...)
    $      ssh pi@[Your Ip Address of POSBOX]
    - With Password: raspberry
    1. Step by step (copy line bellow and paste to terminal console)
    $      sudo su
    $      mount -o remount,rw / && cd /home/pi/odoo/addons
    $      rm -rf hw_escpos && rm -rf hw_drivers && cd ..
    $      rm -rf 20.06.* && rm -rf posbox-*
    $      wget https://github.com/thanhchatvn/posbox/archive/20.06.zip
    $      unzip 20.06.zip && cd posbox-20.06
    $      cp -R hw_escpos /home/pi/odoo/addons && cp -R hw_drivers /home/pi/odoo/addons
    $      cd /home/pi/odoo && chown pi.pi -R addons && cd /home/pi/odoo && chown pi.pi -R addons
    $      sudo reboot now
    2. Finished. Go to POS Config / Sync Between Session [ Active Sync Offline Mode ]
