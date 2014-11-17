from os.path import dirname, abspath, join
import sys

from bzr_sync import sync_git_to_bzr

base_dir = dirname(abspath(__file__))

if len(sys.argv) < 3:
    print (
        "Usage: run-sync.py {project_name} {launchpad_project_name} "
        "{github_user} {launchpad_user}"
    )
    exit(1)

sync_git_to_bzr(
    project_name=sys.argv[1],
    launchpad_project_name=sys.argv[2],
    github_user=sys.argv[3],
    launchpad_user=sys.argv[4],
    repositories_dir=join(base_dir, 'repositories')
)
