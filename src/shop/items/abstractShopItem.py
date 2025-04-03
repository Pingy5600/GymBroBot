from abc import ABC, abstractmethod

class abstractShopItem(ABC):
    def __init__(self, name, emoji, description):
        self.name = name
        self.emoji = emoji
        self.description = description

    def __str__(self):
        return f"{self.emoji} **{self.name}** - {self.description}"
    
    @abstractmethod
    def is_available_for(self, user):
        return
    