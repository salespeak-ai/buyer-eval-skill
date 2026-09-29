import React from 'react';
import {Composition, registerRoot} from 'remotion';
import {BuyerEval, SCENES, TOTAL} from './BuyerEval';

const Root: React.FC = () => (
  <>
    <Composition id="buyer-eval" component={BuyerEval} durationInFrames={TOTAL} fps={30} width={1600} height={900} />
    {/* GIF cut: terminal through the claims table */}
    <Composition
      id="buyer-eval-gif"
      component={BuyerEval}
      durationInFrames={SCENES.neutral[0]}
      fps={30}
      width={1600}
      height={900}
    />
  </>
);

registerRoot(Root);
