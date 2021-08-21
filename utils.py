import numpy as np
from PIL import Image
from io import BytesIO

def calculate_mean(image_path):
  image = Image.open(image_path).convert('L').resize((512, 512))
  image = np.array(image) / 255.0
  mean_image = np.mean(image)

  return float("{:.2f}".format(mean_image))

def calculate_std(image_path):
  image = Image.open(image_path).convert('L').resize((512, 512))
  image = np.array(image) / 255.0
  std_image = np.std(image)

  return float("{:.2f}".format(std_image))

def calculate_min(image_path):
  image = Image.open(image_path).convert('L').resize((512, 512))
  image = np.array(image)
  return np.amin(image)

def calculate_max(image_path):
  image = Image.open(image_path).convert('L').resize((512, 512))
  image = np.array(image)
  return np.amax(image)

def deal_img_file(image_path):

  #calculate statistical values of actual image
  min = calculate_min(image_path)
  max = calculate_max(image_path)
  mean = calculate_mean(image_path)
  std = calculate_std(image_path)

  #get thumbnail of image with pil function
  img = Image.open(image_path)
  img.thumbnail((90,90))

  #To don't save thumbnail as local files, write it byteStream and
  #and save on db from.
  stream = BytesIO()
  img.convert('RGB').save(stream, "JPEG")
  return stream, min, max, mean, std