#!/usr/bin/env bash
# Generate per-scene narration into public/voice/<scene>.mp3 and durations.json.
# Uses ElevenLabs when ELEVENLABS_API_KEY is set (or present in ./.env), otherwise
# macOS `say` as a timing draft.
set -euo pipefail
cd "$(dirname "$0")/.."
[ -f .env ] && set -a && . ./.env && set +a
VOICE_ID="${ELEVENLABS_VOICE_ID:-JBFqnCBsd6RMkjVDRZzb}"   # George (ElevenLabs premade narrator)
MODE=draft; [ -n "${ELEVENLABS_API_KEY:-}" ] && MODE=elevenlabs
echo "voice mode: $MODE"
mkdir -p public/voice
for key in $(python3 -c "import json;print(' '.join(json.load(open('voice/script.json'))))"); do
  text=$(python3 -c "import json,sys;print(json.load(open('voice/script.json'))[sys.argv[1]])" "$key")
  out="public/voice/$key.mp3"
  if [ "$MODE" = elevenlabs ]; then
    body=$(python3 -c "import json,sys;print(json.dumps({'text':sys.argv[1],'model_id':'eleven_multilingual_v2','voice_settings':{'stability':0.55,'similarity_boost':0.75,'style':0.15}}))" "$text")
    code=$(curl -sS -o "$out" -w '%{http_code}' -X POST "https://api.elevenlabs.io/v1/text-to-speech/$VOICE_ID?output_format=mp3_44100_128" \
      -H "xi-api-key: $ELEVENLABS_API_KEY" -H 'Content-Type: application/json' -d "$body")
    [ "$code" = 200 ] || { echo "ElevenLabs error $code for $key: $(head -c 300 "$out")"; exit 1; }
  else
    say -v Samantha -r 175 -o /tmp/bev-$key.aiff "$text"
    ffmpeg -loglevel error -y -i /tmp/bev-$key.aiff -ar 44100 -b:a 128k "$out"
  fi
done
python3 - <<'PY'
import json, subprocess
keys = list(json.load(open('voice/script.json')))
d = {}
for k in keys:
    s = subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'public/voice/{k}.mp3']).decode().strip()
    d[k] = round(float(s), 3)
json.dump(d, open('src/voice-durations.json','w'), indent=2)
print(d)
PY
