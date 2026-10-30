"""Select a verified pair, or its previous version, for the next application restart."""

import argparse
import asyncio
import json
import sys
from pathlib import Path

from login_investigator.knowledge_base.graph_selection import select_version, rollback_version
from login_investigator.knowledge_base.staleness import KnowledgeBaseNotReady


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--state-file', type=Path, required=True,
                        help='Explicit selection file for the separately configured application')
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--version', type=Path, help='The completed version marker')
    action.add_argument('--rollback', action='store_true')
    args = parser.parse_args(argv)
    try:
        result = asyncio.run(rollback_version(args.state_file) if args.rollback
                             else select_version(args.version, args.state_file))
    except KnowledgeBaseNotReady as error:
        print(str(error), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    print('Selection verified. Restart the configured application to adopt it.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
