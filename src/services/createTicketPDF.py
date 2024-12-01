from PIL import Image, ImageDraw, ImageFont, ImageFilter
import qrcode
import os

from utils.hash_name import hash_name

def draw_ticket_pdf(ticket_data):
  width, height = 800, 1600
  image = Image.new('RGB', (width, height), (255, 255, 255))
  draw = ImageDraw.Draw(image)

  path_logo = os.path.join(os.getcwd(), 'logo/logo.png')
  logo = Image.open(path_logo)

  # Posicionar el logo (centrado horizontalmente)
  image.paste(logo, (400 - int(logo.width / 2), 100 - int(logo.height / 2)))

  path = os.path.join(os.getcwd(), 'font/SourGummy-Regular.ttf')
  font = ImageFont.truetype(path, 28)

  title = f"BOLETA {ticket_data["id_transaccion"]:016}"
  
  # calculate the width of the text
  bbox = draw.textbbox((0,0), title, font=font)
  text_width = bbox[2] - bbox[0]

  draw.text(((width - text_width) / 2, 200), title, fill=(0, 0, 0), font=font)

  draw.text((20, 260), 'Embarque:', fill=(0, 0, 0), font=font)
  draw.text((250, 260), ticket_data["embarque"], fill=(0, 0, 0), font=font)
  draw.text((20, 300), 'Desembarque:', fill=(0, 0, 0), font=font)
  draw.text((250, 300), ticket_data["desembarque"], fill=(0, 0, 0), font=font)

  draw.line((20, 360, width - 20, 360), fill=(0, 0, 0), width=2)

  draw.text((20, 380), 'Fecha:', fill=(0, 0, 0), font=font)
  draw.text((180, 380), ticket_data["fecha_salida"].strftime('%d/%m/%Y'), fill=(0, 0, 0), font=font)
  draw.text((400, 380), 'Hora:', fill=(0, 0, 0), font=font)
  draw.text((500, 380), str(ticket_data["hora_salida"]), fill=(0, 0, 0), font=font)
  draw.text((20, 420), 'Asiento:', fill=(0, 0, 0), font=font)
  draw.text((180, 420), str(ticket_data["asiento"]), fill=(0, 0, 0), font=font)
  draw.text((400, 420), 'Piso:', fill=(0, 0, 0), font=font)
  draw.text((500, 420), str(ticket_data["piso"]), fill=(0, 0, 0), font=font)
  draw.text((20, 460), 'Servicio:', fill=(0, 0, 0), font=font)
  draw.text((180, 460), ticket_data["servicio"], fill=(0, 0, 0), font=font)

  draw.line((20, 520, width - 20, 520), fill=(0, 0, 0), width=2)

  draw.text((20, 540), 'Pasajero:', fill=(0, 0, 0), font=font)
  draw.text((160, 540), ticket_data["pasajero"], fill=(0, 0, 0), font=font)
  draw.text((20, 580), 'Tipo de documento:', fill=(0, 0, 0), font=font)
  draw.text((300, 580), 'DNI', fill=(0, 0, 0), font=font)
  draw.text((20, 620), 'Número de documento:', fill=(0, 0, 0), font=font)
  draw.text((350, 620), ticket_data["dni"], fill=(0, 0, 0), font=font)

  draw.line((20, 680, width - 20, 680), fill=(0, 0, 0), width=2)

  left_margin = 600

  current_y = 700

  draw.text((20, current_y), 'Precio Neto:', fill=(0, 0, 0), font=font)
  bbox = draw.textbbox((0,0), str(ticket_data["precio_neto"]), font=font)
  text_width = bbox[2] - bbox[0]
  draw.text((left_margin - text_width, current_y), str(ticket_data["precio_neto"]), fill=(0, 0, 0), font=font)

  current_y += 40
  draw.text((20, current_y), 'IGV:', fill=(0, 0, 0), font=font)
  bbox = draw.textbbox((0,0), str(ticket_data["igv"]), font=font)
  text_width = bbox[2] - bbox[0]
  draw.text((left_margin - text_width, current_y), str(ticket_data["igv"]), fill=(0, 0, 0), font=font)

  current_y += 40
  draw.text((20, current_y), 'Precio Total:', fill=(0, 0, 0), font=font)
  bbox = draw.textbbox((0,0), str(ticket_data["precio_total"]), font=font)
  text_width = bbox[2] - bbox[0]
  draw.text((left_margin - text_width, current_y), str(ticket_data["precio_total"]), fill=(0, 0, 0), font=font)

  current_y += 40
  draw.text((20, current_y), 'Número de tarjeta:', fill=(0, 0, 0), font=font)
  bbox = draw.textbbox((0,0), ticket_data["numero_tarjeta"], font=font)
  text_width = bbox[2] - bbox[0]
  draw.text((left_margin - text_width, current_y), ticket_data["numero_tarjeta"], fill=(0, 0, 0), font=font)

  current_y += 60
  draw.line((20, current_y, width - 20, current_y), fill=(0, 0, 0), width=2)

  # QR code
  qr_data = f'{ticket_data["pasajero"]}_{ticket_data["dni"]}'
  qr = qrcode.QRCode(
    version=1, 
    error_correction=qrcode.constants.ERROR_CORRECT_L, 
    box_size=10, 
    border=1
  )
  qr.add_data(qr_data)
  qr.make(fit=True)

  # Crear la imagen del QR
  qr_img = qr.make_image(fill="black", back_color="white")
  qr_width = 400

  current_y += 20

  qr_resized = qr_img.resize((qr_width, qr_width))
  image.paste(qr_resized, ((width - qr_width) // 2, current_y))

  font = ImageFont.truetype(path, 40)

  current_y += qr_width + 20
  bbox = draw.textbbox((0,0), 'Recomendaciones', font=font)
  text_width = bbox[2] - bbox[0]

  draw.text(((width - text_width) / 2, current_y), 'Recomendaciones', fill=(0, 0, 0), font=font)

  font = ImageFont.truetype(path, 28)
  
  current_y += 60
  draw.text((20, current_y), '1. Llegar 30 minutos al terminal de embarque.', fill=(0, 0, 0), font=font)

  current_y += 40
  draw.text((20, current_y), '2. Presentarse con su DNI o pasaporte físico.', fill=(0, 0, 0), font=font)

  # generate the path to the image file
  directory = os.path.join(os.getcwd(), 'tickets')

  name = f'{ticket_data["pasajero"]}_{hash_name(ticket_data["dni"])}_{ticket_data["fecha_salida"].strftime('%d/%m/%Y')}_{str(ticket_data["hora_salida"])}_{ticket_data["id_pasaje"]}'
  hashed_name = hash_name(name)

  path = os.path.join(os.getcwd(), f'tickets/{hashed_name}.pdf')

  if not os.path.exists(directory):
    os.makedirs(directory)

  image = image.filter(ImageFilter.SMOOTH)
  image.save(path, 'PDF')

  return hashed_name
