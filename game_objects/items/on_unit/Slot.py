from __future__ import annotations
from game_objects.items import Item
from typing import TYPE_CHECKING
from mechanics.events import ItemDroppedEvent
if TYPE_CHECKING:
    from game_objects.battlefield_objects import Unit
    from game_objects.items import ItemTypes


class Slot:
    def __init__(self, name:str, item_type : ItemTypes = None, owner: Unit = None):
        self.name = name
        self.item_type = item_type
        self.owner = owner
        self._content = None

    @property
    def content(self) -> Item:
        return self._content

    @content.setter
    def content(self, item):
        if item:
            assert isinstance(item, Item)
            if self.item_type:
                assert item.item_type is self.item_type
        if self.content:
            raise Exception("Remove existing item first.")

        self._content = item
        item.slot = self
        item.owner = self.owner

        if self.owner:
            try:
                item.game = self.owner.game
                if hasattr(item, "on_equip"):
                    item.on_equip(self)
            except AttributeError:
                pass

    def drop(self):
        if self.content:
            item = self.pop_item()
            ItemDroppedEvent(item)


    def swap_item(self, other_slot):
        self._content, other_slot._content = other_slot.pop_item(), self.pop_item()

    def pop_item(self):
        if self.content is None:
            return

        item = self.content
        self._content = None
        if self.owner:
            if hasattr(item, "on_unequip"):
                item.on_unequip(self)
            self.owner.recalc()
        item.owner = None
        return item



    def __repr__(self):
        return f"{self.owner}'s {self.name} slot with {self.content}"


