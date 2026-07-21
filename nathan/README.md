# Air-Pollution-Code
Note: thanks for reading me! :D

l/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\l

Kaggle Dataset for training model of which i already did (model is resnet18.onnx): https://www.kaggle.com/datasets/mokhammadparvanivafa/urban-images-of-air-pollution-in-kyrgyzstan?select=labels+-+metadata.csv.csv

l-/-\-/-\-/-\-/-\-/-\-/-\-/-\-/-\-/-\-/-\-/-\-/-\-l

My Project uses a camera (tested with webcam) to detect air pollution. It uses a formula where if it's above 75% confident it's polluted, it prints that the air is polluted and it's high pollution. It also allows you to see what the camera is seeing by using NoMachine to access the Orin NANO. Printing this could allow easier ways to detect air pollution, by allowing AI to do it by detecting the Image.

tldr: it finds pollution in air with nomachine and a camera if it's 75% confident

HOW TO RUN
Prerequisites: 
NoMachine (See later if not downloaded)
Orin NANO
Webcam
Dummy Plug
VS CODE
USB - USB-C plug
STEPS:
Plug in the orin to a webcam and also insert the dummy plug in
Plug in your Orin nano with it's Power plug.
Plug in the Orin to your Laptop or PC.
SSH into the Orin Via VS Code. (put its ip on it's box into the pairing thing to pair) 
press open folder and press ok
Put the Air-Pollution-Code Folder inside VS CODE.
(IF NOMACHINE NOT INSTALLED:
Power off the Orin. 
Plug the dummy plug into the Orin
Power On the Orin.
SSH back in
Run this in the terminal to Download NoMachine: wget https://www.nomachine.com/free/arm/v8/deb -O nomachine.deb
and then run this in the terminal to install: sudo dpkg -i nomachine.deb
(NOTE: SUDO asks for your password. it's the one you use to get into VS Code when you SSH IN.)
restart orin with this in the terminal: sudo reboot
make sure your orin is ssh'd in
Open NoMachine in your computer
click "Allow guest desktop sharing access on this server" on the first screen and click ok
on the machines area double click your orin
Enter username and Password (both are your password you use to ssh in)
create a virtual desktop
read tutorial and continue with ok
change display resolution to match the window
congrats
now close it)
open the live_pollution_detector.py and press run
wait until the language font warnings and open NoMachine.
press on your orin in NoMachine
you should see a view of the camera and percents that show the confidence in pollution, and check the terminal to see if the air is polluted because it prints it
press q to quit (if you want to)
7_/7_/7_/7_/7_/7_/7_/7_/7_/7_/7_/7_/7_/7_/7_/7_/7_/7

Have fun!

[text](live_pollution_detector.py)

READMEREADMEREADMEREADMEREADMEREADMEREADMEREADMEREADME
