#!/usr/bin/env bash
# Dark-studio still (GPT Image 2.5 edit) -> 6 s 720p Seedance 2.5 clip, for each putter shot.
cd "$(dirname "$0")"
B=https://cdn.shopify.com/s/files/1/2286/3149/files
STILL='Product photo edit. Keep the gold putter EXACTLY as in the reference: identical head shape, identical neck, identical milled texture, identical green four-leaf clover, identical engraving and sight lines, same angle and framing. Change ONLY the background and lighting: a dark charcoal seamless studio background with soft falloff to near-black, one soft key light raking across the gold so the milling sparkles, subtle rim light on the edges, faint reflection under the head. Moody cinematic product render look. No text, no added logos, no extra objects.'
GUARD='The gold milled putter keeps EXACTLY its shape, neck, milling, green clover and engraving from the first frame. Dark charcoal studio background stays dark. No text, no new logos, no people, no flicker, no morphing.'

run() { # name, shopify file, motion prompt
  name=$1; src=$2; motion=$3
  [ -f "$name-src.png" ] || { curl -s -o "$name-src.webp" "$B/$src"; python -c "from PIL import Image;Image.open('$name-src.webp').convert('RGB').save('$name-src.png')"; }
  url=$(higgsfield generate create gpt_image_2_5 --image "$name-src.png" --aspect_ratio 16:9 --quality high --resolution 2k --prompt "$STILL" --wait --json | python -c "import json,sys;d=json.load(sys.stdin);d=d[0] if isinstance(d,list) else d;print(d['result_url'])")
  curl -s -o "$name-dark.png" "$url"
  vurl=$(higgsfield generate create seedance_2_5 --mode omni_reference --start-image "$name-dark.png" --duration 6 --resolution 720p --aspect_ratio 16:9 --generate_audio false --prompt "Photorealistic product film. $motion $GUARD" --wait --wait-timeout 20m --json | python -c "import json,sys;d=json.load(sys.stdin);d=d[0] if isinstance(d,list) else d;print(d['result_url'])")
  curl -s -o "$name.mp4" "$vurl"
  echo "$name $vurl"
}

run blade-3-topline 10_9f03f10f-f2a9-45a5-8b33-2f4a2ba92cc0.webp 'Slow smooth push-in on the putter head. A soft light glides along the top line and over the single white sight line, then the frame settles still.' &
run mallet-1-face 5_d4dc02e3-6a1a-4a7a-9a4e-d46c39c18bc2.webp 'A thin strip of soft white light slowly sweeps across the milled face from one end to the other, making the diamond milling sparkle. The camera creeps forward very slightly.' &
run mallet-3-wings 1_b00c01f0-8116-464a-a39c-08a6ebf82b6f.webp 'Slow gentle orbit around the mallet head. Light glides along both rear fang wings and the gap between them. Ends steady.' &
wait
echo done
