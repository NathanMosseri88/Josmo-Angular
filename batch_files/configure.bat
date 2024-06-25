@echo off

pip3 install virtualenv

cd /d "C:\Users\%USERNAME%\Desktop\New Projects\Josmo\Josmo-Angular"
python -m virtualenv venv

cd venv/scripts
call activate.bat

cd /d "C:\Users\%USERNAME%\Desktop\New Projects\Josmo\Josmo-Angular"
pip3 install -r requirements.txt

cmd /k
