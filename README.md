# RadiON

FM transmitter for raspberry pi. Works on all raspberry's ARMv8.

1) Connect wire (30-40 centimeters) to GPIO4 that make device work. 
2) Run start.py with argv[1] (start/stop/restart).
3) Move any method audio files in /download to start.
This script audio formats support: flac,mp2,mp3,ogg,wav. For other audio formats please use another converter before move file to /download.
4) After playback files are moved to /tmp
5) Automatic backup (in /backup) with one time in hour.

Class for daemonizing is https://github.com/serverdensity/python-daemon

sudo apt-get update && sudo apt-get install sox libsox-fmt-all

git clone https://github.com/Utopialvo/RadiON

cd RadiON/

sudo chmod 777 *py 

sudo chmod 777 fm_tr

sudo ./start.py start
