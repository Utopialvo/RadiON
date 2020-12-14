# RadiON

FM transmitter for raspberry pi. Works on all raspberry's ARMv8.

1) Connect wire (30-40 centimeters) to GPIO4 that make device work. 
2) Run start.py with argv[1] (start/stop/restart).
3) Move any method (wav/flac/aac/mp3/m4a/ogg/ac3/) files in /download to start. 
4) After playback files are moved to /tmp
5) Automatic backup (in /backup) with one time in hour.

Class for daemonizing is https://github.com/serverdensity/python-daemon

sudo apt-get install sox

git clone https://github.com/Utopialvo/RadiON

cd RadiON/

sudo chmod 777 *py 

sudo chmod 777 fm_tr

sudo ./start.py start
