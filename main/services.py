from PIL import Image, ImageDraw, ImageFilter
from django.conf import settings
from .models import PostFilesModel
from django.contrib import messages
from django.shortcuts import get_list_or_404
from moviepy.editor import *
import os


def _processingImage(file):
    fileName = str(file.file).split('/')[-1]

    with Image.open(file.file) as imageFile:
        img = Image.new('RGB', (1080, 1080), 'black')
        (width, height) = imageFile.size
        try:
            if width > height:
                new_width  = 1080
                new_height = int(new_width * height / width)
                imageFile = imageFile.resize((new_width, new_height), Image.ANTIALIAS)
                (width, height) = imageFile.size
                new_height = int((1080 - height)/2)
                img.paste(imageFile, (0, new_height))

                #top
                (left, upper, right, lower) = (0, new_height, new_width, new_height*2)
                im_crop = img.crop((left, upper, right, lower))
                blurred_image = im_crop.filter(ImageFilter.GaussianBlur(10))
                img.paste(blurred_image, (0, 0))

                #botton
                (left, upper, right, lower) = (0, 1080-new_height*2, new_width, 1080-new_height)
                im_crop = img.crop((left, upper, right, lower))
                blurred_image = im_crop.filter(ImageFilter.GaussianBlur(10))
                img.paste(blurred_image, (0, 1080-new_height))
                img.save(settings.MEDIA_ROOT + '/' + fileName)
                file.file = str(settings.MEDIA_ROOT + '/' + fileName)
                file.save()
            elif width < height:
                new_height = 1080
                new_width = int(new_height * width / height)
                imageFile = imageFile.resize((new_width, new_height), Image.ANTIALIAS)
                (width, height) = imageFile.size
                new_width = int((1080 - width)/2)
                img.paste(imageFile, (new_width, 0))

                #left
                (left, upper, right, lower) = (new_width, 0, new_width*2, 1080)
                im_crop = img.crop((left, upper, right, lower))
                blurred_image = im_crop.filter(ImageFilter.GaussianBlur(10))
                img.paste(blurred_image, (0, 0))

                #right
                (left, upper, right, lower) = (1080-new_width*2, 0, 1080-new_width, 1080)
                im_crop = img.crop((left, upper, right, lower))
                blurred_image = im_crop.filter(ImageFilter.GaussianBlur(10))
                img.paste(blurred_image, (1080-new_width, 0))
                img.save(settings.MEDIA_ROOT + '/' + fileName)
                file.file = str(settings.MEDIA_ROOT + '/' + fileName)
                file.save()
            elif width == height:
                pass
        except Exception as e:
            print(e)


def _processingVideo():
    pass


def processingImagesAndVideos(request, post_id):
    files = get_list_or_404(PostFilesModel, post_id=post_id)
    print(files)
    try:
        for file in files:
            if file.type == 'image':
                _processingImage(file)
            elif file.type == 'video':
                _processingVideo()
        messages.success(request, 'Your successfully add new post! Please reload this page! :)')
    except Exception as e:
        print(e)
        messages.error(request, 'Error! Please try again later!')
