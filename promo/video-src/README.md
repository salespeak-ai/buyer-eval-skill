# Demo video source

Remotion composition for `promo/buyer-eval-demo.mp4` and the GIFs. All content is
the illustrative example (fictional vendors), matching `examples/illustrative-brief.html`.

```bash
npm i remotion @remotion/cli react react-dom
npx remotion render src/index.tsx buyer-eval ../buyer-eval-demo.mp4 --codec=h264 --crf=20
```

`public/brief.png` is a 2x screenshot of `examples/illustrative-brief.html`.
GIFs are cut from the MP4 with ffmpeg (fps 12, 960px, 128-color palette).
