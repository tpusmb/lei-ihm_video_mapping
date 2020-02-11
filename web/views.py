from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "Hello world", 200


@app.route('/test')
def test():
    return render_template('three.html'), 200


@app.route('/sendPoints', methods=['POST'])
def sendPoints():
    print(request.json)
    return "success", 200


if __name__ == "__main__":
    app.run()
