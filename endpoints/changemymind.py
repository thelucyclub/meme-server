from io import BytesIO

from PIL import Image, ImageDraw
from flask import send_file

from utils.endpoint import Endpoint, setup
from utils.textutils import auto_text_size


@setup
class ChangeMyMind(Endpoint):
    params = ['text']

    def generate(self, avatars, text, usernames, kwargs):
        base = Image.open(self.assets.get('assets/changemymind/changemymind.bmp')).convert('RGBA')
        # We need a text layer here for the rotation
        text_layer = Image.new('RGBA', base.size)
        font, text = auto_text_size(text, self.assets.get_font('assets/fonts/sans.ttf'), 310)
        canv = ImageDraw.Draw(text_layer)

        canv.text((290, 300), text, font=font, fill='Black')

        text_layer = text_layer.rotate(23, resample=Image.BICUBIC)

        base.paste(text_layer, (0, 0), text_layer)
        base = base.convert('RGB')

        b = BytesIO()
        base.save(b, format='jpeg')
        b.seek(0)
        return send_file(b, mimetype='image/jpeg')
