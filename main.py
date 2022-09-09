import base64
import json
from flask_cors import CORS

from flask import Flask, abort, render_template, Response

app = Flask(__name__)
CORS(app)


@app.route("/s/graph/<x>/<y>")
def graph(x, y):
    """Generates an SVG graph.

    Args:
        x (decimal): x axis, INT between -1 and 1
        y (decimal): y axis, INT between -1 and 1
    """
    x = float(x)
    y = float(y)
    y = y * -1

    if x < -1 or x > 1:
        abort(400)

    if y > 1 or y < -1:
        abort(400)

    BUFFER = 50
    HEIGHT = 600 - BUFFER
    WIDTH = 1000 - BUFFER

    ci = int(WIDTH * ((x + 1) / 2)) + BUFFER / 2
    tp = int(HEIGHT * ((y + 1) / 2)) + BUFFER / 2

    print(ci, tp, sep=", ")

    return Response(
        render_template("graph.svg", x_coordinate=ci, y_coordinate=tp),
        mimetype="image/svg+xml",
    )


@app.route("/s/share/<token>")
def share(token):
    """Generate an SEO compatible HTML page which redirects to the front-end.


    Args:
        token (str): A base64 encoded json object of the coordinates and person's nickname
    """

    # Decode token
    json_string = base64.b64decode(token)
    data = json.loads(json_string)

    ci = data["ci"]
    tp = data["tp"]

    image_url = f"https://www.politicstest.com/s/graph/{ci}/{tp}"

    return render_template(
        "share.html",
        image_url=image_url,
        nickname=data["nickname"],
        ci=data["ci"],
        tp=data["tp"],
        description=data["description"],
        url=f"https://www.politicstest.com/view/{token}",
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
