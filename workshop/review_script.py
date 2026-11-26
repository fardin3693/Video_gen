"""Run the vendored ytb script-check tool on narration only, not editorial prose.
The tool's WPM estimate is advisory; measured audio remains the production clock.
Does not generate speech, modify scripts, call a network, or change the final MP4.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('episode', type=Path, nargs='?', default=ROOT/'workshop/episode.json')
    parser.add_argument('--wpm', type=float, default=150,
                        help='Advisory reading-speed estimate, never caption timestamps')
    args = parser.parse_args()
    try:
        episode = json.loads(args.episode.read_text())
        sections = episode['sections']
        if not sections or args.wpm <= 0:
            raise ValueError('Need spoken sections and a positive WPM')
        text = '\n'.join(s['text'].strip() for s in sections)
        if not all(isinstance(s['text'], str) and s['text'].strip() for s in sections):
            raise ValueError('Every section needs non-empty spoken text')
        with tempfile.TemporaryDirectory(prefix='workshop-script-review-') as d:
            path = Path(d)/'narration.txt'
            path.write_text(text+'\n')
            tool = ROOT/'workshop/vendor/ytb-research-skills/tools/script_check.py'
            print('Advisory WPM estimate only; use actual narration samples for duration and captions.', flush=True)
            return subprocess.run([sys.executable, str(tool), str(path), '--short',
                                   '--wpm', str(args.wpm)], check=False).returncode
    except (KeyError, ValueError, TypeError, AttributeError, OSError) as error:
        print(f'Script review failed: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
