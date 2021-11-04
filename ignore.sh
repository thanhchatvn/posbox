git config --global core.excludesfile ignore.txt
find . -name "*.pyc" -exec rm -f {} \;
find . -name "*.DS_Store" -exec rm -f {} \;
find . -path "*/__pycache__" -type d -exec rm -r {} ';'
find . -path "*/__MACOSX" -type d -exec rm -r {} ';'
git config --global user.email "thanhchatvn@gmail.com"
git config --global user.name "Bruce Nguyen"

