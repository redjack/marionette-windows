# because we need wine >= 1.5
sudo add-apt-repository -y ppa:ubuntu-wine/ppa

# reqs.
sudo apt-get -y update
sudo apt-get --no-install-recommends -y install libgmp-dev
sudo apt-get --no-install-recommends -y install python-pip python-dev
sudo apt-get --no-install-recommends -y install git
sudo apt-get --no-install-recommends -y install m4
sudo apt-get --no-install-recommends -y install zip unzip
sudo apt-get --no-install-recommends -y install subversion
sudo apt-get --no-install-recommends -y install faketime
sudo apt-get --no-install-recommends -y install g++-mingw-w64 gcc-mingw-w64 mingw-w64
sudo apt-get --no-install-recommends -y install wine1.6
sudo apt-get --no-install-recommends -y install p7zip-full
