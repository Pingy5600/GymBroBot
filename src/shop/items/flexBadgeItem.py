from .abstractShopItem import abstractShopItem

class flexBadgeItem(abstractShopItem):
    def __init__(self):
        super().__init__("Flex badge", "💸", "Do you have too much money? Then this is the item for you!")

    def is_available_for(self, user):
        return True