from __future__ import absolute_import

import logging.handlers
import os

import cv2

from datas.models.Garden import Garden
from datas.repositories.PlayerRepository import PlayerRepository
from datas.repositories.FlowerRepository import FlowerRepository
from utils.img_utils import draw_text_onto_image, add_sub_image

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

COMMANDE_PLANTER_PLANTE = os.path.join(FOLDER_ABSOLUTE_PATH, "ressources", "images", "commands",
                                       "CommandePlanterPlante.png")
COMMANDE_APPRENDRE_A_JARDINER = os.path.join(FOLDER_ABSOLUTE_PATH, "ressources", "images", "commands",
                                             "CommandeApprendreAJardiner.png")
COMMANDE_VOIR_PROGRESSION = os.path.join(FOLDER_ABSOLUTE_PATH, "ressources", "images", "commands",
                                         "CommandeVoirProgression.png")
COMMANDE_ENTRETENIR_PLANTE = os.path.join(FOLDER_ABSOLUTE_PATH, "ressources", "images", "commands",
                                          "CommandeEntretenirPlante.png")
COMMANDE_VOIR_ETAT_PLANTE = os.path.join(FOLDER_ABSOLUTE_PATH, "ressources", "images", "commands",
                                         "CommandeVoirEtatPlante.png")
COMMANDE_PROGRESSION_PLANTE = os.path.join(FOLDER_ABSOLUTE_PATH, "ressources", "images", "commands",
                                           "CommandeProgressionPlante.png")
COMMANDE_PROGRESSION_JARDINIER = os.path.join(FOLDER_ABSOLUTE_PATH, "ressources", "images", "commands",
                                              "CommandeProgressionJardinier.png")
ACTION_CREUSER = os.path.join(FOLDER_ABSOLUTE_PATH, "ressources", "images", "actions", "ActionCreuser.png")
ACTION_PLACER_BULBE = os.path.join(FOLDER_ABSOLUTE_PATH, "ressources", "images", "actions", "ActionPlacerBulbe.png")
ACTION_REBOUCHER_TROU = os.path.join(FOLDER_ABSOLUTE_PATH, "ressources", "images", "actions", "ActionReboucherTrou.png")
ACTION_ARROSER_LE_BULBE = os.path.join(FOLDER_ABSOLUTE_PATH, "ressources", "images", "actions",
                                       "ActionArroserLeBulbe.png")
ACTION_BINER = os.path.join(FOLDER_ABSOLUTE_PATH, "ressources", "images", "actions", "ActionBiner.png")
FEEDBACKS_BON = os.path.join(FOLDER_ABSOLUTE_PATH, "ressources", "images", "feedbacks", "Bon.png")
FEEDBACKS_PAS_BON = os.path.join(FOLDER_ABSOLUTE_PATH, "ressources", "images", "feedbacks", "PasBon.png")
FEEDBACKS_PAS_COMPRIS = os.path.join(FOLDER_ABSOLUTE_PATH, "ressources", "images", "feedbacks", "PasCompris.png")
ETAT_PLANTE = os.path.join(FOLDER_ABSOLUTE_PATH, "ressources", "images", "EtatPlante.png")
DANCE = os.path.join(FOLDER_ABSOLUTE_PATH, "ressources", "videos", "karaoke", "dance.mp4")
KARAOKE_GANG_NAMSEUTAYIL = os.path.join(FOLDER_ABSOLUTE_PATH, "ressources", "videos", "karaoke",
                                        "karaoke_gang-namseutayil.mp4")
NIVEAU_DU_JARDINIER = os.path.join(FOLDER_ABSOLUTE_PATH, "ressources", "images", "NiveauDuJardinier.png")
PROCHAIN_NIVEAU_DU_JARDINIER = os.path.join(FOLDER_ABSOLUTE_PATH, "ressources", "images",
                                            "ProchainNiveauDuJardinier.png")
JARDINIER_RANG = os.path.join(FOLDER_ABSOLUTE_PATH, "ressources", "images", "rangs", "JardinierRang")
LISTE_DES_COMMANDES = os.path.join(FOLDER_ABSOLUTE_PATH, "ressources", "images", "ListeDesCommandes.png")
ETAPES_PLANTE = os.path.join(FOLDER_ABSOLUTE_PATH, "ressources", "images", "etapes", "Etape")
ANIMATIONS = os.path.join(FOLDER_ABSOLUTE_PATH, "ressources", "videos", "animations")


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
        self.py_video_mapping.show_image(0, "{}{}Plante.png".format(ETAPES_PLANTE, state))
        image_text1 = draw_text_onto_image(
            cv2.imread(ETAT_PLANTE), "{} C".format(garden.temperature), 230, 650, 3)
        image_text2 = draw_text_onto_image(image_text1, "{}%".format(garden.humidity), 745, 650, 3)
        animation_name = "{}_plant.mp4".format(garden.flower.mood)
        self.py_video_mapping.show_video_on_wallpaper(
            1, os.path.join(ANIMATIONS, animation_name),
            image_text2, 225, 10, 650, 1, True)
        next_state = state + 1 if state < 4 else state
        self.py_video_mapping.show_image(2, "{}{}Plante.png".format(ETAPES_PLANTE, next_state))

    def display_plant_progression(self, flower_repo: FlowerRepository):
        previous_mood_animation_name = "{}_plant.mp4".format(
            flower_repo.flower.saved_moods[len(flower_repo.flower.saved_moods) - 1])
        current_mood_animation_name = "{}_plant.mp4".format(
            flower_repo.flower.mood)
        self.py_video_mapping.show_video(0, os.path.join(ANIMATIONS, previous_mood_animation_name), True)
        self.py_video_mapping.show_image(1, flower_repo.mood_plot())
        self.py_video_mapping.show_video(2, os.path.join(ANIMATIONS, current_mood_animation_name), True)

    def display_gardener_progression(self, player_repo: PlayerRepository):
        rank_img_name = player_repo.player.level + 1
        print(rank_img_name)
        if rank_img_name > 5:
            rank_img_name = 5
        next_rank_img_name = player_repo.player.level + 2
        if next_rank_img_name > 5:
            next_rank_img_name = 5

        gardener_current_rank_image = add_sub_image(cv2.imread(NIVEAU_DU_JARDINIER),
                                                    cv2.imread("{}{}.png".format(JARDINIER_RANG, rank_img_name)), 200,
                                                    250)
        gardener_next_rank_image = add_sub_image(cv2.imread(PROCHAIN_NIVEAU_DU_JARDINIER),
                                                 cv2.imread("{}{}.png".format(JARDINIER_RANG, next_rank_img_name)), 200,
                                                 250)

        gardener_current_rank_with_level_image = draw_text_onto_image(gardener_current_rank_image,
                                                                      "{}".format(player_repo.player.level), 600, 500,
                                                                      10, (0, 0, 0), 20)
        gardener_next_rank_with_level_image = draw_text_onto_image(gardener_next_rank_image,
                                                                   "{}".format(player_repo.player.level + 1), 600, 500,
                                                                   10, (0, 0, 0), 20)

        self.py_video_mapping.show_image(0, gardener_current_rank_with_level_image)
        self.py_video_mapping.show_image(1, player_repo.xp_bar_draw())
        self.py_video_mapping.show_image(2, gardener_next_rank_with_level_image)

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
