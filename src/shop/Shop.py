import importlib
import pkgutil
import shop.items
from shop.items.abstractShopItem import abstractShopItem

class Shop:
    def __init__(self):
        self.items = self.load_items()

    def load_items(self):
        items = []
        package = shop.items  # Reference to the package

        # Iterate through modules in the package
        for finder, module_name, is_pkg in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
            module = importlib.import_module(module_name)

            # Iterate through attributes in the module
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and issubclass(attr, abstractShopItem) and attr is not abstractShopItem:
                    items.append(attr())

        return items
    

    def get_available_items_for_user(self, user):
        # TODO toon verschillende items afhankelijk van user (welke ze al hebben etc)
        return [item for item in self.items if item.is_available_for(user)] 
