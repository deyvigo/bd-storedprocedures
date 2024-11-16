from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

def draw_ticket_pdf(ticket_data):
  width, height = 800, 1600
  image = Image.new('RGB', (width, height), (255, 255, 255))

  draw = ImageDraw.Draw(image)

  path = os.path.join(os.getcwd(), 'font/SourGummy-Regular.ttf')
  font = ImageFont.truetype(path, 28)

  title = f"BOLETA {ticket_data["id_pasaje"]:016}"
  
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
  draw.text((220, 540), ticket_data["pasajero"], fill=(0, 0, 0), font=font)
  draw.text((20, 580), 'Tipo de documento:', fill=(0, 0, 0), font=font)
  draw.text((300, 580), 'DNI', fill=(0, 0, 0), font=font)
  draw.text((20, 620), 'Número de documento:', fill=(0, 0, 0), font=font)
  draw.text((350, 620), ticket_data["dni"], fill=(0, 0, 0), font=font)

  draw.line((20, 680, width - 20, 680), fill=(0, 0, 0), width=2)

  left_margin = 600

  draw.text((20, 700), 'Precio Neto:', fill=(0, 0, 0), font=font)
  bbox = draw.textbbox((0,0), str(ticket_data["precio_neto"]), font=font)
  text_width = bbox[2] - bbox[0]
  draw.text((left_margin - text_width, 700), str(ticket_data["precio_neto"]), fill=(0, 0, 0), font=font)

  draw.text((20, 740), 'IGV:', fill=(0, 0, 0), font=font)
  bbox = draw.textbbox((0,0), str(ticket_data["igv"]), font=font)
  text_width = bbox[2] - bbox[0]
  draw.text((left_margin - text_width, 740), str(ticket_data["igv"]), fill=(0, 0, 0), font=font)

  draw.text((20, 780), 'Precio Total:', fill=(0, 0, 0), font=font)
  bbox = draw.textbbox((0,0), str(ticket_data["precio_total"]), font=font)
  text_width = bbox[2] - bbox[0]
  draw.text((left_margin - text_width, 780), str(ticket_data["precio_total"]), fill=(0, 0, 0), font=font)

  draw.text((20, 820), 'Número de tarjeta:', fill=(0, 0, 0), font=font)
  bbox = draw.textbbox((0,0), ticket_data["numero_tarjeta"], font=font)
  text_width = bbox[2] - bbox[0]
  draw.text((left_margin - text_width, 820), ticket_data["numero_tarjeta"], fill=(0, 0, 0), font=font)

  draw.line((20, 880, width - 20, 880), fill=(0, 0, 0), width=2)

  font = ImageFont.truetype(path, 40)

  bbox = draw.textbbox((0,0), 'Recomendaciones', font=font)
  text_width = bbox[2] - bbox[0]

  draw.text(((width - text_width) / 2, 900), 'Recomendaciones', fill=(0, 0, 0), font=font)

  font = ImageFont.truetype(path, 28)
  draw.text((20, 960), '1. Llegar 30 minutos al terminal de embarque.', fill=(0, 0, 0), font=font)
  draw.text((20, 1000), '2. Presentarse con su DNI o pasaporte físico.', fill=(0, 0, 0), font=font)

  # generate the path to the image file
  path = os.path.join(os.getcwd(), 'tickets/ticket.pdf')

  image = image.filter(ImageFilter.SMOOTH)
  image.save(path, 'PDF')
