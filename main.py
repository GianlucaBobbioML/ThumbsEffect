import PIL
from PIL import Image, ImageFilter, ImageEnhance
name = 't8.webp'
img = Image.open(name)
height = int(img.size[1])
width = int(img.size[0])

def mostFreqColor(img_attr):
    pixels = img_attr.getcolors(500)
    most_frequent_pixel = pixels[0]
    for count, colour in pixels:
        if count > most_frequent_pixel[0]:
            most_frequent_pixel = (count, colour)
    return most_frequent_pixel[1]

def useMostFreqColor():
    global img
    global height
    global width
    global name
    if(width != height):
        if(width > height):
            neededH = (width - height)/2

            new_im1crop = img.crop((0, 0, width, 1))
            new_im1crop = new_im1crop.resize((width, neededH), PIL.Image.BICUBIC)
            new_im1 = Image.new('RGB', (width,neededH), color=mostFreqColor(new_im1crop))

            new_im2crop = img.crop((0, height - 1, width, height))
            new_im2crop = new_im2crop.resize((width, neededH), PIL.Image.BICUBIC)
            new_im2 = Image.new('RGB', (width,neededH), color=mostFreqColor(new_im2crop))

            finalImg = Image.new('RGB', (width,width))
            finalImg.paste(new_im1, (0,0))
            finalImg.paste(img, (0,neededH))
            finalImg.paste(new_im2, (0,neededH + height))
            finalImg.save(name+'-freq.jpg')
        else:
            neededW = (height - width)/2

            new_im1crop = img.crop((0, 0, 1, height))
            new_im1crop = new_im1crop.resize((neededW, height), PIL.Image.BICUBIC)
            new_im1 = Image.new('RGB', (neededW,height), color=mostFreqColor(new_im1crop))

            new_im2crop = img.crop((width - 1, 0, width, height))
            new_im2crop = new_im2crop.resize((neededW, height), PIL.Image.BICUBIC)
            new_im2 = Image.new('RGB', (neededW,height), color=mostFreqColor(new_im2crop))

            finalImg = Image.new('RGB', (height,height))
            finalImg.paste(new_im1, (0,0))
            finalImg.paste(img, (neededW,0))
            finalImg.paste(new_im2, (neededW + width, 0))
            finalImg.save(name+'-freq.jpg')

def useStrech():
    global img
    global height
    global width
    global name
    if(width != height):
        if(width > height):
            neededH = (width - height)/2

            new_im1 = img.crop((0, 0, width, 20))
            new_im1 = new_im1.resize((width, neededH + 20), PIL.Image.ANTIALIAS).filter(ImageFilter.GaussianBlur(10))

            new_im2 = img.crop((0, height - 20, width, height))
            new_im2 = new_im2.resize((width, neededH + 20), PIL.Image.ANTIALIAS).filter(ImageFilter.GaussianBlur(10))

            finalImg = Image.new('RGB', (width,width))
            finalImg.paste(new_im1, (0,0))
            finalImg.paste(img, (0,neededH))
            finalImg.paste(new_im2, (0,neededH + height - 20))
            finalImg.save(name+'-strech.jpg')
        else:
            neededW = (height - width)/2

            new_im1 = img.crop((0, 0, 20, height))
            new_im1 = new_im1.resize((neededW + 20, height), PIL.Image.ANTIALIAS).filter(ImageFilter.GaussianBlur(10))

            new_im2 = img.crop((width - 20, 0, width, height))
            new_im2 = new_im2.resize((neededW + 20, height), PIL.Image.ANTIALIAS).filter(ImageFilter.GaussianBlur(10))

            finalImg = Image.new('RGB', (height,height))
            finalImg.paste(new_im1, (0,0))
            finalImg.paste(img, (neededW,0))
            finalImg.paste(new_im2, (neededW + width - 20, 0))
            finalImg.save(name+'-strech.jpg')

def useBlurred():
    global img
    global height
    global width
    global name
    if(width != height):
        if(width > height):
            needed = width
        else:
            needed = height
        blurredImg = img.resize((needed, needed), PIL.Image.NEAREST).filter(ImageFilter.GaussianBlur(30))
        brightness = ImageEnhance.Brightness(blurredImg)
        blurredImg = brightness.enhance(1.6)
        if(width > height):
            blurredImg.paste(img, (0,(width - height)/ 2))
        else:
            blurredImg.paste(img, ((height - width)/ 2,0))
        blurredImg.save(name+'-blur.jpg')

def useBlurredAndResized():
    global img
    global height
    global width
    global name
    if(width != height):
        if(width > height):
            needed = width
        else:
            needed = height
        blurredImg = img.resize((needed, needed), PIL.Image.NEAREST).filter(ImageFilter.GaussianBlur(30))
        contrastness = ImageEnhance.Contrast(blurredImg)
        blurredImg = contrastness.enhance(0.6)
        brightness = ImageEnhance.Brightness(blurredImg)
        blurredImg = brightness.enhance(1.6)
        if(width > height):
            relationAspect = float(height)/width
            if(relationAspect < 0.7):
                neededH = int(width * 0.7)
                neededW = int(width * (float(neededH) / height))
                img = img.resize((neededW, neededH), PIL.Image.NEAREST)
                blurredImg.paste(img, (-(neededW - width)/ 2, (width - neededH)/ 2))
            else:
                blurredImg.paste(img, (0, (width - height)/ 2))
        else:
            relationAspect = float(width)/height
            if(relationAspect < 0.7):
                neededW = int(height * 0.7)
                neededH = int(height * (float(neededW) / width))
                img = img.resize((neededW, neededH), PIL.Image.NEAREST)
                blurredImg.paste(img, ((height - neededW)/ 2, -(neededH - height)/ 2))
            else:
                blurredImg.paste(img, ((height - width)/ 2, 0))
        blurredImg.save(name+'-blur-resize.jpg')

useBlurredAndResized()