SERVER_USERNAME=odroid
SERVER_IP=192.168.35.139
SERVER_PROJECT_LOCATION=/home/odroid/proxy
SERVER_PASSWORD=password

activate_venv() {
  source ./venv/bin/activate
}

create_requirements_txt() {
  pip freeze >requirements.txt
}

delete_requirements_txt() {
  rm requirements.txt
}

deactivate_venv() {
  deactivate
}

ask_server_password() {
  echo "SERVER_PASSWORD:"
  read -s SERVER_PASSWORD
}

zip_file() {
  zip -r appiumProxy.zip .
}

delete_zip_file() {
  rm appiumProxy.zip
}

transfer_zip_file() {
  scp ${PWD}/appiumProxy.zip ${PWD}/run.sh ${SERVER_USERNAME}@${SERVER_IP}:${SERVER_PROJECT_LOCATION}
}

activate_venv
create_requirements_txt
deactivate_venv
zip_file
transfer_zip_file
delete_zip_file
delete_requirements_txt
ssh -t ${SERVER_USERNAME}@${SERVER_IP} "sudo ${SERVER_PROJECT_LOCATION}/run.sh"
