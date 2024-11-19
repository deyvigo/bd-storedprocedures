from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

from utils.hash_name import hash_name

def draw_transaccion_pdf(transaction):
  width, height = 800, 1600
  image = Image.new('RGB', (width, height), (255, 255, 255))
  draw = ImageDraw.Draw(image)

  path_logo = os.path.join(os.getcwd(), 'logo/logo.png')
  logo = Image.open(path_logo)

  # Posicionar el logo (centrado horizontalmente)
  image.paste(logo, (400 - int(logo.width / 2), 100 - int(logo.height / 2)))

  path = os.path.join(os.getcwd(), 'font/SourGummy-Regular.ttf')
  font = ImageFont.truetype(path, 28)

  brand = "tourXpress S.A.C."
  bbox = draw.textbbox((0,0), brand, font=font)
  text_width = bbox[2] - bbox[0]
  draw.text(((width - text_width) / 2, 200), brand, fill=(0, 0, 0), font=font)

  title = f"BOLETA {transaction["id_transaccion"]:016}"
  
  # calculate the width of the text
  bbox = draw.textbbox((0,0), title, font=font)
  text_width = bbox[2] - bbox[0]

  draw.text(((width - text_width) / 2, 260), title, fill=(0, 0, 0), font=font)


  # save
  directory = os.path.join(os.getcwd(), 'transactions')

  name = "aaaaaaaaaaa"
  hashed_name = hash_name(name)
  if not os.path.exists(directory):
    os.makedirs(directory)
  
  path = os.path.join(os.getcwd(), f'transactions/{hashed_name}.pdf')

  image = image.filter(ImageFilter.SMOOTH)
  image.save(path, 'PDF')

  return hashed_name