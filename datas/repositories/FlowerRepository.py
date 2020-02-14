from datas.models.Flower import Flower


class FlowerRepository:
    CHANGE_FLOWER_RANK_MINUTE = 5  # Minute

    def __init__(self, flower: Flower):
        self.flower = flower

    def change_rank(self):
        if not self.flower.is_last_rank():
            self.flower.rank += 1
