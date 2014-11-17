from os.path import dirname, abspath, join
from bzr_sync import sync_git_to_bzr

base_dir = dirname(abspath(__file__))

sync_git_to_bzr(
    project_name='assets-manager',
    git_user='canonicalltd',
    repositories_dir=join(base_dir, 'repositories')
)

