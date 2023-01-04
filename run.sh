SERVER_PROJECT_LOCATION=/home/odroid/proxy

unzip_project() {
  rm -f -r appiumProxy
  mkdir appiumProxy
  unzip appiumProxy.zip -d ${SERVER_PROJECT_LOCATION}/appiumProxy
  rm -f appiumProxy.zip
}

install_venv() {
  source ${SERVER_PROJECT_LOCATION}/appiumProxy/venv/bin/activate
  pip3 install -r requirements.txt
}

cd ${SERVER_PROJECT_LOCATION}
unzip_project
cd appiumProxy
install_venv
python3 ${SERVER_PROJECT_LOCATION}/appiumProxy/main.py
