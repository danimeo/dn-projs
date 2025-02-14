

sudo apt-get install -y libespeak-dev
sudo apt-get install -y pulseaudio
sudo apt-get install -y libpulse-ocaml-dev
sudo apt-get install -y libsndfile1-dev libpulse-dev libncurses5-dev libmp3lame-dev libespeak-dev
sudo apt-get install -y libespeak-dev libsndfile1-dev libpulse-dev libncurses5-dev libestools-dev festival-dev libvorbis-dev libmp3lame-dev libdotconf-dev texinfo
sudo apt install -y autoconf libtool 
sudo apt install -y libsndfile1-dev libespeak-ng-dev libpulse-dev texinfo libltdl-dev libmpg123-dev libsonic-dev libutfcpp-dev



wget http://sourceforge.net/projects/e-guidedog/files/Ekho/9.0/ekho-9.0.tar.xz
tar -xvf ekho-9.0.tar.xz
cd ekho-9.0
./configure --enable-speechd
make && make install

ekho "你好"

rm -f ekho-9.0.tar.xz

