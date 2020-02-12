from py_video_mapping import *

py_video_mapping = PyVideoMapping(PyVideoMapping.get_all_screens()[1])
py_video_mapping.show_video(0, "ressources/videos/animations/angry_plant.mp4")
py_video_mapping.show_video(1, "ressources/videos/animations/angry_plant.mp4")
py_video_mapping.show_image(2, "ressources/images/actions/ActionArroserLeBulbe.png")
input("enter top stop")
py_video_mapping.stop()
