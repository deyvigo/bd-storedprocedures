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

  title = f"BOLETA {transaction['id_transaccion']:016}"
  
  # calculate the width of the text
  bbox = draw.textbbox((0,0), title, font=font)
  text_width = bbox[2] - bbox[0]

  draw.text(((width - text_width) / 2, 260), title, fill=(0, 0, 0), font=font)

  # Draw the data of the transaction
  draw.text((20, 340), f"Fecha:", fill=(0, 0, 0), font=font)
  draw.text((180, 340), transaction["fecha_compra"].strftime('%d/%m/%Y'), fill=(0, 0, 0), font=font)
  draw.text((400, 340), f"Hora:", fill=(0, 0, 0), font=font)
  draw.text((500, 340), str(transaction["fecha_compra"].strftime('%H:%M:%S')), fill=(0, 0, 0), font=font)
  draw.text((20, 380), f"DNI:", fill=(0, 0, 0), font=font)
  draw.text((180, 380), transaction["dni"], fill=(0, 0, 0), font=font)
  draw.text((20, 420), f"RUC:", fill=(0, 0, 0), font=font)
  draw.text((180, 420), transaction["ruc"], fill=(0, 0, 0), font=font)

  draw.line((20, 480, width - 20, 480), fill=(0, 0, 0), width=2)

  # Separe by service type: pos_y = 500 * for loop
  p_text = f"Pasaje: {transaction['origen']} - {transaction['destino']}\nservicio: {transaction['servicio']} x {transaction['cantidad_pasajes']}"
  pos_y = 500
  draw.text((20, pos_y), p_text, fill=(0, 0, 0), font=font)

  left_margin = 650
  # draw igv + lines
  pos_y += 80
  draw.text((20, pos_y), f"Sub Total:", fill=(0, 0, 0), font=font)
  bbox = draw.textbbox((0,0), str(transaction["precio_neto"]), font=font)
  text_width = bbox[2] - bbox[0]
  draw.text((left_margin - text_width, pos_y), str(transaction["precio_neto"]), fill=(0, 0, 0), font=font)

  pos_y += 40
  draw.text((20, pos_y), f"IGV:", fill=(0, 0, 0), font=font)
  bbox = draw.textbbox((0,0), str(transaction["igv"]), font=font)
  text_width = bbox[2] - bbox[0]
  draw.text((left_margin - text_width, pos_y), str(transaction["igv"]), fill=(0, 0, 0), font=font)

  pos_y += 40
  draw.text((20, pos_y), f"Descuento:", fill=(0, 0, 0), font=font)
  bbox = draw.textbbox((0,0), str(transaction["descuento"]), font=font)
  text_width = bbox[2] - bbox[0]
  draw.text((left_margin - text_width, pos_y), str(transaction["descuento"]), fill=(0, 0, 0), font=font)

  pos_y += 40
  draw.text((20, pos_y), f"Total:", fill=(0, 0, 0), font=font)
  bbox = draw.textbbox((0,0), str(transaction["precio_total"]), font=font)
  text_width = bbox[2] - bbox[0]
  draw.text((left_margin - text_width, pos_y), str(transaction["precio_total"]), fill=(0, 0, 0), font=font)

  pos_y += 60
  draw.line((20, pos_y, width - 20, pos_y), fill=(0, 0, 0), width=2)

  pos_y += 20
  draw.text((20, pos_y), f"Tarjeta:", fill=(0, 0, 0), font=font)
  draw.text((180, pos_y), transaction["numero_tarjeta"], fill=(0, 0, 0), font=font)

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
