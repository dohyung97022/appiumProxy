from flask import make_response, jsonify
from src.utils.object import object_utils


# 통일용 응답
class ResponseEntity:

    @classmethod
    def build(cls, data=None, code: int = 200):
        return make_response(jsonify(object_utils.object_to_dict(data)), code)
