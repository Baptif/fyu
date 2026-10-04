"""Génère les icônes de lancement Android à partir de resources/icon-512.png.
Usage : python3 scripts/make_icons.py   (depuis la racine du projet, après `npx cap add android`)"""
import os, shutil
from PIL import Image, ImageDraw

RES = os.path.join('android', 'app', 'src', 'main', 'res')
SIZES = {'mdpi': 48, 'hdpi': 72, 'xhdpi': 96, 'xxhdpi': 144, 'xxxhdpi': 192}
src = Image.open(os.path.join('resources', 'icon-512.png')).convert('RGBA')

# On retire les icônes adaptatives par défaut (logo Capacitor) pour utiliser nos PNG.
shutil.rmtree(os.path.join(RES, 'mipmap-anydpi-v26'), ignore_errors=True)

for name, px in SIZES.items():
    d = os.path.join(RES, f'mipmap-{name}')
    os.makedirs(d, exist_ok=True)
    icon = src.resize((px, px), Image.LANCZOS)
    icon.save(os.path.join(d, 'ic_launcher.png'))
    icon.save(os.path.join(d, 'ic_launcher_foreground.png'))
    mask = Image.new('L', (px * 4, px * 4), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, px * 4 - 1, px * 4 - 1), fill=255)
    mask = mask.resize((px, px), Image.LANCZOS)
    round_icon = Image.new('RGBA', (px, px), (0, 0, 0, 0))
    round_icon.paste(icon, (0, 0), mask)
    round_icon.save(os.path.join(d, 'ic_launcher_round.png'))
print('Icônes générées.')
