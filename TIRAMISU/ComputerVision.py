import sensor, image, time, math
from pyb import LED,UART,Pin
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQSIF)
sensor.set_auto_gain(True)
sensor.set_auto_whitebal(False)
sensor.set_auto_exposure(True)
sensor.set_contrast(3)
sensor.set_saturation(3)
ImageX = 88
ImageY = 60
letter_thresholds = (0, 50)
red_thresholds = (30, 70, 30, 100, 30, 100)
yellow_thresholds = (70, 100, -10, 30, 60, 100)
green_thresholds = (30, 100, -100, -40, 30, 100)
uart = UART(3, 9600, timeout_char=10)
uart.init(9600)
clock = time.clock()
blobHcenter = 0
blobHtop = 255
blobHbottom = 255
blobHleft = 0
blobHright = 0
blobHtopleft = 0
blobHtopright = 0
blobHbottomleft = 0
blobHbottomright = 0
blobScenter = 0
blobStop = 0
blobSbottom = 0
blobSleft = 255
blobSright = 255
blobStopleft = 255
blobStopright = 255
blobSbottomleft = 255
blobSbottomright = 255
blobUcenter = 255
blobUtop = 255
blobUbottom = 0
blobUleft = 0
blobUright = 0
blobUtopleft = 0
blobUtopright = 0
blobUbottomleft = 255
blobUbottomright = 255

while(True):
    clock.tick()
    img = sensor.snapshot()
    red_blobfound=False
    yellow_blobfound=False
    green_blobfound=False
    for blob in img.find_blobs([red_thresholds], area_threshold=150, merge=False):
        if(max(blob.w(), blob.h())/min(blob.w()+blob.w(), blob.h())<1.5 and blob.cx()+(blob.w()/2)<ImageX and blob.cx()-(blob.w()/2)>0 and blob.cy()-(blob.h()/2)>0 and blob.cy()+(blob.h()/2)<ImageY and math.sqrt(((blob.cx()-(ImageX/2))*(blob.cx()-(ImageX/2)))+((blob.cy()-(ImageY/2))*(blob.cy()-(ImageY/2))))<(ImageY/3) and img.get_statistics(roi=blob.rect()).stdev()<30):
            red_blobfound=True
            img.draw_rectangle(blob.rect())
    for blob in img.find_blobs([yellow_thresholds], area_threshold=150, merge=False):
        if(max(blob.w(), blob.h())/min(blob.w()+blob.w(), blob.h())<1.5 and blob.cx()+(blob.w()/2)<ImageX and blob.cx()-(blob.w()/2)>0 and blob.cy()-(blob.h()/2)>0 and blob.cy()+(blob.h()/2)<ImageY and math.sqrt(((blob.cx()-(ImageX/2))*(blob.cx()-(ImageX/2)))+((blob.cy()-(ImageY/2))*(blob.cy()-(ImageY/2))))<(ImageY/3) and img.get_statistics(roi=blob.rect()).stdev()<30):
            yellow_blobfound=True
            img.draw_rectangle(blob.rect())
    for blob in img.find_blobs([green_thresholds], area_threshold=150, merge=False):
        if(max(blob.w(), blob.h())/min(blob.w()+blob.w(), blob.h())<1.5 and blob.cx()+(blob.w()/2)<ImageX and blob.cx()-(blob.w()/2)>0 and blob.cy()-(blob.h()/2)>0 and blob.cy()+(blob.h()/2)<ImageY and math.sqrt(((blob.cx()-(ImageX/2))*(blob.cx()-(ImageX/2)))+((blob.cy()-(ImageY/2))*(blob.cy()-(ImageY/2))))<(ImageY/3) and img.get_statistics(roi=blob.rect()).stdev()<30):
            green_blobfound=True
            img.draw_rectangle(blob.rect())
    img.cartoon(size=1, seed_threshold=1)
    img.binary([letter_thresholds], zero=True)
    letter_blobfound=False
    for blob in img.find_blobs([letter_thresholds], area_threshold=150, merge=False):
        if(max(blob.w(), blob.h())/min(blob.w()+blob.w(), blob.h())<1.5 and blob.cx()+(blob.w()/2)<ImageX and blob.cx()-(blob.w()/2)>0 and blob.cy()-(blob.h()/2)>0 and blob.cy()+(blob.h()/2)<ImageY and math.sqrt(((blob.cx()-(ImageX/2))*(blob.cx()-(ImageX/2)))+((blob.cy()-(ImageY/2))*(blob.cy()-(ImageY/2))))<(ImageY/3) and img.get_statistics(roi=blob.rect()).stdev()>30):
            letter_blobfound=True
            SimilarityH = 255-((abs(image.rgb_to_grayscale(img.get_pixel(blob.cx(), blob.y()))-blobHtop)+abs(image.rgb_to_grayscale(img.get_pixel(blob.x(), blob.cy()))-blobHleft)+abs(image.rgb_to_grayscale(img.get_pixel(blob.x(), blob.y()))-blobHtopleft)+abs(image.rgb_to_grayscale(img.get_pixel(blob.cx(), blob.cy()))-blobHcenter))/4)
            SimilarityS = 255-((abs(image.rgb_to_grayscale(img.get_pixel(blob.cx(), blob.y()))-blobStop)+abs(image.rgb_to_grayscale(img.get_pixel(blob.x(), blob.cy()))-blobSleft)+abs(image.rgb_to_grayscale(img.get_pixel(blob.x(), blob.y()))-blobStopleft)+abs(image.rgb_to_grayscale(img.get_pixel(blob.cx(), blob.cy()))-blobScenter))/4)
            SimilarityU = 255-((abs(image.rgb_to_grayscale(img.get_pixel(blob.cx(), blob.y()))-blobUtop)+abs(image.rgb_to_grayscale(img.get_pixel(blob.x(), blob.cy()))-blobUleft)+abs(image.rgb_to_grayscale(img.get_pixel(blob.x(), blob.y()))-blobUtopleft)+abs(image.rgb_to_grayscale(img.get_pixel(blob.cx(), blob.cy()))-blobUcenter))/4)
            img.draw_rectangle(blob.rect())
    if(red_blobfound==True):
        print('Red')
        uart.write('R')
    elif(yellow_blobfound==True):
        print('Yellow')
        uart.write('Y')
    elif(green_blobfound==True):
        print('Green')
        uart.write('G')
    elif(letter_blobfound==True):
        if(SimilarityS>=SimilarityH and SimilarityS>=SimilarityU):
            print('S')
            uart.write('S')
        elif(SimilarityU>=SimilarityH and SimilarityU>=SimilarityS):
            print('U')
            uart.write('U')
        else:
            print('H')
            uart.write('H')
    else:
        print(clock.fps())
        uart.write('n')
