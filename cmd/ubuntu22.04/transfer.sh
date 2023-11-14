SERVER_USERNAME=ubuntu
SERVER_IP=192.168.35.45

activate_venv() {
  source ./venv/bin/activate
}

create_requirements_txt() {
  pip freeze > requirements.txt
}

delete_requirements_txt() {
  rm requirements.txt
}

deactivate_venv() {
  deactivate
}

zip_file() {
  zip -r appiumProxy.zip . -x "venv/lib/*" ".git/*" ".idea/*" ".private/*"
}

delete_zip_file() {
  rm appiumProxy.zip
}

transfer_zip_file() {
  server_ip=$1
  server_username=$2
  scp ${PWD}/appiumProxy.zip ${PWD}/cmd/ubuntu22.04/run.sh ${PWD}/cmd/ubuntu22.04/install.sh ${server_username}@${server_ip}:./proxy
}

activate_venv
create_requirements_txt
deactivate_venv
zip_file
transfer_zip_file ${SERVER_IP} ${SERVER_USERNAME}
delete_zip_file
delete_requirements_txt
ssh -t ${SERVER_USERNAME}@${SERVER_IP} "sudo ./proxy/run.sh"
