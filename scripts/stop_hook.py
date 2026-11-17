#!/usr/bin/env python3
"""Run a trusted project check; turn failure into an explicit Stop block."""
import argparse
import json
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--timeout', type=float, default=60)
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ['--'] else args.command
    reason = None
    if not command or args.timeout <= 0:
        reason = 'Verification blocked: configure a command and a positive timeout.'
    else:
        try:
            result = subprocess.run(command, stdin=subprocess.DEVNULL,
                                    stdout=sys.stderr, stderr=sys.stderr, timeout=args.timeout)
            if result.returncode:
                reason = f'Verification blocked: check exited {result.returncode}. Fix the check before completing.'
        except subprocess.TimeoutExpired:
            reason = 'Verification blocked: check timed out. Investigate and rerun.'
        except OSError as error:
            reason = f'Verification blocked: configured command could not start ({type(error).__name__}).'
    if reason:
        print(reason, file=sys.stderr)
        # Explicit JSON also avoids the Stop event's missing-file stderr exception.
        print(json.dumps({'decision': 'block', 'reason': reason}))
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
