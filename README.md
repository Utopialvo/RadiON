# RadiON

FM transmitter for raspberry pi. Works on all raspberry's.

1) Connect wire (30-40 centimeters) to GPIO4 that make device work. 
2) Run start.py to create catalog system.
3) Move any method you prefer (wav/flac/aac/mp3/m4a/ogg/ac3/) files in download/ to start. 
4) After playback files are moved to tmp/
5) Automatic backup (in backup/) with one time per hour.



git clone https://github.com/Utopialvo/RadiON

cd RadiON/

sudo chmod 777 *py 

sudo chmod 777 fm_tr

sudo ./start.py
