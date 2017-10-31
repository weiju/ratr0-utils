from PIL import Image
import math


def chunks(l, n):
    for i in range(0, len(list(l)), n):
        yield l[i:i+n]


def color_to_plane_bits(color, depth):
    """returns the bits for a given pixel in a list, lowest to highest plane"""
    result = [0] * depth
    for bit in range(depth):
        if color & (1 << bit) != 0:
            result[bit] = 1
    return result


def extract_planes(im, depth, verbose):
    """check extract_planes(), seems to be wrong and lose data !!!"""
    imdata = im.getdata()
    width, height = im.size

    map_words_per_row = int(width / 16)
    if width % 16 > 0:
        map_words_per_row += 1

    if verbose:
        print('source image width: %d height: %d' % (width, height))
        print('bitmap words/row: %d'  % map_words_per_row)

    # create the converted planar data
    planes = [[0] * (map_words_per_row * height) for _ in range(depth)]
    #print(planes)
    for y in range(height):
        x = 0
        while x < width:
            # build a word for each plane
            for i in range(min(16, width - x)):
                # get the palette index for pixel (x + i, y)
                color = imdata[y * width + x + i]  # color index
                planebits = color_to_plane_bits(color, depth)
                # now we need to "or" the bits into the words in their respective planes
                wordidx = (x + i) / 16  # word number in current row
                pos = int(y * map_words_per_row + wordidx)  # list index in the plane
                for planeidx in range(depth):
                    if planebits[planeidx]:
                        planes[planeidx][pos] |= (1 << (15 - (x + i) % 16)) # 1 << ((x + i) % 16)
            x += 16
    #print(planes)
    return planes, map_words_per_row


def interleave_planes(planes, map_words_per_row):
    """transforms a set of bitplanes into a large array of 16-bit
    word rows. each representing a line of an image
    """
    # 1. for each plane generate a list of lists of <map_words_per_row>
    # values
    chunked = list([list(chunks(plane, map_words_per_row)) for plane in planes])
    #print(chunked)

    # 2. for each plane, add the rows one after another to the result list
    num_rows = len(chunked[0])
    result = []
    for i in range(num_rows):
        for chunk in chunked:
            result.append(chunk[i])
    return result
