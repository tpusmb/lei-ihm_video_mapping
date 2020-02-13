import sys
from enum import Enum
from typing import Union

import requests


class Intent(Enum):
    SALUTATION = "salutation"
    FIN = "fin"
    SUIVRE_ETAT_PLANTE = "suivre_etat_plante"
    AFFICHER_ETAT_PLANTE = "afficher_etat_plante"
    ENTRETENIR_PLANTE = "entretenir_plante"
    AFFICHER_PROGRES_DU_JARDINIER = "afficher_progres_du_jardinier"
    AFFICHER_COURBE_PROGRESSION = "afficher_courbe_progression"
    AFFICHER_NIVEAU = "afficher_niveau"
    PLANTER_UNE_NOUVELLE_PLANTE = "planter_une_nouvelle_plante"
    PLANTER_UN_BULBE = "planter_un_bulbe"
    POSITIF = "positif"
    NEGATIF = "negatif"
    PLANTE_CHALLENGE = "plante_challenge"

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

    def __init__(self, url="http://localhost:5005/model/parse"):
        self.url = url
        # TODO start server in background

    def detect_intent(self, text: str) -> Union[Intent, None]:  # TODO use intent enumeration
        res = requests.post(self.url, json={"text": text})
        intent_res = res.json().get("intent", [])
        intent_str = intent_res.get("name")
        confidence = intent_res.get('confidence')
        if intent_str and confidence < 0.5:
            print(f"Low intent score for text: <{text}>", file=sys.stderr)
            print(f"Confidence: {confidence}, for intent <{intent_str}> ", file=sys.stderr)
        return Intent.from_str(intent_str)


if __name__ == '__main__':
    rasa_intent = RasaIntent()
    msg = input("enter a message where an intent is to be detected ")
    while msg:
        print("intent detected: ", end='')
        print(rasa_intent.detect_intent(msg))
        print()
        msg = input("enter a message where an intent is to be detected, press enter to quit ")
