from io import BytesIO
from PIL import Image
from django.core.files import File


#image compression method
def compress(image):
    im = Image.open(image)
    im_io = BytesIO()
    im.save(im_io, 'JPEG', optimize = True, quality=13) 
    new_image = File(im_io, name=image.name)
    return new_image


def small_compress(image):
    im = Image.open(image)
    im_io = BytesIO()
    im.save(im_io, 'JPEG', optimize = True, quality=60) 
    new_image = File(im_io, name=image.name)
    return new_image


#image compression method
def drastic_compress(image):
    im = Image.open(image)
    im_io = BytesIO()
    im.save(im_io, 'JPEG', optimize = True, quality=6) 
    new_image = File(im_io, name=image.name)
    return new_image