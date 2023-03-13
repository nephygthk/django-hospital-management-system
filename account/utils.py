from io import BytesIO
from PIL import Image
from django.core.files import File


#image compression method
def compress(image):
    im = Image.open(image)
    im_io = BytesIO() 
    im.save(im_io, 'JPEG', quality=30) 
    new_image = File(im_io, name=image.name)
    return new_image