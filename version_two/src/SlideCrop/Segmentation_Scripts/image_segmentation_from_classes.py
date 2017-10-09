import version_two.src.SlideCrop.ImarisImage as I
from version_two.src.SlideCrop.ImageSegmenter import ImageSegmenter as seg

FILE = "E:/testdata1/AT8 sc2231m 7~B.ims"
image = I.ImarisImage(FILE)

channelled_image = image.get_multichannel_segmentation_image()

segmentations = seg.segment_image(channelled_image)

for i in segmentations.segments:
    print(i)


