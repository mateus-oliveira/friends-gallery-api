import sys
import tempfile
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


def make_square(im, min_size=266, fill_color=(255, 255, 255, 0)):
    x, y = im.size
    size = max(min_size, x, y)
    new_im = Image.new('RGBA', (size, size), fill_color)
    new_im.paste(im, (int((size - x)/2), int((size - y)/2)))
    return new_im


def resize_and_crop_file(uploaded_image, multiplier=1):
    dimensions = [500, 200, 50]
    dimension = dimensions[multiplier-1]

    name = {1: '', 2: '_medium', 3: '_low'}

    img_temp = Image.open(uploaded_image)
    output_io_stream = BytesIO()
    img_temp = make_square(img_temp)

    img_temp_resized = img_temp.resize(
        (dimension, dimension), Image.ANTIALIAS
    )

    img_temp_resized.save(
        output_io_stream, format='png', quality=int(100/multiplier)
    )

    uploaded_image = InMemoryUploadedFile(
        output_io_stream,
        'FileField',
        f"{uploaded_image.name.split('.')[0]}{name[multiplier]}.png",
        'image/png',
        sys.getsizeof(output_io_stream), None
    )

    return uploaded_image


def get_temp_asset():
    image = Image.new(mode='RGB', size=(200, 200), color='blue')
    tmp_file = tempfile.NamedTemporaryFile(suffix='.png')
    image.save(tmp_file)
    tmp_file.seek(0)

    return tmp_file
