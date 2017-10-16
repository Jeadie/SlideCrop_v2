import numpy as np

class ImageSegmentation(object):
    """
    Data Structure to hold box segments for images. Box segments are defined by two points: 
    upper-left & bottom-right.  
    """
    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.segments = []

    def add_segmentation(self, x1, y1, x2, y2):
        """
        Adds a segmentation array to the ImageSegmentation object
        :param x1, y1: upper-left point of the segment box
        :param x2, y2: bottom-right point of the segment box
        :return: null
        """
        if (any(value < 0 for value in [x1, y1, x2, y2]) | any(x > self.width for x in [x1, x2]) |
           any(y > self.height for y in [y1, y2]) | (x1 > x2) | (y1 > y2)):
            print(x1, y1, x2, y2)
            print(self.width, self.height)
            raise InvalidSegmentError()
        else:
            self.segments.append([x1, y1, x2, y2])

    def get_scaled_segments(self, width, height):
        """
        :param width: pixel width of image to be scaled to.
        :param height: pixel height of image to be scaled to. 
        :return: An array of segment boxes scaled to the dimensions width x height
        """

        # make into 2d Array
        matrix = np.array(self.segments)[:]

        #column multiplication of columns 0 & 2 by width/self.width
        matrix[:, [0, 2]] = np.multiply(matrix[:, [0,2]], (width/self.width))

        # same for y axis columns 1 & 3. Multiply by height/self.height
        matrix[:, [1, 3]] = np.multiply(matrix[:, [1,3]], (height/self.height))
        return matrix

    def get_relative_segments(self):
        """
        :return: An array of segment boxes without scaling.  0<= x, y <=1. 
        """
        return self.get_scaled_segments(1, 1)

    def get_max_segment(self):
        """
        :return: Returns the segment [x1, y1, x2, y2] with the largest area
        """
        max_segment = self.segments[0]
        max_area = self.segment_area(max_segment)

        for segment in self.segments:
            segment_area = self.segment_area(segment)
            if segment_area > max_area:
                max_segment = segment
                max_area = segment_area

        return max_segment


    def segment_area(self, segment):
        """
        :param segment: Bounding box of form [x1, y1, x2, y2] 
        :return: area of bounding box
        """
        return (segment[0] - segment[2]) * (segment[1] - segment[3])

    def change_segment_bounds(self, factor):
        """
        :param factor: a float value dictating the change in bounding box size. 
        :return: an ImageSegmentation object with bounding boxes increased/decreased by the given factor
        """
        new_image_segmentation = ImageSegmentation(self.width, self.height)
        for bounding_box in self.segments:
            centre_point = [(bounding_box[0] + bounding_box[2])/2, (bounding_box[1] + bounding_box[3])/2]
            half_dimensions = [(bounding_box[2] - bounding_box[0])/2, (bounding_box[3] - bounding_box[1])/2]
            new_image_segmentation.add_segmentation(centre_point[0] - factor * half_dimensions[0],
                                                    centre_point[1] - factor * half_dimensions[1],
                                                    centre_point[0] + factor * half_dimensions[0],
                                                    centre_point[1] + factor * half_dimensions[1]
                                                    )

        return new_image_segmentation


class InvalidSegmentError(Exception):
    pass