from __future__ import absolute_import

from data_drawer import BarDraw
from datas.models.Flower import Flower
from datas.models.Garden import Garden
from py_video_mapping import draw_text_onto_image
import logging.handlers
import os
import cv2

from datas.repositories.PlayerRepository import PlayerRepository

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

COMMANDE_PLANTER_PLANTE = os.path.join(FOLDER_ABSOLUTE_PATH, "ressources/images/commands/CommandePlanterPlante.png")
COMMANDE_APPRENDRE_A_JARDINER = os.path.join(FOLDER_ABSOLUTE_PATH,
                                             "ressources/images/commands/CommandeApprendreAJardiner.png")
COMMANDE_VOIR_PROGRESSION = os.path.join(FOLDER_ABSOLUTE_PATH, "ressources/images/commands/CommandeVoirProgression.png")
COMMANDE_ENTRETENIR_PLANTE = os.path.join(FOLDER_ABSOLUTE_PATH,
                                          "ressources/images/commands/CommandeEntretenirPlante.png")
COMMANDE_VOIR_ETAT_PLANTE = os.path.join(FOLDER_ABSOLUTE_PATH, "ressources/images/commands/CommandeVoirEtatPlante.png")
COMMANDE_PROGRESSION_PLANTE = os.path.join(FOLDER_ABSOLUTE_PATH,
                                           "ressources/images/commands/CommandeProgressionPlante.png")
COMMANDE_PROGRESSION_JARDINIER = os.path.join(FOLDER_ABSOLUTE_PATH,
                                              "ressources/images/commands/CommandeProgressionJardinier.png")
ACTION_CREUSER = os.path.join(FOLDER_ABSOLUTE_PATH, "ressources/images/actions/ActionCreuser.png")
ACTION_PLACER_BULBE = os.path.join(FOLDER_ABSOLUTE_PATH, "ressources/images/actions/ActionPlacerBulbe.png")
ACTION_REBOUCHER_TROU = os.path.join(FOLDER_ABSOLUTE_PATH, "ressources/images/actions/ActionReboucherTrou.png")
ACTION_ARROSER_LE_BULBE = os.path.join(FOLDER_ABSOLUTE_PATH, "ressources/images/actions/ActionArroserLeBulbe.png")
ACTION_BINER = os.path.join(FOLDER_ABSOLUTE_PATH, "ressources/images/actions/ActionBiner.png")
FEEDBACKS_BON = os.path.join(FOLDER_ABSOLUTE_PATH, "ressources/images/feedbacks/Bon.png")
FEEDBACKS_PAS_BON = os.path.join(FOLDER_ABSOLUTE_PATH, "ressources/images/feedbacks/PasBon.png")
FEEDBACKS_PAS_COMPRIS = os.path.join(FOLDER_ABSOLUTE_PATH, "ressources/images/feedbacks/PasCompris.png")
ETAT_PLANTE = os.path.join(FOLDER_ABSOLUTE_PATH, "ressources/images/EtatPlante.png")
DANCE = os.path.join(FOLDER_ABSOLUTE_PATH, "ressources/videos/karaoke/dance.mp4")
KARAOKE_GANG_NAMSEUTAYIL = os.path.join(FOLDER_ABSOLUTE_PATH, "ressources/videos/karaoke/karaoke_gang-namseutayil.mp4")
LISTE_DES_COMMANDES = os.path.join(FOLDER_ABSOLUTE_PATH, "ressources/images/ListeDesCommandes.png")


class Scenario:

    def __init__(self, video_mapping):
        self.py_video_mapping = video_mapping

    # Menus
    def display_main_menu(self):
        self.py_video_mapping.show_image(0, COMMANDE_PLANTER_PLANTE)
        self.py_video_mapping.show_image(1, COMMANDE_APPRENDRE_A_JARDINER)
        self.py_video_mapping.show_image(2, COMMANDE_VOIR_PROGRESSION)

    def display_sub_menu1(self):
        self.py_video_mapping.show_image(0, COMMANDE_ENTRETENIR_PLANTE)
        self.py_video_mapping.set_blackout(1, True)
        self.py_video_mapping.show_image(2, COMMANDE_VOIR_ETAT_PLANTE)

    def display_sub_menu2(self):
        self.py_video_mapping.show_image(0, COMMANDE_PROGRESSION_PLANTE)
        self.py_video_mapping.set_blackout(1, True)
        self.py_video_mapping.show_image(2, COMMANDE_PROGRESSION_JARDINIER)

    # Actions
    def display_action_creuser(self):
        self.py_video_mapping.set_blackout(0, True)
        self.py_video_mapping.show_image(1, ACTION_CREUSER)
        self.py_video_mapping.set_blackout(2, True)

    def display_action_placer_bulbe(self):
        self.py_video_mapping.set_blackout(0, True)
        self.py_video_mapping.show_image(1, ACTION_PLACER_BULBE)
        self.py_video_mapping.set_blackout(2, True)

    def display_action_reboucher_trou(self):
        self.py_video_mapping.set_blackout(0, True)
        self.py_video_mapping.show_image(1, ACTION_REBOUCHER_TROU)
        self.py_video_mapping.set_blackout(2, True)

    def display_action_arroser(self):
        self.py_video_mapping.set_blackout(0, True)
        self.py_video_mapping.show_image(1, ACTION_ARROSER_LE_BULBE)
        self.py_video_mapping.set_blackout(2, True)

    def display_action_biner(self):
        self.py_video_mapping.set_blackout(0, True)
        self.py_video_mapping.show_image(1, ACTION_BINER)
        self.py_video_mapping.set_blackout(2, True)

    # Feedbacks
    def display_good_feedback(self):
        self.py_video_mapping.show_image(0, FEEDBACKS_BON)
        self.py_video_mapping.show_image(2, FEEDBACKS_BON)

    def display_bad_feedback(self):
        self.py_video_mapping.show_image(0, FEEDBACKS_PAS_BON)
        self.py_video_mapping.show_image(2, FEEDBACKS_PAS_BON)

    def display_incomprehension_feedback(self):
        self.py_video_mapping.show_image(0, FEEDBACKS_PAS_COMPRIS)
        self.py_video_mapping.show_image(2, FEEDBACKS_PAS_COMPRIS)

    # Data
    def display_plant_state(self, state: int, garden: Garden):
        """
        :param garden: The current garden
        :param state: Represent the growth of the plant (between 0 and 5)
        :return:
        """
        garden.refresh_data()
        self.py_video_mapping.show_image(0, "ressources/images/etapes/Etape{}Plante.png".format(state))
        image_text1 = draw_text_onto_image(
            cv2.imread(ETAT_PLANTE), "{} C".format(garden.temperature), 230, 650, 3)
        image_text2 = draw_text_onto_image(image_text1, "{}%".format(garden.humidity), 745, 650, 3)
        self.py_video_mapping.show_video_on_wallpaper(
            1, "ressources/videos/animations/{}_plant.mp4".format(garden.flower.mood.value),
            image_text2, 225, 10, 650, 1, True)
        next_state = state + 1 if state < 4 else state
        self.py_video_mapping.show_image(2, "ressources/images/etapes/Etape{}Plante.png".format(next_state))

    def display_plant_progression(self, flower: Flower):
        self.py_video_mapping.show_video(0, "ressources/videos/animations/{}_plant.mp4".format(flower.mood.value), True)
        # TODO faire le graphique
        self.py_video_mapping.show_image(1, COMMANDE_PROGRESSION_PLANTE)
        self.py_video_mapping.show_video(2, "ressources/videos/animations/{}_plant.mp4".format(flower.mood.value), True)

    def display_gardener_progression(self, player_repo: PlayerRepository):
        # TODO le level sur l'image 1 et 3 et rajouter la jauge d'xp sur l'image 2
        self.py_video_mapping.show_image(0, COMMANDE_PROGRESSION_JARDINIER)
        # self.py_video_mapping.show_image(1, "ressources/images/NiveauDuJardinier.png")
        nivel_gui = BarDraw("Demo")
        nivel_gui.start()
        nivel_gui.add_bar("_")
        nivel_gui.update_value("_", player_repo.xp_percent_to_next_level())
        self.py_video_mapping.show_image(1, nivel_gui.get_figure_cv2_image())
        self.py_video_mapping.show_image(2, COMMANDE_PROGRESSION_JARDINIER)

    # Help
    def display_command_list(self):
        self.py_video_mapping.set_blackout(0, True)
        self.py_video_mapping.show_image(1, LISTE_DES_COMMANDES)
        self.py_video_mapping.set_blackout(2, True)

    # Karaoke
    def display_karaoke(self):
        self.py_video_mapping.show_video(0, DANCE, False)
        self.py_video_mapping.show_video(1, KARAOKE_GANG_NAMSEUTAYIL, True)
        self.py_video_mapping.show_video(2, DANCE, False)

    def stop_mapping(self):
        input("enter top stop")
        self.py_video_mapping.stop()

    def blackout(self):
        self.py_video_mapping.set_blackout(0, True)
        self.py_video_mapping.set_blackout(1, True)
        self.py_video_mapping.set_blackout(2, True)
