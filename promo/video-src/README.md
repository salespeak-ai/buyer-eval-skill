# Demo video source

Remotion composition for `promo/buyer-eval-demo.mp4` and the GIFs. All content is
the illustrative example (fictional vendors), matching `examples/illustrative-brief.html`.

```bash
npm i remotion @remotion/cli react react-dom
voice/generate.sh      # narration: ElevenLabs if ELEVENLABS_API_KEY is set (env or .env), else macOS `say` draft
npx remotion render src/index.tsx buyer-eval ../buyer-eval-demo.mp4 --codec=h264 --crf=20
```

Narration lines live in `voice/script.json`, one per scene. Scene lengths are
computed from the generated audio (`src/voice-durations.json`), so editing a line
and regenerating keeps picture and voice in sync. Default voice: ElevenLabs
premade narrator "George" (override with `ELEVENLABS_VOICE_ID`).

`public/brief.png` is a 2x screenshot of `examples/illustrative-brief.html`.
GIFs are cut from the MP4 with ffmpeg (fps 12, 960px, 128-color palette).
