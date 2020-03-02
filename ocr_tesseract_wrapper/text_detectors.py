from abc import abstractmethod

from ocr_tesseract_wrapper import OCR


class TextDetectorOCRConfigsAbs(OCR):
    """
    Naive because it assumes that every text is going to be located at the same spot every time.
    """
    prefix = 'tessedit_char_whitelist='
    num = '0123456789'
    space = ' '
    alpha_lower = 'abcdefghijklmnopqrstuvwxyz'
    alpha_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    configs_dict = {
        'num': prefix + num,
        'num_space': prefix + space + num,
        'alphanum_space': prefix + space + num + alpha_lower + alpha_upper,
    }

    def __init__(self, draw=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.draw = draw

    def _parse_configs(self, configs):
        return [self.configs_dict.get(x, '') for x in configs]

    def _get_rois_bounding_boxes(self, img, sticker_rois):
        if self.draw:
            from PIL import ImageDraw
            draw = ImageDraw.Draw(img)

        w, h = img.size

        roi_imgs = []
        for r in sticker_rois:
            start_y = max(0, int(r[0][1] * h))
            end_y = min(int(r[1][1] * h), h)
            start_x = max(0, int(r[0][0] * w))
            end_x = min(int(r[1][0] * w), w)
            rect = (start_x, start_y, end_x, end_y)

            roi_imgs.append(img.crop(rect))
            if self.draw:
                draw.rectangle(rect, outline=(255, 0, 0))

        return roi_imgs

    @abstractmethod
    def _get_rois(self):
        """
        :return: list of text positions as ratios relative to the image size where first tuple in each
            list element is left-upper x, y and second tuple is right-down x, y.
            for instance:
            [
                [(0.14, 0), (0.59, 0.18)]
            ]
        """
        raise NotImplementedError

    @abstractmethod
    def _get_configs(self):
        """
        :return:
            additional OCR configs for each of the ROI. Each list element is a key for self.configs_dict.
            for instance:
            [
                'alphanum_space'
            ]
        """
        raise NotImplementedError

    def _find_text(self, image):
        """
        :param image: Pillow image
        :return: tuple where first element is list of images for OCR and second is list of additional OCR configs
        """
        image_rois = self._get_rois_bounding_boxes(image, self._get_rois())
        configs = self._parse_configs(self._get_configs())

        return image_rois, configs

    def run_ocr(self, image):
        """
        :param image: Pillow image
        :return: dictionary containing at least order_name, position, dimensions and printed_at entries
        """
        images, configs = self._find_text(image)
        results = self.ocr(images, configs)

        return results
