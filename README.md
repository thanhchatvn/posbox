#### Technical guide rebuild posbox 
    - POSBox image you can download from: https://nightly.odoo.com/master/posbox/posbox_image_v17.zip
    - Open your terminal (linux, ubuntu terminal ...)
    $      ssh pi@[Your Ip Address of POSBOX]
    - With Password: raspberry
    $      sudo su
    $      mount -o remount,rw / && cd /home/pi/odoo/addons
    $      rm -rf hw_escpos && rm -rf hw_screen && cd ..
    $      rm -rf 17.* && rm -rf posbox-*
    $      wget https://github.com/thanhchatvn/posbox/archive/17.zip --no-check-certificate
    $      unzip 17.zip && cd posbox-17
    $      cp -R hw_escpos /home/pi/odoo/addons && cp -R hw_screen /home/pi/odoo/addons
    $      cd /home/pi/odoo && chown pi.pi -R addons
    $      rm -rf 17.* && rm -rf posbox-*
    $      sudo reboot now
