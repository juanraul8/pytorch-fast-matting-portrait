import os
import urllib
from PIL import Image
from threading import Thread
from Queue import Queue

from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


#q = Queue(1000)
data_folder = 'images_data'

def download(imgname, url):
    pstr = 'download image %s ...' % imgname

    if url == 'None':
        print(pstr + ' None')
        return

    imgpath = os.path.join(data_folder, imgname)
    if os.path.exists(imgpath):
        print(pstr + ' Exist, Skip!')
        return

    urllib.urlretrieve(url, imgpath)
    print(pstr + ' Done!')


def crop(imgname, crop_xy):
    pstr = 'crop image %s ...' % imgname
    crop_xy = list(map(int, crop_xy.split()))

    imgpath = os.path.join(data_folder, imgname)
    
    if os.path.exists(imgpath):
        if not os.path.exists(os.path.join(data_folder + '_crop', imgname)):
            img = Image.open(imgpath)
            area = (crop_xy[2], crop_xy[0], crop_xy[3], crop_xy[1])
            img = img.crop(area)
            img = img.resize((600, 800))
            img.save(os.path.join(data_folder + '_crop', imgname))
            print(pstr + ' Done!')
        else:
            print('Exists!')
    else:
        print(pstr + ' Does not exist!')


def thread_work():
    while True:
        job, params = q.get()
        if job == 'download':
            #download(*params)
            print("Skip")
        elif job == 'crop':
            crop(*params)
        q.task_done()


def main():
    if not os.path.isdir(data_folder):
        os.mkdir(data_folder)

    #for i in range(5):
    #    t = Thread(target=thread_work)
    #    t.daemon = True
    #    t.start()

    imgs_names = open('alldata_urls.txt', 'r').read().strip().split('\n')
    for item in imgs_names:
        print(item)
        #q.put(['download', item.split()])
    #q.join()
    print('\t\tDownload - Done!')

    images = os.listdir(data_folder)
    for item in imgs_names:
        img_path = os.path.join(data_folder, item.split()[0])
        if os.path.exists(img_path):
            filesize = os.stat(img_path).st_size
            if filesize <= 10 * 1024:
                print('Remove %s which size %d bytes below 10 * 1024 bytes' % (
                    item.split()[0], filesize))
                os.remove(img_path)

    # crop the downloaded images
    if not os.path.isdir(data_folder + '_crop'):
        os.mkdir(data_folder + '_crop')

    crop_params = open('crop.txt', 'r').read().strip().split('\n')
    #print(crop_params)
    for item in crop_params:
        print(item)
        #q.put(['crop', item.split(' ', 1)])
        imgname, crop_xy = item.split(' ', 1)
        crop(imgname, crop_xy)
    #q.join()
    print('\t\tEverything - Done!')


if __name__ == '__main__':
    main()
