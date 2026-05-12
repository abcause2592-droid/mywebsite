#!/bin/bash
# Organize Downloads — scheduled task

DOWNLOADS="/Users/abcause25/Downloads"

# Category → extensions mapping
declare -A EXT_MAP=(
  [documents]="pdf doc docx txt rtf pages odt pptx key xlsx numbers csv"
  [images]="jpg jpeg png gif svg heic webp tiff bmp ico raw"
  [videos]="mp4 mov avi mkv wmv m4v webm"
  [audio]="mp3 wav m4a aac flac ogg aiff"
  [archives]="zip tar gz 7z rar bz2"
  [installers]="dmg pkg exe msi deb rpm appimage"
  [code]="py js ts html css json yaml yml sh rb java go rs cpp c h"
)

moved=0
skipped=()

# Process each file at root level only
for filepath in "$DOWNLOADS"/*; do
  # Skip if it's a directory
  [ -d "$filepath" ] && continue
  # Skip hidden files
  filename=$(basename "$filepath")
  [[ "$filename" == .* ]] && continue

  # Get lowercase extension
  ext="${filename##*.}"
  ext=$(echo "$ext" | tr '[:upper:]' '[:lower:]')

  # Find matching category
  matched_folder=""
  for folder in "${!EXT_MAP[@]}"; do
    for e in ${EXT_MAP[$folder]}; do
      if [ "$ext" = "$e" ]; then
        matched_folder="$folder"
        break 2
      fi
    done
  done

  if [ -n "$matched_folder" ]; then
    dest="$DOWNLOADS/$matched_folder"
    mkdir -p "$dest"
    mv "$filepath" "$dest/"
    echo "  Moved: $filename → $matched_folder/"
    ((moved++))
  else
    skipped+=("$filename")
    echo "  Skipped (no category): $filename"
  fi
done

echo ""
echo "Done. Moved: $moved file(s)."
if [ ${#skipped[@]} -gt 0 ]; then
  echo "Skipped ${#skipped[@]} file(s) with unrecognized extensions:"
  for f in "${skipped[@]}"; do echo "  - $f"; done
fi
