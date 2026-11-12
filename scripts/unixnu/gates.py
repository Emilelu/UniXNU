"""Run the device repository's compliance registry before any build-ish step.

`clean_build.sh` was the only thing that ran the gates, so calling `unixnu build`
directly produced untracked artefacts that skipped every rule. The registry is
now consulted here, inside the tool, so a build cannot be started without it.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

from .util import Error

GATED = ('build', 'bootimg', 'vendor_boot', 'ipsw', 'release')


def preflight(ctx, command: str, skip: bool = False) -> None:
    if command not in GATED:
        return
    if skip or os.environ.get('UNIXNU_SKIP_GATES') == '1':
        print(f'unixnu: {command}: GATES SKIPPED on request; the result is not gated',
              file=sys.stderr)
        return
    script = ctx.device / 'scripts' / 'check-rules.py'
    if not script.is_file():
        raise Error(f'{script} is missing: refusing to {command} without the compliance registry')
    repo = os.environ.get('K60_REPO') or str(ctx.device)
    if not (Path(repo) / 'docs' / 'engineering' / 'RULES.toml').is_file():
        raise Error(
            f'{command} refused: {repo} has no docs/engineering/RULES.toml, so the registry '
            f'cannot run. Point K60_REPO at the device repository that produced this build input.')
    env = dict(os.environ)
    if env.get('K60_FORCE_NEW') and not env.get('K60_PORTING_ARGS'):
        env['K60_PORTING_ARGS'] = '--force-new-series'
    print(f'unixnu: {command}: running the compliance registry ({repo})', file=sys.stderr)
    done = subprocess.run([sys.executable, str(script), '--repo', repo], cwd=str(ctx.device),
                          env=env, capture_output=True, text=True, check=False)
    if done.returncode == 0:
        return
    failures = [line for line in (done.stdout + done.stderr).splitlines()
                if line.startswith('❌') or re.match(r'^   - ', line)]
    raise Error(f'{command} refused: the compliance registry failed\n' + '\n'.join(failures[:12]))
