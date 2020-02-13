from __future__ import absolute_import
from py_video_mapping import *
import logging.handlers
import os

from screeninfo import Monitor

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/screen_relation.log",
                                                 when="midnight", backupCount=60)
STREAM_HDLR = logging.StreamHandler()
FORMATTER = logging.Formatter("%(asctime)s %(filename)s [%(levelname)s] %(message)s")
HDLR.setFormatter(FORMATTER)
STREAM_HDLR.setFormatter(FORMATTER)
PYTHON_LOGGER.addHandler(HDLR)
PYTHON_LOGGER.addHandler(STREAM_HDLR)
PYTHON_LOGGER.setLevel(logging.DEBUG)

# Absolute path to the folder location of this python file
FOLDER_ABSOLUTE_PATH = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))


class Scenario:

    def __init__(self, video_mapping):
        self.py_video_mapping = video_mapping

    # Menus
    def display_main_menu(self):
        self.py_video_mapping.show_image(0, "ressources/images/commands/CommandePlanterPlante.png")
        self.py_video_mapping.show_image(1, "ressources/images/commands/CommandeApprendreAJardiner.png")
        self.py_video_mapping.show_image(2, "ressources/images/commands/CommandeVoirProgression.png")

    def display_sub_menu1(self):
        self.py_video_mapping.show_image(0, "ressources/images/commands/CommandeEntretenirPlante.png")
        self.py_video_mapping.set_blackout(1, True)
        self.py_video_mapping.show_image(2, "ressources/images/commands/CommandeVoirEtatPlante.png")

    def display_sub_menu2(self):
        self.py_video_mapping.show_image(0, "ressources/images/commands/CommandeProgressionPlante.png")
        self.py_video_mapping.set_blackout(1, True)
        self.py_video_mapping.show_image(2, "ressources/images/commands/CommandeProgressionJardinier.png")

    # Actions
    def display_action_creuser(self):
        self.py_video_mapping.set_blackout(0, True)
        self.py_video_mapping.show_image(1, "ressources/images/actions/ActionCreuser.png")
        self.py_video_mapping.set_blackout(2, True)

    def display_action_placer_bulbe(self):
        self.py_video_mapping.set_blackout(0, True)
        self.py_video_mapping.show_image(1, "ressources/images/actions/ActionPlacerBulbe.png")
        self.py_video_mapping.set_blackout(2, True)

    def display_action_reboucher_trou(self):
        self.py_video_mapping.set_blackout(0, True)
        self.py_video_mapping.show_image(1, "ressources/images/actions/ActionReboucherTrou.png")
        self.py_video_mapping.set_blackout(2, True)

    def display_action_arroser(self):
        self.py_video_mapping.set_blackout(0, True)
        self.py_video_mapping.show_image(1, "ressources/images/actions/ActionArroserLeBulbe.png")
        self.py_video_mapping.set_blackout(2, True)

    # Feedbacks
    def display_good_feedback(self):
        self.py_video_mapping.show_image(0, "ressources/images/feedbacks/Bon.png")
        self.py_video_mapping.show_image(2, "ressources/images/feedbacks/Bon.png")

    def display_bad_feedback(self):
        self.py_video_mapping.show_image(0, "ressources/images/feedbacks/PasBon.png")
        self.py_video_mapping.show_image(2, "ressources/images/feedbacks/PasBon.png")

    def display_incomprehension_feedback(self):
        self.py_video_mapping.show_image(0, "ressources/images/feedbacks/PasCompris.png")
        self.py_video_mapping.show_image(2, "ressources/images/feedbacks/PasCompris.png")

    # Data
    def display_plant_state(self, state):
        self.py_video_mapping.show_image(0, "ressources/images/etapes/Etape{}Plante.png".format(state))
        # TODO rajouter la video par dessus l'image
        self.py_video_mapping.show_image(1, "ressources/images/EtatPlante.png")
        next_state = state + 1 if state < 4 else state
        self.py_video_mapping.show_image(2, "ressources/images/etapes/Etape{}Plante.png".format(next_state))

    def display_plant_progression(self, mood):
        self.py_video_mapping.show_video(0, "ressources/videos/animations/{}_plant.mp4".format(mood))
        # TODO faire le graphique
        self.py_video_mapping.show_image(1, "ressources/images/commands/CommandeProgressionPlante.png")
        self.py_video_mapping.show_video(2, "ressources/videos/animations/{}_plant.mp4".format(mood))

    def display_gardener_progression(self, level, exp):
        # TODO le level sur l'image 1 et 3 et rajouter la jauge d'xp sur l'image 2
        self.py_video_mapping.show_image(0, "ressources/images/commands/CommandeProgressionJardinier.png")
        self.py_video_mapping.show_image(1, "ressources/images/NiveauDuJardinier.png")
        self.py_video_mapping.show_image(2, "ressources/images/commands/CommandeProgressionJardinier.png")

    # Help
    def display_command_list(self):
        self.py_video_mapping.set_blackout(0, True)
        self.py_video_mapping.show_image(1, "ressources/images/ListeDesCommandes.png")
        self.py_video_mapping.set_blackout(2, True)

    # Karaoke
    def display_karaoke(self):
        self.py_video_mapping.show_video(0, "ressources/videos/karaoke/dance.mp4")
        self.py_video_mapping.show_video(1, "ressources/videos/karaoke/karaoke_gang-namseutayil.mp4")
        self.py_video_mapping.show_video(2, "ressources/videos/karaoke/dance.mp4")

    def stop_mapping(self):
        input("enter top stop")
        self.py_video_mapping.stop()

