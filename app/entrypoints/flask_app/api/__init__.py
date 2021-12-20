from dataclasses import dataclass

from flask import Blueprint, jsonify, request

from app.response_objects import ResponseFailure
from app.use_cases import hello

api = Blueprint("api", __name__)


@dataclass
class HelloRequestObject:
    name: str

    @classmethod
    def from_dict(cls, params):
        name = params.get("name")
        return cls(name=name)


@api.route("/hello")
def handle_hello():
    uc = hello.HelloUseCase()
    ro = HelloRequestObject.from_dict({"name": request.args.get("name", "Peter")})
    resp = uc.execute(ro)
    if not resp:
        if resp.type == ResponseFailure.RESOURCE_ERROR:
            return jsonify({"message": resp.message}), 404
        else:
            return jsonify({"message": resp.message}), 400

    return jsonify({"data": resp.value})
