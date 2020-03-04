from flask import Flask, render_template, request
from utils import save_mapping

from py_video_mapping import PyVideoMapping, creat_monitor

app = Flask(__name__)
MAPPING_DATA = "mapping_data.map"

if len(PyVideoMapping.get_all_screens()) >= 1:
    py_video_mapping = PyVideoMapping(PyVideoMapping.get_all_screens()[-1])
else:
    print("No projector detected")
    py_video_mapping = None


@app.route('/')
def ihm():
    return render_template('index.html', configs=save_mapping.load(MAPPING_DATA)), 200


@app.route('/test')
def test():
    return render_template('demo/three.html'), 200


@app.route('/sendPoints', methods=['POST'])
def send_points():
    data_json = request.json
    save_mapping.save(data_json, MAPPING_DATA)

    if py_video_mapping is not None:
        if py_video_mapping.screen_relation is None:
            py_video_mapping.change_ui_screen(creat_monitor(data_json["width"], data_json["heigth"]))
        py_video_mapping.mapping_calibration(data_json["points"])

    return "success", 200
