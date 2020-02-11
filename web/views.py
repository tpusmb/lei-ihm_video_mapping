from flask import Flask, render_template, request
from utils import save_mapping

app = Flask(__name__)


@app.route('/')
def ihm():
    return render_template('index.html', configs=save_mapping.load()), 200


@app.route('/test')
def test():
    return render_template('demo/three.html'), 200


@app.route('/sendPoints', methods=['POST'])
def send_points():
    data = request.json
    save_mapping.save(data)
    print(request.json)
    return "success", 200


if __name__ == "__main__":
    app.run()
