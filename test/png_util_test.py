#!/usr/bin/env python3

"""png_util_test.py
"""
import unittest
import xmlrunner
import png_util
import sys

class MockImage(object):
    """just a mock up to imitate a PIL image object"""

    def __init__(self, size, data):
        self.data = data
        self.size = size

    def getdata(self):
        return self.data


class PNGUtilTest(unittest.TestCase):  # pylint: disable-msg=R0904
    """Test class for png_util"""

    def test_chunks(self):
        """test the chunks() function"""
        self.assertEquals([[1], [2], [3]], list(png_util.chunks([1, 2, 3], 1)))
        self.assertEquals([[1, 2], [3, 4]], list(png_util.chunks([1, 2, 3, 4], 2)))

    def test_color_to_plane_bits_depth_0(self):
        """call color_to_plane_bits() with depth 0"""
        self.assertEquals([], png_util.color_to_plane_bits(0, 0))

    def test_color_to_plane_bits_depth_1(self):
        """call color_to_plane_bits() with depth 1"""
        self.assertEquals([0], png_util.color_to_plane_bits(0, 1))
        self.assertEquals([1], png_util.color_to_plane_bits(1, 1))

    def test_color_to_plane_bits_depth_2(self):
        """call color_to_plane_bits() with depth 2"""
        self.assertEquals([0, 0], png_util.color_to_plane_bits(0, 2))
        self.assertEquals([1, 0], png_util.color_to_plane_bits(1, 2))
        self.assertEquals([0, 1], png_util.color_to_plane_bits(2, 2))
        self.assertEquals([1, 1], png_util.color_to_plane_bits(3, 2))

    def test_extract_planes_0(self):
        """attempting to extract from an image with depth 0"""
        im = MockImage((2, 2), [1, 0, 0, 1])
        planes, map_words_per_row = png_util.extract_planes(im, 0, False)
        self.assertEquals([], planes)
        self.assertEquals(1, map_words_per_row)

    def test_extract_planes_1_2by2_all_0(self):
        """an image that has 2x2 pixels all set to 0"""
        im = MockImage((2, 2), [0, 0, 0, 0])
        planes, map_words_per_row = png_util.extract_planes(im, 1, False)
        self.assertEquals(1, map_words_per_row)
        self.assertEquals([[0, 0]], planes)

    def test_extract_planes_1_2by2_all_1(self):
        """an image that has 2x2 pixels all set to color 1"""
        im = MockImage((2, 2), [1, 1, 1, 1])
        planes, map_words_per_row = png_util.extract_planes(im, 1, False)
        self.assertEquals(1, map_words_per_row)
        row = 0b11 << (16 - 2)
        self.assertEquals([[row, row]], planes)

    def test_extract_planes_1_2by16_all_1(self):
        """an image that has 16x2 pixels all set to color 1"""
        im = MockImage((16, 2), [1] * 32)
        planes, map_words_per_row = png_util.extract_planes(im, 1, False)
        self.assertEquals(1, map_words_per_row)
        self.assertEquals([[65535, 65535]], planes)

    def test_extract_planes_1_2by32_all_1(self):
        """an image that has 16x2 pixels with each rows 16 pixels color 1 and
        16 pixels color 0"""
        im = MockImage((32, 2), ([1] * 16) + ([0] * 16) + ([1] * 16) + ([0] * 16))
        planes, map_words_per_row = png_util.extract_planes(im, 1, False)
        self.assertEquals(2, map_words_per_row)
        self.assertEquals([[65535, 0, 65535, 0]], planes)


if __name__ == '__main__':
    SUITE = []
    SUITE.append(unittest.TestLoader().loadTestsFromTestCase(PNGUtilTest))
    if len(sys.argv) > 1 and sys.argv[1] == 'xml':
      xmlrunner.XMLTestRunner(output='test-reports').run(unittest.TestSuite(SUITE))
    else:
      unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(SUITE))
