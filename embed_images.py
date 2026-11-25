import base64, json, mimetypes, pathlib

here = pathlib.Path(__file__).resolve().parent
src = here / 'drug-eruption-ddx.html'
img_dir = here / 'images'
out = here / 'drug-eruption-standalone.html'

html = src.read_text(encoding='utf-8')
data = {}
for f in sorted(img_dir.rglob('*')):
    if f.is_file() and f.suffix.lower() in ('.jpg', '.jpeg', '.png', '.webp'):
        rel = f.relative_to(img_dir).as_posix()
        mime = mimetypes.guess_type(f.name)[0] or 'image/jpeg'
        data[rel] = f"data:{mime};base64," + base64.b64encode(f.read_bytes()).decode('ascii')

marker = 'const EMBEDDED_IMAGES = {};'
assert html.count(marker) == 1, 'ไม่พบจุดฝังรูปในไฟล์ HTML'
html = html.replace(marker, 'const EMBEDDED_IMAGES = ' + json.dumps(data, ensure_ascii=False) + ';')
out.write_text(html, encoding='utf-8')
print(f'ฝังรูป {len(data)} ไฟล์ -> {out.name}')
