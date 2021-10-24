#https://colab.research.google.com/drive/1AOkk-TSDFbvCb3Mxb7sTqRMAFbMi6Ra-?usp=sharing#scrollTo=vgZemXj6hejq
#!apt install tesseract-ocr-rus
#!apt install libtesseract-dev
#!pip install pytesseract
import pytesseract
import cv2
import pandas as pd


def tesseract_enabled():
    return 'rus' in pytesseract.get_languages()


# def get_text_corpus(jpg, config=r'-l rus --oem 3 --psm 6'):
#     '''
#     # Функция принимает на вход jpg, возвращает корпус текста строкой
#     # txt, coord = get_text_corpus(img)
#     '''
#     if not tesseract_enabled():
#         raise Exception('Russian is not installed..')
        
#     data = pytesseract.image_to_data(jpg, output_type='data.frame', config=config)
#     data = data[~pd.isna(data.text)]
#     #data.text = data.text.apply(lambda x: x.lower())
    
#     if len(data) < 1:
#         raise Exception('No words..')
#     try:
#         return data.text.str.cat(sep=' '), data #[['left', 'top', 'width', 'height']]
#     except:
#         return ' '.join(data['text'].astype('str')), data


def get_text_corpus(jpg):
    if not tesseract_enabled():
        raise Exception('Russian is not installed..')
        
    data = pytesseract.image_to_data(jpg, output_type='data.frame', lang='rus', config='hocr')
    median = data[data['conf'] > 0]['conf'].median()
    data = data[~pd.isna(data.text)]
    
    if median >= 95:
        metrics = 1
    else:
        metrics = 0

    if len(data) < 1:
        raise Exception('No words..')
    try:
        return data.text.str.cat(sep=' '), data, metrics #[['left', 'top', 'width', 'height']]
    except:
        return ' '.join(data['text'].astype('str')), data, metrics     
 
def get_text_corpus_doc(doc):
    return ''


def get_jpg_anon(jpg, coordinates, filled=True):
    '''
    # Функция принимает картинку, список имен, возвращает картинку с закрашенными
    # plt.imshow(get_jpg_anon(img, coord))
    '''
    if filled:
        filled = -1
    else:
        filled = 2
    for item in coordinates.iterrows():
        c = item[1]
        jpg = cv2.rectangle(jpg, (c.left, c.top), (c.left + c.width, c.top + c.height), (0, 0, 0), filled) #black
    return jpg

    
