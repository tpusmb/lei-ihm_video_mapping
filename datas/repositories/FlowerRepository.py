from datas.models.Flower import Flower


class FlowerRepository:
    """
    Manage the flower
    """
    CHANGE_FLOWER_RANK_MINUTE = 5  # Minute

    def __init__(self, flower: Flower):
        self.flower = flower

    def change_rank(self):
        """
        Increment the rank of the plant, simply when the limit has not been reached
        """
        if not self.flower.is_last_rank():
            self.flower.rank += 1
