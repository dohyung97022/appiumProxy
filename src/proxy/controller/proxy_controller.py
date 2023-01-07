from __main__ import app

from src.flask.domain.response_entity import ResponseEntity
from src.proxy.service import proxy_service


@app.route("/api/proxy/port/<port>/reconnect/ip", methods=['POST'])
def post_proxy_port_reconnect_ip(port: str):
    return ResponseEntity.build(data=proxy_service.proxy_port_reconnect_ip(port))
