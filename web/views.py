from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "Hello world", 200


@app.route('/test')
def test():
    return render_template('simple.html'), 200


if __name__ == "__main__":
    app.run()
