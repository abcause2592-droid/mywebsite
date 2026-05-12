"""
Run this script from the same folder as index.html and headshot.jpg.
It embeds the headshot as base64 directly into the HTML, creating a
single fully portable file: index-portable.html

Usage:
  python3 embed_headshot.py
"""

import base64, re, os, sys

html_file   = "index.html"
image_file  = "headshot.jpg"
output_file = "index-portable.html"

if not os.path.exists(html_file):
    sys.exit(f"❌  {html_file} not found. Run this script from your my-website folder.")
if not os.path.exists(image_file):
    sys.exit(f"❌  {image_file} not found. Make sure it's in the same folder as index.html.")

with open(image_file, "rb") as f:
    b64 = base64.b64encode(f.read()).decode("utf-8")

data_url = f"data:image/jpeg;base64,{b64}"

with open(html_file, "r", encoding="utf-8") as f:
    html = f.read()

# Replace the src attribute
updated = html.replace('src="headshot.jpg"', f'src="{data_url}"')

with open(output_file, "w", encoding="utf-8") as f:
    f.write(updated)

size_kb = round(os.path.getsize(output_file) / 1024)
print(f"✅  Done! Created {output_file} ({size_kb} KB)")
print(f"    Upload this file anywhere — no separate image needed.")
