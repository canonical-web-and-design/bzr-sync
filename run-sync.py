from os.path import dirname, abspath, join
import sys

from bzr_sync import sync_git_to_bzr

base_dir = dirname(abspath(__file__))

if len(sys.argv) < 3:
    print "Usage: run-sync.py {project_name} {git_user}"
    exit(1)

sync_git_to_bzr(
    project_name=sys.argv[1],
    git_user=sys.argv[2],
    repositories_dir=join(base_dir, 'repositories')
)
