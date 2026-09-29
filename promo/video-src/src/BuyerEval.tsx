import React from 'react';
import voiceDurations from './voice-durations.json';
import {
  AbsoluteFill,
  Audio,
  Easing,
  Img,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';

const C = {
  ink: '#1b1d21',
  muted: '#5d6470',
  line: '#e3e5e9',
  soft: '#f6f7f9',
  ok: ['#1f7a4d', '#e7f4ed'],
  warn: ['#8a5a00', '#fbf1dc'],
  bad: ['#a8322d', '#fbe9e7'],
  info: ['#34598a', '#e9eff8'],
  none: ['#5d6470', '#eef0f3'],
};
const FONT = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif';
const MONO = '"SF Mono", Menlo, Monaco, Consolas, monospace';

type Status = 'Verified' | 'Qualified' | 'Contradicted' | 'Unverified' | 'Unknown';
const STATUS_COLORS: Record<Status, string[]> = {
  Verified: C.ok,
  Qualified: C.warn,
  Contradicted: C.bad,
  Unverified: C.info,
  Unknown: C.none,
};

// Scene timing (30 fps). Each scene lasts at least its visual minimum and at
// least as long as its narration plus a short lead-in and tail.
const MIN_FRAMES = {
  title: 90,
  terminal: 330,
  found: 210,
  claims: 360,
  neutral: 150,
  unanswered: 210,
  demo: 180,
  brief: 240,
  end: 150,
} as const;
type SceneKey = keyof typeof MIN_FRAMES;
export const VOICE_LEAD = 8;
const ORDER = Object.keys(MIN_FRAMES) as SceneKey[];
const buildScenes = () => {
  const out = {} as Record<SceneKey, readonly [number, number]>;
  let at = 0;
  for (const k of ORDER) {
    const voice = (voiceDurations as Record<string, number>)[k] ?? 0;
    const dur = Math.max(MIN_FRAMES[k], Math.ceil(voice * 30) + VOICE_LEAD + 22);
    out[k] = [at, dur] as const;
    at += dur;
  }
  return {scenes: out, total: at};
};
const built = buildScenes();
export const SCENES = built.scenes;
export const TOTAL = built.total;

const fade = (frame: number, dur: number) =>
  Math.min(
    interpolate(frame, [0, 12], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
    interpolate(frame, [dur - 12, dur], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
  );

const rise = (frame: number, start: number, fps: number) => {
  const s = spring({frame: frame - start, fps, config: {damping: 200}, durationInFrames: 18});
  return {opacity: s, transform: `translateY(${(1 - s) * 16}px)`};
};

const Scene: React.FC<{dur: number; children: React.ReactNode; bg?: string}> = ({dur, children, bg = '#fff'}) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{backgroundColor: bg, fontFamily: FONT, color: C.ink}}>
      <AbsoluteFill style={{opacity: fade(frame, dur)}}>{children}</AbsoluteFill>
    </AbsoluteFill>
  );
};

const Illustrative: React.FC<{dark?: boolean}> = ({dark}) => (
  <div
    style={{
      position: 'absolute',
      bottom: 28,
      right: 40,
      fontSize: 18,
      color: dark ? '#8b919c' : C.muted,
      letterSpacing: 0.3,
    }}
  >
    Illustrative example · fictional vendors
  </div>
);

const Heading: React.FC<{eyebrow: string; title: string}> = ({eyebrow, title}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return (
    <div style={{...rise(frame, 0, fps)}}>
      <div style={{fontSize: 20, letterSpacing: 2, textTransform: 'uppercase', color: C.muted, marginBottom: 10}}>
        {eyebrow}
      </div>
      <div style={{fontSize: 52, fontWeight: 700, lineHeight: 1.15}}>{title}</div>
    </div>
  );
};

const Pill: React.FC<{status: Status; size?: number}> = ({status, size = 20}) => {
  const [fg, bg] = STATUS_COLORS[status];
  return (
    <span
      style={{
        display: 'inline-block',
        fontSize: size,
        fontWeight: 600,
        color: fg,
        background: bg,
        padding: `${size * 0.2}px ${size * 0.6}px`,
        borderRadius: 999,
        whiteSpace: 'nowrap',
      }}
    >
      {status}
    </span>
  );
};

// 1. Title
const Title: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return (
    <Scene dur={SCENES.title[1]}>
      <AbsoluteFill style={{justifyContent: 'center', padding: '0 140px'}}>
        <div style={{...rise(frame, 0, fps), fontSize: 96, fontWeight: 800, letterSpacing: -2}}>Buyer Eval</div>
        <div style={{...rise(frame, 10, fps), fontSize: 44, color: C.muted, marginTop: 12}}>
          An AI analyst for buying B2B software.
        </div>
        <div
          style={{
            ...rise(frame, 22, fps),
            marginTop: 40,
            height: 4,
            width: interpolate(frame, [22, 60], [0, 420], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)}),
            background: C.ink,
          }}
        />
      </AbsoluteFill>
    </Scene>
  );
};

// 2. Terminal
const PROMPT =
  'Evaluate Example Vendor A and Example Vendor B for customer success. We need deep Salesforce sync and we can’t wait 6 months to go live.';
const STEPS: [number, string][] = [
  [150, 'Framing criteria: 2 stated, 2 inferred'],
  [168, 'Checking for vendor AI agents: 1 found (answers treated as vendor claims)'],
  [186, 'Collecting claims from sites, docs, pricing, trust pages'],
  [204, 'Checking claims against independent sources'],
  [222, 'Challenge pass: trying to disprove the leading conclusion'],
  [240, 'Decision Brief written to ~/buyer-eval-reports/'],
];
const Terminal: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const typed = Math.floor(interpolate(frame, [18, 130], [0, PROMPT.length], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}));
  const cursorOn = Math.floor(frame / 15) % 2 === 0;
  return (
    <Scene dur={SCENES.terminal[1]} bg="#eceef1">
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
        <div
          style={{
            ...rise(frame, 0, fps),
            width: 1380,
            height: 500,
            background: '#15171b',
            borderRadius: 16,
            boxShadow: '0 30px 80px rgba(0,0,0,0.25)',
            overflow: 'hidden',
            fontFamily: MONO,
          }}
        >
          <div style={{height: 44, background: '#23262c', display: 'flex', alignItems: 'center', padding: '0 18px', gap: 10}}>
            {['#ff5f57', '#febc2e', '#28c840'].map((c) => (
              <div key={c} style={{width: 14, height: 14, borderRadius: 7, background: c}} />
            ))}
            <div style={{color: '#8b919c', fontSize: 16, marginLeft: 16, fontFamily: FONT}}>Claude Code</div>
          </div>
          <div style={{padding: '34px 40px', fontSize: 27, lineHeight: 1.55, color: '#e6e8eb'}}>
            <div>
              <span style={{color: '#7aa2f7'}}>&gt; </span>
              {PROMPT.slice(0, typed)}
              {typed < PROMPT.length && cursorOn ? <span style={{background: '#e6e8eb'}}>&nbsp;</span> : null}
            </div>
            <div style={{marginTop: 26}}>
              {STEPS.map(([at, text]) => {
                const o = interpolate(frame, [at, at + 8], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
                const done = frame > at + 14;
                return (
                  <div key={text} style={{opacity: o, color: '#c3c8cf', marginBottom: 6}}>
                    <span style={{color: done ? '#5fd38d' : '#8b919c', display: 'inline-block', width: 34}}>
                      {done ? '✓' : '…'}
                    </span>
                    {text}
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </AbsoluteFill>
      <Illustrative />
    </Scene>
  );
};

// 3. What we found
const COUNTS: [string, number][] = [
  ['claims investigated', 8],
  ['verified', 3],
  ['qualified', 2],
  ['contradicted', 1],
  ['unverified', 1],
  ['unknown', 1],
];
const Found: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return (
    <Scene dur={SCENES.found[1]}>
      <AbsoluteFill style={{padding: '90px 140px'}}>
        <Heading eyebrow="Decision Brief" title="What we found" />
        <div style={{display: 'grid', gridTemplateColumns: 'repeat(6, 1fr)', gap: 16, marginTop: 40}}>
          {COUNTS.map(([label, n], i) => {
            const shown = Math.round(
              interpolate(frame, [14 + i * 5, 40 + i * 5], [0, n], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
            );
            return (
              <div key={label} style={{...rise(frame, 10 + i * 5, fps), background: C.soft, borderRadius: 10, padding: '20px 22px'}}>
                <div style={{fontSize: 52, fontWeight: 700, color: label === 'contradicted' ? C.bad[0] : C.ink}}>{shown}</div>
                <div style={{fontSize: 20, color: C.muted}}>{label}</div>
              </div>
            );
          })}
        </div>
        <div style={{marginTop: 44, borderLeft: `5px solid ${C.ink}`, paddingLeft: 26, fontSize: 30, lineHeight: 1.45}}>
          <div style={{...rise(frame, 60, fps), marginBottom: 16}}>
            <b>Most important finding:</b> Vendor B&rsquo;s &ldquo;live in 6 weeks&rdquo; claim is contradicted by two
            customer accounts of 4-6 month rollouts.
          </div>
          <div style={{...rise(frame, 90, fps), marginBottom: 16}}>
            <b>Most important unknown:</b> whether either vendor syncs custom Salesforce objects both ways without
            professional services.
          </div>
          <div style={{...rise(frame, 120, fps)}}>
            <b>Ask next:</b> have Vendor A show a custom object syncing both ways, live.
          </div>
        </div>
      </AbsoluteFill>
      <Illustrative />
    </Scene>
  );
};

// 4. Claims vs evidence
const ROWS: {vendor: string; claim: string; source: string; evidence: string; status: Status}[] = [
  {vendor: 'A', claim: 'Bidirectional Salesforce sync (standard objects)', source: 'Vendor website', evidence: 'Docs describe it; customer reviews confirm it works', status: 'Verified'},
  {vendor: 'A', claim: 'Custom objects supported in sync', source: 'Vendor docs', evidence: 'Setup guide: “configured with your onboarding team”', status: 'Qualified'},
  {vendor: 'A', claim: 'SCIM provisioning available', source: 'Vendor docs', evidence: 'Documented; which plan includes it is stated nowhere', status: 'Unknown'},
  {vendor: 'B', claim: 'Customers go live in 6 weeks', source: 'Vendor AI agent', evidence: 'Two customer accounts describe 4-6 month rollouts', status: 'Contradicted'},
  {vendor: 'B', claim: 'Native Salesforce integration', source: 'Vendor AI agent', evidence: 'Reads from Salesforce; writing back needs a paid connector', status: 'Qualified'},
  {vendor: 'B', claim: 'Used by 1,000+ companies', source: 'Vendor website', evidence: 'No independent count found', status: 'Unverified'},
];
const Claims: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const highlight = interpolate(frame, [200, 222], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <Scene dur={SCENES.claims[1]}>
      <AbsoluteFill style={{padding: '80px 110px', display: 'block'}}>
        <Heading eyebrow="The centerpiece" title="Claims vs. evidence" />
        <div style={{marginTop: 34, fontSize: 22}}>
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: '90px 1.35fr 0.8fr 1.6fr 190px',
              gap: 16,
              padding: '12px 16px',
              background: C.soft,
              color: C.muted,
              fontSize: 16,
              letterSpacing: 1,
              textTransform: 'uppercase',
              fontWeight: 600,
            }}
          >
            <div>Vendor</div>
            <div>Claim</div>
            <div>Source of claim</div>
            <div>Evidence</div>
            <div>Status</div>
          </div>
          {ROWS.map((r, i) => {
            const isHot = r.status === 'Contradicted';
            const dim = isHot ? 1 : 1 - highlight * 0.4;
            return (
              <div
                key={r.claim}
                style={{
                  ...rise(frame, 20 + i * 14, fps),
                  display: 'grid',
                  gridTemplateColumns: '90px 1.35fr 0.8fr 1.6fr 190px',
                  gap: 16,
                  padding: '16px 16px',
                  borderBottom: `1px solid ${C.line}`,
                  alignItems: 'center',
                  background: isHot ? `rgba(251,233,231,${highlight})` : 'transparent',
                  opacity: (rise(frame, 20 + i * 14, fps).opacity as number) * dim,
                }}
              >
                <div style={{fontWeight: 600}}>{r.vendor}</div>
                <div>{r.claim}</div>
                <div style={{color: C.muted}}>{r.source}</div>
                <div>{r.evidence}</div>
                <div>
                  <Pill status={r.status} />
                </div>
              </div>
            );
          })}
        </div>
        <div
          style={{
            marginTop: 30,
            fontSize: 28,
            opacity: highlight,
            transform: `translateY(${(1 - highlight) * 10}px)`,
          }}
        >
          The vendor&rsquo;s own AI agent made the claim. Independent evidence says otherwise.
        </div>
      </AbsoluteFill>
      <Illustrative />
    </Scene>
  );
};

// 5. Neutrality
const Neutral: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const lines = [
    'Vendor AI agent answers are vendor claims.',
    'They get checked like everything else.',
    'Having an agent never improves fit, confidence, or score.',
  ];
  return (
    <Scene dur={SCENES.neutral[1]}>
      <AbsoluteFill style={{justifyContent: 'center', padding: '0 140px'}}>
        <div style={{...rise(frame, 0, fps), fontSize: 20, letterSpacing: 2, textTransform: 'uppercase', color: C.muted, marginBottom: 24}}>
          Neutral by design
        </div>
        {lines.map((l, i) => (
          <div key={l} style={{...rise(frame, 8 + i * 16, fps), fontSize: 50, fontWeight: 700, lineHeight: 1.3}}>
            {l}
          </div>
        ))}
      </AbsoluteFill>
    </Scene>
  );
};

// 6. Unanswered
const QS = [
  {q: 'Which plan includes SCIM provisioning?', who: 'Both vendors', checked: 'Pricing pages, docs, reviews, vendor AI agent', material: true},
  {q: 'Does custom-object sync need a services engagement?', who: 'Vendor A', checked: 'Docs, setup guide, community forum', material: true},
  {q: 'What happens to historical data during migration?', who: 'Both vendors', checked: 'Docs, migration guide, reviews', material: false},
];
const Unanswered: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return (
    <Scene dur={SCENES.unanswered[1]}>
      <AbsoluteFill style={{padding: '90px 140px'}}>
        <Heading eyebrow="What you still need to find out" title="Questions we still could not answer" />
        <div style={{marginTop: 40}}>
          {QS.map((q, i) => (
            <div key={q.q} style={{...rise(frame, 20 + i * 22, fps), padding: '22px 0', borderTop: i ? `1px solid ${C.line}` : 'none'}}>
              <div style={{fontSize: 32, fontWeight: 600}}>
                {q.q}{' '}
                {q.material ? <span style={{fontSize: 20, color: C.bad[0], marginLeft: 10}}>Could change the decision</span> : null}
              </div>
              <div style={{fontSize: 22, color: C.muted, marginTop: 8}}>
                Checked: {q.checked} · Who should answer: {q.who}
              </div>
            </div>
          ))}
        </div>
      </AbsoluteFill>
      <Illustrative />
    </Scene>
  );
};

// 7. Demo questions
const Demo: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const items = [
    ['Vendor A', 'Show a custom object syncing both ways, live, in a sandbox.', 'Whether it needs your onboarding team or a paid package.'],
    ['Vendor B', 'Introduce us to two customers our size who went live in under 90 days.', 'Hesitation, or references from much smaller teams.'],
  ];
  return (
    <Scene dur={SCENES.demo[1]}>
      <AbsoluteFill style={{padding: '90px 140px'}}>
        <Heading eyebrow="Walk in prepared" title="Questions for the next demo" />
        <div style={{marginTop: 44}}>
          {items.map(([v, q, l], i) => (
            <div key={q} style={{...rise(frame, 20 + i * 24, fps), marginBottom: 34}}>
              <div style={{fontSize: 22, color: C.muted, fontWeight: 600, marginBottom: 6}}>{v}</div>
              <div style={{fontSize: 34, fontWeight: 600}}>{q}</div>
              <div style={{fontSize: 24, color: C.muted, marginTop: 6}}>Listen for: {l}</div>
            </div>
          ))}
        </div>
      </AbsoluteFill>
      <Illustrative />
    </Scene>
  );
};

// 8. Brief scroll
const BRIEF_W = 1100;
const BRIEF_H = Math.round((7510 / 2200) * BRIEF_W);
const Brief: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const viewport = 640;
  const y = interpolate(frame, [30, 210], [0, -(BRIEF_H - viewport)], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.inOut(Easing.cubic),
  });
  return (
    <Scene dur={SCENES.brief[1]} bg="#eceef1">
      <AbsoluteFill style={{alignItems: 'center', paddingTop: 50}}>
        <div style={{...rise(frame, 0, fps), fontSize: 34, fontWeight: 700, marginBottom: 22}}>
          One HTML file. Forward it to the CFO, security, and the VP.
        </div>
        <div
          style={{
            ...rise(frame, 6, fps),
            width: BRIEF_W + 2,
            borderRadius: 12,
            overflow: 'hidden',
            background: '#fff',
            boxShadow: '0 30px 80px rgba(0,0,0,0.18)',
          }}
        >
          <div style={{height: 38, background: '#f1f2f4', display: 'flex', alignItems: 'center', padding: '0 14px', gap: 8, borderBottom: `1px solid ${C.line}`}}>
            {['#ff5f57', '#febc2e', '#28c840'].map((c) => (
              <div key={c} style={{width: 12, height: 12, borderRadius: 6, background: c}} />
            ))}
            <div style={{fontSize: 15, color: C.muted, marginLeft: 14}}>example-vendor-a-vs-example-vendor-b-buyer-evaluation.html</div>
          </div>
          <div style={{height: viewport, overflow: 'hidden', position: 'relative'}}>
            <Img src={staticFile('brief.png')} style={{width: BRIEF_W, position: 'absolute', top: y, left: 0}} />
          </div>
        </div>
      </AbsoluteFill>
      <Illustrative />
    </Scene>
  );
};

// 9. End card
const End: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return (
    <Scene dur={SCENES.end[1]}>
      <AbsoluteFill style={{justifyContent: 'center', padding: '0 140px'}}>
        <div style={{...rise(frame, 0, fps), fontSize: 60, fontWeight: 800, lineHeight: 1.2}}>
          What they claim.
          <br />
          What the evidence supports.
          <br />
          What you still need to ask.
        </div>
        <div
          style={{
            ...rise(frame, 20, fps),
            marginTop: 50,
            fontFamily: MONO,
            fontSize: 20,
            whiteSpace: 'nowrap',
            background: '#15171b',
            color: '#e6e8eb',
            padding: '22px 28px',
            borderRadius: 10,
            display: 'inline-block',
            alignSelf: 'flex-start',
          }}
        >
          git clone https://github.com/salespeak-ai/buyer-eval-skill.git ~/.claude/skills/buyer-eval-skill
        </div>
        <div style={{...rise(frame, 34, fps), marginTop: 26, fontSize: 24, color: C.muted}}>
          Free and open source · Works in Claude Code and the Claude desktop app
        </div>
      </AbsoluteFill>
    </Scene>
  );
};

export const BuyerEval: React.FC = () => (
  <AbsoluteFill style={{backgroundColor: '#fff'}}>
    <Sequence from={SCENES.title[0]} durationInFrames={SCENES.title[1]}><Title /><Sequence from={VOICE_LEAD}><Audio src={staticFile('voice/title.mp3')} /></Sequence></Sequence>
    <Sequence from={SCENES.terminal[0]} durationInFrames={SCENES.terminal[1]}><Terminal /><Sequence from={VOICE_LEAD}><Audio src={staticFile('voice/terminal.mp3')} /></Sequence></Sequence>
    <Sequence from={SCENES.found[0]} durationInFrames={SCENES.found[1]}><Found /><Sequence from={VOICE_LEAD}><Audio src={staticFile('voice/found.mp3')} /></Sequence></Sequence>
    <Sequence from={SCENES.claims[0]} durationInFrames={SCENES.claims[1]}><Claims /><Sequence from={VOICE_LEAD}><Audio src={staticFile('voice/claims.mp3')} /></Sequence></Sequence>
    <Sequence from={SCENES.neutral[0]} durationInFrames={SCENES.neutral[1]}><Neutral /><Sequence from={VOICE_LEAD}><Audio src={staticFile('voice/neutral.mp3')} /></Sequence></Sequence>
    <Sequence from={SCENES.unanswered[0]} durationInFrames={SCENES.unanswered[1]}><Unanswered /><Sequence from={VOICE_LEAD}><Audio src={staticFile('voice/unanswered.mp3')} /></Sequence></Sequence>
    <Sequence from={SCENES.demo[0]} durationInFrames={SCENES.demo[1]}><Demo /><Sequence from={VOICE_LEAD}><Audio src={staticFile('voice/demo.mp3')} /></Sequence></Sequence>
    <Sequence from={SCENES.brief[0]} durationInFrames={SCENES.brief[1]}><Brief /><Sequence from={VOICE_LEAD}><Audio src={staticFile('voice/brief.mp3')} /></Sequence></Sequence>
    <Sequence from={SCENES.end[0]} durationInFrames={SCENES.end[1]}><End /><Sequence from={VOICE_LEAD}><Audio src={staticFile('voice/end.mp3')} /></Sequence></Sequence>
  </AbsoluteFill>
);
