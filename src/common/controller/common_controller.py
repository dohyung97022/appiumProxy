from __main__ import app
from src.flask.domain.response_entity import ResponseEntity


@app.route("/test", methods=['GET'])
def get_test():
    return ResponseEntity.build(data={'test': 1})
