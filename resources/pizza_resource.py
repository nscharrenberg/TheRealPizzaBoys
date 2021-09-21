from flask.json import jsonify


class pizza_resource:

    @staticmethod
    def all():
        return jsonify({
            "message": "Hello There"
        })
