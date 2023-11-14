unzip_project() {
  rm -f -r appiumProxy
  mkdir appiumProxy
  unzip appiumProxy.zip -d $PWD/appiumProxy
  rm -f appiumProxy.zip
}

install_venv() {
  source venv/bin/activate
  pip3 install -r requirements.txt
}

cd $PWD/proxy
unzip_project
cd appiumProxy
install_venv
sudo apt-get -y install android-tools-adb
sudo python3 main.py
