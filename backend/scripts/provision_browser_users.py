"""Add stable human logins to a running complete pair. Never reset existing users."""

import argparse
import asyncio
import json
import sys
from pathlib import Path

from login_investigator.knowledge_base.browser_access import provision_browser_users


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version-file', type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        result = asyncio.run(provision_browser_users(args.version_file))
    except Exception:  # noqa: BLE001 - Never expose database errors or credential parameters.
        print('Browser user provisioning refused. Check both LI_GRAPH_ADMIN_PASSWORD and '
              'LI_GRAPH_READER_PASSWORD in the main .env and a complete running pair.', file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
