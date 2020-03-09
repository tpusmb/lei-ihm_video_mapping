import json
import subprocess
import sys
from enum import Enum
from typing import Union, Tuple

import requests


class Intent(Enum):
    SALUTATION = "salutation"
    FIN = "fin"
    SUIVRE_ETAT_PLANTE = "suivre_etat_plante"
    AFFICHER_ETAT_PLANTE = "afficher_etat_plante"
    ENTRETENIR_PLANTE = "entretenir_plante"
    AFFICHER_PROGRES_PLANTE = "afficher_progres_de_la_plante"
    AFFICHER_PROGRES_DU_JARDINIER = "afficher_progres_du_jardinier"
    AFFICHER_COURBE_PROGRESSION = "afficher_courbe_progression"
    AFFICHER_NIVEAU = "afficher_niveau"
    PLANTER_UNE_NOUVELLE_PLANTE = "planter_une_nouvelle_plante"
    PLANTER_UN_BULBE = "planter_un_bulbe"
    POSITIF = "positif"
    NEGATIF = "negatif"
    PLANTE_CHALLENGE = "plante_challenge"
    UNKNOWN_INTENT = ""

    @staticmethod
    def from_str(intent_str: str) -> Union["Intent", None]:
        if not str:
            return
        intent_dict = Intent.__dict__.get("_member_map_")
        for _, intent in intent_dict.items():
            if intent.value == intent_str:
                return intent
        print(f"/!\\ MISSING INTENT /!\\ : <{intent_str}>", file=sys.stderr)
        return None


class RasaIntent:

    def __init__(self, url="http://localhost:5005/model/parse", headers=None):
        self.url = url
        self.headers = headers if headers else {}
        if isinstance(self.headers, str):
            self.headers = json.loads(headers)

    def detect_intent(self, text: str) -> Tuple[Union[Intent, None], float]:
        res = requests.post(
            self.url,
            json={"text": text},
            headers=self.headers,
        )
        intent_res = res.json().get("intent", [])
        intent_str = intent_res.get("name")
        confidence = intent_res.get('confidence')
        return Intent.from_str(intent_str), confidence


if __name__ == '__main__':
    rasa_intent = RasaIntent()
    msg = input("enter a message where an intent is to be detected ")
    while msg:
        print("intent detected: ", end='')
        print(rasa_intent.detect_intent(msg))
        print()
        msg = input("enter a message where an intent is to be detected, press enter to quit ")
