from PIL import Image,ImageEnhance
import PIL

def reduce_opacity(im, opacity):
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im

def watermark_image(filename,source):
    # import and convert to RGBA
    background = Image.open(source)
    img = Image.open('ol.png')
    background = background.convert("RGBA")
    overlay = img.convert("RGBA")

    # transform overlay image
    basewidth,baseheight = background.size
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), PIL.Image.ANTIALIAS)


    # hori,verti
    w2,h2 = img.size
    background.paste(img,(0,baseheight-h2),reduce_opacity(img,.2))
    background.save("converted/"+filename,"PNG")