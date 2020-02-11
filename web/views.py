from flask import Flask, render_template, request
from utils import save_mapping

from py_video_mapping import PyVideoMapping, creat_monitor

app = Flask(__name__)

if len(PyVideoMapping.get_all_screens()) > 1:
    py_video_mapping = PyVideoMapping(PyVideoMapping.get_all_screens()[1])
    py_video_mapping.show_to_projector(py_video_mapping.wall_paper, blocking=False)
else:
    py_video_mapping = None


@app.route('/')
def ihm():
    return render_template('index.html', configs=save_mapping.load()), 200


@app.route('/test')
def test():
    return render_template('demo/three.html'), 200


@app.route('/sendPoints', methods=['POST'])
def send_points():
    print("update projector")
    data_json = request.json
    save_mapping.save(data_json)

    if py_video_mapping is not None:
        if py_video_mapping.screen_relation is None:
            py_video_mapping.change_ui_screen(creat_monitor(data_json["width"], data_json["heigth"]))
        py_video_mapping.mapping_calibration(data_json["points"])
    return "success", 200


if __name__ == "__main__":
    app.run()
