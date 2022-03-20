# -*- coding: utf-8 -*-

from enum import Enum

class Constants(Enum):
    MAX_ITEM_QUALITY: int = 50
    BACKSTAGE_PASS_THRESHOLD: int = 10

class ItemNames(Enum):
    SULFURAS: str = "Sulfuras, Hand of Ragnaros"
    AGED_BRIE: str = "Aged Brie"
    BACKSTAGE_PASS: str = "Backstage passes to a TAFKAL80ETC concert"

class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
            return "%s, %s, %s" % (self.name, self.sell_in, self.quality)

class GildedRose:

    def __init__(self, items):
        self.items = items

    def update_quality(self) -> None:
        for item in self.items:
            self._update_item_quality(item)

    def _update_item_quality(self, item: Item) -> None:
        if item.name in {ItemNames.SULFURAS.value}:
            return

        item.sell_in -= 1

        self._handle_quality(item)

        self._handle_item_expiration(item)

    def _handle_quality(self, item: Item) -> None:
        if self._item_increases_in_value(item):
            if item.quality < Constants.MAX_ITEM_QUALITY.value:
                item.quality += 1

            self._handle_concert(item)

            return

        if item.quality > 0:
            item.quality -= 1

    def _handle_item_expiration(self, item: Item) -> None:
        if not self._expired_item(item):
            return

        if item.name == ItemNames.AGED_BRIE.value:
            if item.quality < Constants.MAX_ITEM_QUALITY.value:
                item.quality += 1
            return

        if item.name == ItemNames.BACKSTAGE_PASS.value:
            item.quality = 0
            return

        can_decrease_quality_further = item.quality > 0
        if can_decrease_quality_further:
            item.quality -= 1

    @staticmethod
    def _item_increases_in_value(item) -> bool:
        return item.name in {ItemNames.AGED_BRIE.value, ItemNames.BACKSTAGE_PASS.value}

    @staticmethod
    def _expired_item(item) -> bool:
        return item.sell_in < 0

    @staticmethod
    def _handle_concert(item) -> None:
        is_backstage_pass = item.name == ItemNames.BACKSTAGE_PASS.value
        is_under_pass_threshold = item.sell_in <= Constants.BACKSTAGE_PASS_THRESHOLD.value
        can_update_quality = item.quality < Constants.MAX_ITEM_QUALITY.value

        if is_backstage_pass and is_under_pass_threshold and can_update_quality:
            item.quality += 1
