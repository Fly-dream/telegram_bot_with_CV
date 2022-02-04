import os
import pathlib

import tensorflow as tf
import matplotlib as mpl
import pandas as pd
import logging

# Load compressed models from tensorflow_hub
os.environ['TFHUB_MODEL_LOAD_FORMAT'] = 'COMPRESSED'
mpl.rcParams['figure.figsize'] = (12, 12)
mpl.rcParams['axes.grid'] = False

IMAGE_SIZE = 500
local_path = pathlib.Path().resolve()
styles_path = local_path / 'styles'
image_classes_path = local_path / 'styles_classes'


def load_img(path_to_img):
    logging.info(f'Trying to load file {path_to_img}')
    img = tf.io.read_file(path_to_img)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)
    shape = tf.cast(tf.shape(img)[:-1], tf.float32)
    long_dim = max(shape)
    scale = IMAGE_SIZE / long_dim
    new_shape = tf.cast(shape * scale, tf.int32)
    img = tf.image.resize(img, new_shape)
    img = img[tf.newaxis, :]
    img = img * 255
    return img


def find_images(path):
    images = pd.DataFrame()
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".jpg"):
                path = os.path.join(file)
                path = pd.Series(data=path)
                images = images.append(path, ignore_index=True)
                logging.info(f'Find a file {path}')
    images.rename(columns={0: 'filename'}, inplace=True)
    logging.info(f'Find {len(images.index)} images')
    return images


def get_image_classes(images):
    df = pd.DataFrame()
    vgg = tf.keras.applications.VGG19(include_top=True, weights='imagenet')
    for index, row in images.iterrows():
        path = styles_path + images["filename"][index]
        image = load_img(path)
        x = tf.keras.applications.vgg19.preprocess_input(image)
        x = tf.image.resize(x, (224, 224))
        prediction_probabilities = vgg(x)
        predicted_top_5 = pd.DataFrame(
            tf.keras.applications.vgg19.decode_predictions(prediction_probabilities.numpy())[0],
            columns=["id", "name", "probability"])
        for ind, rw in predicted_top_5.iterrows():
            frame = [images["filename"][index], predicted_top_5["id"][ind], predicted_top_5["name"][ind],
                     predicted_top_5["probability"][ind]]
            df2 = pd.DataFrame([frame], columns=["filename", "id", "name", "probability"])
            df = df.append(df2, ignore_index=True)
        x = None
    logging.info(f'Return {len(df.index)} classes for images')
    return df


def match_style_image(image):
    logging.info(f'Looking for the best style image for {image}')
    image = load_img(image)
    vgg = tf.keras.applications.VGG19(include_top=True, weights='imagenet')
    x = tf.keras.applications.vgg19.preprocess_input(image)
    x = tf.image.resize(x, (224, 224))
    prediction_probabilities = vgg(x)
    predicted_top_5 = pd.DataFrame(
        tf.keras.applications.vgg19.decode_predictions(prediction_probabilities.numpy())[0],
        columns=["id", "name", "probability"])
    path = image_classes_path / 'local_images_classes.csv'
    styles = pd.read_csv(str(path))
    styles = styles.merge(predicted_top_5, how='left', on='id',
                                                      suffixes=('_left', '_right'))
    styles.sort_values(by=['probability_right', 'probability_left'], ascending=False, inplace=True)
    styles = styles.reset_index(drop=True)
    filename = styles['filename'][0]
    logging.info(f'Matched image {filename}')
    return filename



if __name__ == '__main__':
    local_images = find_images(styles_path)
    local_images_classes = get_image_classes(local_images)
    path = image_classes_path / 'local_images_classes.csv'
    local_images_classes.to_csv(str(path))