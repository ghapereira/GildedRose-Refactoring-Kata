# -*- coding: utf-8 -*-

from enum import Enum

class Constants(Enum):
    MAX_ITEM_QUALITY: int = 50
    BACKSTAGE_PASS_THRESHOLD_1: int = 10
    BACKSTAGE_PASS_THRESHOLD_2: int = 5
    CONJURED_PREFIX: str = "Conjured"
    DEFAULT_QUALITY_CHANGE: int = 1

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

        quality_to_update = self._handle_quality(item)
        item.quality += quality_to_update

        self._adjust_bounds(item)

        item.sell_in -= 1

    @staticmethod
    def _adjust_bounds(item: Item) -> None:
        if item.quality > Constants.MAX_ITEM_QUALITY.value:
            item.quality = Constants.MAX_ITEM_QUALITY.value

        if item.quality < 0:
            item.quality = 0

    def _handle_quality(self, item: Item) -> int:
        if item.name == ItemNames.BACKSTAGE_PASS.value:
            return self._calculate_backstage_quality_update(item)

        quality_to_update = self._calculate_quality_to_update(item)
        if self._expired_item(item):
            quality_to_update *= 2

        return quality_to_update

    def _calculate_backstage_quality_update(self, item: Item) -> int:
        if item.sell_in > Constants.BACKSTAGE_PASS_THRESHOLD_1.value:
            return Constants.DEFAULT_QUALITY_CHANGE.value

        if item.sell_in > Constants.BACKSTAGE_PASS_THRESHOLD_2.value:
            return 2 * Constants.DEFAULT_QUALITY_CHANGE.value

        if item.sell_in > 0:
            return 3 * Constants.DEFAULT_QUALITY_CHANGE.value

        return -item.quality

    def _calculate_quality_to_update(self, item: Item) -> int:
        if item.name == ItemNames.AGED_BRIE.value:
            return Constants.DEFAULT_QUALITY_CHANGE.value

        if self._is_conjured_item(item):
            return -2 * Constants.DEFAULT_QUALITY_CHANGE.value

        return -Constants.DEFAULT_QUALITY_CHANGE.value

    @staticmethod
    def _is_conjured_item(item) -> bool:
        return item.name.startswith(Constants.CONJURED_PREFIX.value)

    @staticmethod
    def _expired_item(item) -> bool:
        return item.sell_in <= 0
