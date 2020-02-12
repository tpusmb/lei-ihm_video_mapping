from py_video_mapping import *

py_video_mapping = PyVideoMapping(PyVideoMapping.get_all_screens()[1])
py_video_mapping.show_video(0, "dance.mp4")
py_video_mapping.show_video(1, "ressources/videos/karaoke/karaoke_gang-namseutayil.mp4")
py_video_mapping.show_video(2, "ressources/videos/karaoke/dance.mp4")
input("enter top stop")
py_video_mapping.stop()
