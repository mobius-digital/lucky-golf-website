#!/usr/bin/env bash
# Takomo "balanced" sequence, Blade: B = swing top view -> low front view; C = front view -> X-ray with shaft line + balance point.
cd "$(dirname "$0")"
gen() { # name start end prompt
  url=$(higgsfield generate create seedance_2_5 --mode omni_reference --start-image "$2" --end-image "$3" --duration 5 --resolution 720p --aspect_ratio 16:9 --generate_audio false --prompt "$4" --wait --wait-timeout 25m --json 2>/dev/null | python -c "import json,sys;d=json.load(sys.stdin);d=d[0] if isinstance(d,list) else d;print(d.get('result_url') or '')")
  [ -n "$url" ] && curl -s -o "$1.mp4" "$url"; echo "$1 $url"
}
gen seq-b-swing blade-3-topline-dark.png blade-face-dark.png "High-end CGI product animation for a premium golf brand, like a real 3D render. The gold putter head stays rigid and keeps its exact shape, neck, sight line and green clover. One smooth, confident camera move: the camera arcs from the high view looking down at the back of the head, sweeping down and around to a low view facing the milled face, ending exactly on the last frame. Slight motion blur during the fastest part of the move, eased in and out. Dark charcoal studio, soft rim light. No text, no people, no extra objects, no morphing." &
gen seq-c-xray blade-face-dark.png blade-face-xray.png "High-end CGI product animation, clean like a 3D engineering render. Locked-off camera with a very slow push-in; the putter never moves or changes shape. Hold on the solid gold head for a beat, then the gold metal turns into dark transparent glass revealing thin glowing pale-gold wireframe edges. Then one thin warm-orange line draws smoothly down the centre of the shaft and neck to the sole, a small hollow circle with a crosshair fades in at the middle of the head, and a thin dashed line draws across from the circle to the orange line. Ends exactly on the final frame. Dark studio. No text, no labels, no people, no particles, no morphing." &
wait; echo done
