import threading

from pytesseract import pytesseract
from PIL import Image


class OCR:
    """
    OCR Engine modes (oem parameter):
      0    Legacy engine only.
      1    Neural nets LSTM engine only.
      2    Legacy + LSTM engines.
      3    Default, based on what is available.

    Page segmentation modes (psm parameter):
      0    Orientation and script detection (OSD) only.
      1    Automatic page segmentation with OSD.
      2    Automatic page segmentation, but no OSD, or OCR.
      3    Fully automatic page segmentation, but no OSD. (Default)
      4    Assume a single column of text of variable sizes.
      5    Assume a single uniform block of vertically aligned text.
      6    Assume a single uniform block of text.
      7    Treat the image as a single text line.
      8    Treat the image as a single word.
      9    Treat the image as a single word in a circle.
     10    Treat the image as a single character.
     11    Sparse text. Find as much text as possible in no particular order.
     12    Sparse text with OSD.
     13    Raw line. Treat the image as a single text line, bypassing hacks that are Tesseract-specific.
    """
    OEM_DEFAULT = 3
    PSM_DEFAULT = 6

    def __init__(self, oem=OEM_DEFAULT, psm=PSM_DEFAULT):
        """
        Args:
            oem: oem parameter (look at the beginning of the file)
            psm: psm parameter (Modes 6 and 7 work well, and for large blocks of text try 3, the default mode)
        """
        self.config = "--oem %s --psm %d -c tessedit_do_invert=0" % (oem, psm)
        self.results = {}
        self.lock = threading.RLock()

    @staticmethod
    def _transform_image(image):
        """
        override this method to apply image transformations in order to increase OCR accuracy.
        good starting point is cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1] but be sure to
            transform PIL images to numpy array first (np.array(image))
        """
        return image

    def _preprocess_images(self, images):
        return [self._transform_image(x) for x in images]

    def _get_extra_config(self, additional_configs, idx):
        new_config = self.config

        try:
            extra_config = additional_configs[idx]
            if extra_config is not None and len(extra_config):
                new_config = "%s -c '%s'" % (self.config, extra_config)
        except (IndexError, TypeError):
            pass

        return new_config

    def _save_result(self, k, v):
        self.lock.acquire()
        try:
            self.results[k] = v
        finally:
            self.lock.release()

    def _work(self, roi, idx, extra_config):
        text = pytesseract.image_to_string(roi, config=extra_config)
        text = text.strip()
        self._save_result(idx, text)

    def _order_results(self):
        ordered = []

        for idx in sorted(self.results.keys()):
            ordered.append(self.results[idx])

        self.results = {}
        return ordered

    def _run_ocr_ang_get_result(self, images, additional_configs):
        threads = []
        for idx, img in enumerate(images):
            extra_config = self._get_extra_config(additional_configs, idx)
            t = threading.Thread(target=self._work, args=(img, idx, extra_config))
            threads.append(t)

        [x.start() for x in threads]
        [x.join() for x in threads]

        return self._order_results()

    def ocr(self, images=None, additional_configs=None):
        """
        Args:
            images: list of numpy array RGB images or string image paths to run OCR on.
            additional_configs: list of configs and restrictions for each of the images given to the OCR.
                for instance: [None, 'tessedit_char_whitelist=0123456789'] will apply no restriction to the first but
                will only return numeric characters from the second image.
        Returns:
            list of OCR results in the same order as given input
        """
        if not isinstance(images, list) or len(images) == 0:
            print('Usage: ocr([img1, img2])')
            pass
        if isinstance(images[0], str):
            images = [Image.open(x) for x in images]

        additional_configs = additional_configs or []

        images = self._preprocess_images(images)
        return self._run_ocr_ang_get_result(images, additional_configs)
