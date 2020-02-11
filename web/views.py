from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def ihm():
    return render_template('index.html'), 200


@app.route('/test')
def test():
    return render_template('demo/three.html'), 200


@app.route('/sendPoints', methods=['POST'])
def send_points():
    print(request.json)
    return "success", 200


if __name__ == "__main__":
    app.run()
