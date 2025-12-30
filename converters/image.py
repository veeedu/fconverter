from PIL import Image

def convert(input_path, output_path):
    img = Image.open(input_path)
    img.save(output_path)
