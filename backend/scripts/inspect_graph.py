"""Prepare checked native Browser queries for one complete graph version. No provider calls."""

import argparse
import asyncio
import json
import sys
from pathlib import Path

from login_investigator.knowledge_base.inspection import prepare_inspection


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version-file', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--finding-id')
    args = parser.parse_args(argv)
    try:
        report = asyncio.run(prepare_inspection(args.version_file, args.output, args.finding_id))
    except Exception as error:
        print(f'Inspection preparation failed ({type(error).__name__}). Check the complete version, '
              'running services, finding ID and a new output directory. No application selection changed.', file=sys.stderr)
        return 1
    print(json.dumps(report, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
