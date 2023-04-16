
from functools import wraps
from flask import make_response, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt




def student_required(refresh=False):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if refresh:
                verify_jwt_in_request(refresh=True)
                claims = get_jwt()
                if claims["auth_level"] == "student":
                    return fn(*args, **kwargs)
                else:
                    return make_response(jsonify({"msg": "UNAUTHORISED ACCESS"}), 401)
            else:
                verify_jwt_in_request()
                claims = get_jwt()
                if claims["auth_level"] == "student":
                    return fn(*args, **kwargs)
                else:
                    return make_response(jsonify({"msg": "UNAUTHORISED ACCESS"}), 401)

        return decorator

    return wrapper

def staff_required(refresh=False):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if refresh:
                verify_jwt_in_request(refresh=True)
                claims = get_jwt()
                if claims["auth_level"] == "staff":
                    return fn(*args, **kwargs)
                else:
                    return make_response(jsonify({"msg": "UNAUTHORISED ACCESS"}), 401)
            else:
                verify_jwt_in_request()
                claims = get_jwt()
                if claims["auth_level"] == "staff":
                    return fn(*args, **kwargs)
                else:
                    return make_response(jsonify({"msg": "UNAUTHORISED ACCESS"}), 401)

        return decorator

    return wrapper


def admin_required(refresh=False):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if refresh:
                verify_jwt_in_request(refresh=True)
                claims = get_jwt()
                if claims["auth_level"] == "admin":
                    return fn(*args, **kwargs)
                else:
                    return make_response(jsonify({"msg": "UNAUTHORISED ACCESS"}), 401)
            else:
                verify_jwt_in_request()
                claims = get_jwt()
                if claims["auth_level"] == "admin":
                    return fn(*args, **kwargs)
                else:
                    return make_response(jsonify({"msg": "UNAUTHORISED ACCESS"}), 401)

        return decorator

    return wrapper