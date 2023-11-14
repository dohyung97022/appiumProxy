modify_sysctl() {
  sudo sed -i -e 's/#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/' /etc/sysctl.conf
  sudo sed -i -e 's/#net.ipv6.conf.all.forwarding=1/net.ipv6.conf.all.forwarding=1/' /etc/sysctl.conf
  sudo sysctl -p
}

install_3proxy() {
  sudo apt install git
  git clone https://github.com/z3apa3a/3proxy
  cd 3proxy
  sudo sed -i '1i #define ANONYMOUS 1' src/proxy.h
  sudo ln -s Makefile.Linux Makefile
  sudo make
  sudo make install
  sudo systemctl is-enabled 3proxy.service
  if grep -q "# custom routes" /etc/iproute2/rt_tables; then
    echo "route setting exists"
  else
    echo '# custom routes' | sudo tee -a /etc/iproute2/rt_tables
    echo '1 gw1' | sudo tee -a /etc/iproute2/rt_tables
  fi
}

modify_sysctl
install_3proxy