import os
import cv2
import json
import pytesseract
from matplotlib import pyplot as plt
from pdf2image import convert_from_path


def get_config():
    with open(os.path.join(os.path.dirname(__file__), 'config.json')) as config:
        return json.loads(config.read())


def clear_data():
    data_dirs = ["/celery/uploaded-files/", "/celery/temp/imgs"]

    for _dir in data_dirs:
        for _file in os.listdir(_dir):
            if _file.endswith(".pdf") or _file.endswith(".jpg"):
                os.remove(os.path.join(_dir, _file))


def check_temp_dir_path(config):
    if not os.path.exists(config["pdf_2_image_savepath"]):
        os.makedirs(config["pdf_2_image_savepath"])


def sort_ascendically(_dict):
    return {k: v for k, v in sorted(_dict.items(), key=lambda item: item[1], reverse=True)}


def convert_pdf_to_images(config, pdfid):
    pages = convert_from_path("/celery/uploaded-files/" +
                              pdfid + ".pdf", config['pdf_2_image_dpi'])

    os.makedirs("/celery/temp/imgs/" + pdfid + "/", exist_ok=True)

    for (idx, page) in enumerate(pages):
        image_name = "Page_" + str(idx) + ".jpg"
        page.save(config["pdf_2_image_savepath"] +
                  pdfid + "/" + image_name, "JPEG")


def get_marked_regions(img_path):

    im = cv2.imread(img_path)

    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    thresh = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 30)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    dilate = cv2.dilate(thresh, kernel, iterations=4)

    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    line_items_coordinates = []
    for c in cnts:
        area = cv2.contourArea(c)
        x, y, w, h = cv2.boundingRect(c)

        image = None

        if y >= 600 and x <= 1000:
            if area > 10000:
                image = cv2.rectangle(
                    im, (x, y), (2200, y+h), color=(255, 0, 255), thickness=3)
                line_items_coordinates.append([(x, y), (2200, y+h)])

        if y >= 2400 and x <= 2000:
            image = cv2.rectangle(im, (x, y), (2200, y+h),
                                  color=(255, 0, 255), thickness=3)
            line_items_coordinates.append([(x, y), (2200, y+h)])

    return image, line_items_coordinates


def recognize(pdfid):
    config = get_config()

    check_temp_dir_path(config)

    convert_pdf_to_images(config, pdfid)

    _text = {}

    pdfpages_folder = os.path.join(config["pdf_2_image_savepath"], pdfid)

    for (idx, filename) in enumerate(os.listdir(pdfpages_folder)):

        _imgfile = os.path.join(pdfpages_folder, filename)

        image, line_items_coordinates = get_marked_regions(_imgfile)

        original_image = cv2.imread(_imgfile)

        for line_items_coordinate in line_items_coordinates:
            c = line_items_coordinate

            img = original_image[c[0][1]:c[1][1], c[0][0]:c[1][0]]

            # plt.figure(figsize=(10, 10))
            # plt.imshow(img)
            # plt.show()

            ret, threshold = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)

            text = str(pytesseract.image_to_string(
                threshold, config='--psm 6'))

            _text[filename.split("_")[1].split('.')[0]] = text

    return sort_ascendically(_text)


if __name__ == "__main__":
    pdfid = input("PDF ID:")
    recognize(pdfid)
