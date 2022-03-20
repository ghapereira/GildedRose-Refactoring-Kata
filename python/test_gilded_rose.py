# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose


class GildedRoseTest(unittest.TestCase):
    def test_item_name_correctly_set(self):
        items = [Item("foo", 0, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("foo", items[0].name)

    def test_item_repr(self):
        items = [
            Item("spam", 1, 3),
            Item("eggs", 99, 100)
        ]

        self.assertEqual('spam, 1, 3', str(items[0]))
        self.assertEqual('eggs, 99, 100', str(items[1]))

    def test_one_day_decrease(self):
        items = [
            Item(name="spam", sell_in=1, quality=3),
            Item(name="eggs", sell_in=8, quality=4),
            Item(name="cheese", sell_in=10, quality=1)
        ]

        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].quality, 2)
        self.assertEqual(items[0].sell_in, 0)
        self.assertEqual(items[1].quality, 3)
        self.assertEqual(items[1].sell_in, 7)
        self.assertEqual(items[2].quality, 0)
        self.assertEqual(items[2].sell_in, 9)

    def test_two_day_decrease(self):
        items = [
            Item(name="spam", sell_in=1, quality=3),
            Item(name="eggs", sell_in=8, quality=4),
            Item(name="cheese", sell_in=10, quality=1)
        ]

        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        gilded_rose.update_quality()

        self.assertEqual(items[0].quality, 0)
        self.assertEqual(items[0].sell_in, -1)
        self.assertEqual(items[1].quality, 2)
        self.assertEqual(items[1].sell_in, 6)
        self.assertEqual(items[2].quality, 0)
        self.assertEqual(items[2].sell_in, 8)

    def test_quality_is_never_negative(self):
        items = [
            Item(name="foo", sell_in=1, quality=1)
        ]

        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].quality, 0)
        self.assertEqual(items[0].sell_in, 0)

        gilded_rose.update_quality()

        self.assertEqual(items[0].quality, 0)
        self.assertEqual(items[0].sell_in, -1)

    def test_sell_in_dates_consistent_after_negative(self):
        items = [
            Item(name="foo", sell_in=2, quality=2)
        ]

        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].quality, 1)
        self.assertEqual(items[0].sell_in, 1)

        gilded_rose.update_quality()

        self.assertEqual(items[0].quality, 0)
        self.assertEqual(items[0].sell_in, 0)

        gilded_rose.update_quality()

        self.assertEqual(items[0].quality, 0)
        self.assertEqual(items[0].sell_in, -1)

    def test_legendary_items_remain_unaltered(self):
        items = [
            Item(name="Sulfuras, Hand of Ragnaros", sell_in=1, quality=80)
        ]

        gilded_rose = GildedRose(items)
        for _ in range(100):
            gilded_rose.update_quality()

        self.assertEqual(items[0].sell_in, 1)
        self.assertEqual(items[0].quality, 80)

    def test_expired_items_have_quality_degrading_faster(self):
        items = [Item("foo", 1, 10)]
        gilded_rose = GildedRose(items)

        gilded_rose.update_quality()
        self.assertEqual(items[0].quality, 9)
        self.assertEqual(items[0].sell_in, 0)

        gilded_rose.update_quality()
        self.assertEqual(items[0].quality, 7)
        self.assertEqual(items[0].sell_in, -1)

        gilded_rose.update_quality()
        self.assertEqual(items[0].quality, 5)
        self.assertEqual(items[0].sell_in, -2)

    def test_regular_items_have_maximum_quality(self):
        items = [
            Item("Aged Brie", 10, 49),
            Item("Backstage passes to a TAFKAL80ETC concert", 10, 49)
        ]
        gilded_rose = GildedRose(items)

        gilded_rose.update_quality()
        self.assertEqual(items[0].quality, 50)
        self.assertEqual(items[0].sell_in, 9)
        self.assertEqual(items[1].quality, 50)
        self.assertEqual(items[1].sell_in, 9)

        gilded_rose.update_quality()
        self.assertEqual(items[0].quality, 50)
        self.assertEqual(items[0].sell_in, 8)
        self.assertEqual(items[1].quality, 50)
        self.assertEqual(items[1].sell_in, 8)

    def test_aged_brie_incresases_in_quality(self):
        items = [Item("Aged Brie", 2, 1)]
        gilded_rose = GildedRose(items)

        gilded_rose.update_quality()
        self.assertEqual(items[0].quality, 2)
        self.assertEqual(items[0].sell_in, 1)

        gilded_rose.update_quality()
        self.assertEqual(items[0].quality, 3)
        self.assertEqual(items[0].sell_in, 0)

        gilded_rose.update_quality()
        self.assertEqual(items[0].quality, 5)
        self.assertEqual(items[0].sell_in, -1)

        gilded_rose.update_quality()
        self.assertEqual(items[0].quality, 7)
        self.assertEqual(items[0].sell_in, -2)

    def backstage_passes_increases_in_quality_before_expiration_date(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 13, 1)]
        gilded_rose = GildedRose(items)

        gilded_rose.update_quality()
        self.assertEqual(items[0].quality, 14)
        self.assertEqual(items[0].sell_in, 12)

        gilded_rose.update_quality()
        self.assertEqual(items[0].quality, 15)
        self.assertEqual(items[0].sell_in, 11)

        gilded_rose.update_quality()
        self.assertEqual(items[0].quality, 17)
        self.assertEqual(items[0].sell_in, 10)

        for _ in range(4):
            gilded_rose.update_quality()

        self.assertEqual(items[0].quality, 25)
        self.assertEqual(items[0].sell_in, 6)

        for _ in range(5):
            gilded_rose.update_quality()

        self.assertEqual(items[0].quality, 40)
        self.assertEqual(items[0].sell_in, 0)

        gilded_rose.update_quality()
        self.assertEqual(items[0].quality, 0)
        self.assertEqual(items[0].sell_in, -1)

    def backstage_passes_quality_drops_to_zero_after_concert_date(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 0, 1)]
        gilded_rose = GildedRose(items)

        for _ in range(5):
            gilded_rose.update_quality()

        self.assertEqual(items[0].quality, 0)
        self.assertEqual(items[0].sell_in, -5)


if __name__ == '__main__':
    unittest.main()
