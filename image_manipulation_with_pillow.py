import PIL
from PIL import Image
from PIL import ImageEnhance
from PIL import ImageDraw
from PIL import ImageFont


#help(Image)

# read image and convert to RGB
image=Image.open("readonly/msi_recruitment.gif")
image=image.convert('RGB')


# build a list of 9 images which have different brightnesses
enhancer=ImageEnhance.Brightness(image)
images=[]
for i in range(1, 10):
    images.append(enhancer.enhance(i/10))

# create a contact sheet from different brightnesses
first_image=images[0]
#text_sheet = PIL.Image.new(first_image.mode, (first_image.width,150))
#display(text_sheet)

photo_text_sheet=PIL.Image.new(first_image.mode, (first_image.width,first_image.height+150))


#Create the text boxes with a function
def textbox(channel, val):
    text_sheet = PIL.Image.new(first_image.mode, (first_image.width,80))
    font = ImageFont.truetype(font='readonly/fanwood-webfont.ttf', size=75)
    text_box = ImageDraw.Draw(text_sheet)    
    text_box.text((10,5), "Channel {} Intensity {}".format(channel, val), font=font)
                        
    return text_sheet


#function to modify RGB parameters. Available by 2 different systems
def RGBmodify(img, channel, val):
    
    r, g, b = img.split()
    #Rpixels = list(img.getdata(band=0))
    #Gpixels = list(img.getdata(band=1))
    #Bpixels = list(img.getdata(band=2))
    
    if channel == 0:
        r = r.point(lambda i : int(i*val))        
        #Rpixels = [int(pix*val) for pix in Rpixels]
    if channel == 1:
        g = g.point(lambda i : int(i*val))
        #Gpixels = [int(pix*val) for pix in Gpixels]
    if channel == 2:
        b = b.point(lambda i : int(i*val))
        #Bpixels = [int(pix*val) for pix in Bpixels]
        
    #pixel_list = list(zip(Rpixels, Gpixels, Bpixels))
    #im2 = Image.new(img.mode, img.size)
    #im2.putdata(pixel_list)
    modified_image = Image.merge('RGB', (r, g, b))

    return modified_image


#make text boxes to add in the footer of the picture
text_list = []
channel_values = [0.1, 0.5, 0.9]
        
for channel in range(0,3):
    for val in channel_values:
        text_list.append(textbox(channel, val))


    
accum = 0     
images_list_color_modified = []
for channel in range(0,3):
    for val in channel_values:
        #merge picture with the footer
        image_and_text_sheet = PIL.Image.new(image.mode, (image.width,image.height+150))
        image_and_text_sheet.paste(image, (0, 0) )
        image_and_text_sheet.paste(text_list[accum], (0, image.height) )
        #modify the picture + footer in a function passing channel and multiplier value
        img = RGBmodify(image_and_text_sheet,channel, val)
        images_list_color_modified.append(img)
        accum += 1
        
        
#use the first image in the list to have the dimensions        
first_image_and_text = images_list_color_modified[0]
   
#create a base to paste all the elements
contact_sheet=PIL.Image.new(first_image_and_text.mode, (first_image_and_text.width*3,first_image_and_text.height*3))
x=0
y=0
    
for img in images_list_color_modified:
    # Lets paste the current image into the contact sheet
    contact_sheet.paste(img, (x, y) )
    # Now we update our X position. If it is going to be the width of the image, then we set it to 0
    # and update Y as well to point to the next "line" of the contact sheet.
    if x+first_image_and_text.width == contact_sheet.width:
        x=0
        y=y+first_image_and_text.height
    else:
        x=x+first_image_and_text.width

# resize and display the contact sheet
contact_sheet = contact_sheet.resize((int(contact_sheet.width/2),int(contact_sheet.height/2) ))
display(contact_sheet)