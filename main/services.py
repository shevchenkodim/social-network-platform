from PIL import Image, ImageDraw, ImageFilter
from django.conf import settings
from .models import PostFilesModel
from moviepy.editor import *
import os

def generate_gif_for_video(file_id):
    file = PostFilesModel.objects.get(id=file_id)
    name = file.file.url
    name = name.split("/")
    full_name = name[-1]
    name = full_name.split(".")
    name_gif = name[0]
    clip = (VideoFileClip(os.path.join(settings.BASE_DIR, 'media/posts/image', full_name)))
    clip.subclip((15.0),(18.0))
    clip.resize(0.5)
    clip.write_gif(os.path.join(settings.BASE_DIR, 'media/posts/gif/') +  name_gif +'.gif')

    # print(os.path.join(settings.BASE_DIR, 'media/posts/image', full_name))
    # print(os.path.exists(os.path.join(settings.BASE_DIR, 'media/posts/image', full_name)))
    # # gif = os.system('ffmpeg -ss 10 -t 15 -i ' + os.path.join(settings.BASE_DIR, 'media/posts/image', full_name) + ' -vf "fps=10,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 ' + os.path.join(settings.BASE_DIR, 'media/posts/image') +  name_gif +'.gif')
    file.video_gif =  name_gif +'.gif'
    file.save()
    return True

def image_processing(picture, new_file_name):
    try:
        img = Image.new('RGBA', (1080, 1080), 'black')
        img_to = Image.open(picture)
        (width, height) = img_to.size

        if width > height:
            new_width  = 1080
            new_height = int(new_width * height / width)
            img_to = img_to.resize((new_width, new_height), Image.ANTIALIAS)
            (width, height) = img_to.size
            new_height = int((1080 - height)/2)
            img.paste(img_to, (0, new_height))

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

            img.save(settings.MEDIA_ROOT + '/posts/image/' + str(new_file_name) + '.png')
            return str(settings.MEDIA_ROOT + '/posts/image/' + str(new_file_name) + '.png')
        else:
            new_height = 1080
            new_width = int(new_height * width / height)
            img_to = img_to.resize((new_width, new_height), Image.ANTIALIAS)
            (width, height) = img_to.size
            new_width = int((1080 - width)/2)
            img.paste(img_to, (new_width, 0))

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

            img.save(settings.MEDIA_ROOT + '/posts/image/' + str(new_file_name) + '.png')
            return str(settings.MEDIA_ROOT + '/posts/image/' + str(new_file_name) + '.png')
    except Exception as e:
        print(e)
        return False
