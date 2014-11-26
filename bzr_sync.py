from os.path import isdir, join, abspath, dirname

from sh import bzr, cd, git, rm, ErrorReturnCode

from wsgi_helpers import ShLogger


def sync_git_to_bzr(
    git_url,
    bzr_url,
    repositories_dir=join(dirname(abspath(__file__)), 'repositories'),
):
    """
    Using the provided {repositories_dir},
    pull down the git project from a git host (git_url),
    export all commits to a bzr repository,
    and push to a bzr host (bzr_url).
    """

    git_dir = git_url.replace('/', '-').replace(':', '-')
    bzr_dir = bzr_url.replace('/', '-').replace(':', '-')
    git_path = join(repositories_dir, git_dir)
    bzr_path = join(repositories_dir, bzr_dir)

    logger = ShLogger()

    # Clone the git repo, or pull if it exists
    if not isdir(git_path):
        logger.update_for_command(
            "Cloning " + git_url,
            git.clone(git_url, git_dir)
        )
    else:
        cd(git_path)
        logger.update_for_command(
            "Fetching " + git_url,
            git.fetch(all=True)
        )
        logger.update_for_command(
            "Resetting to HEAD",
            git.reset('--hard', 'origin/master')
        )

    # Always delete and recreate the bzr repo
    logger.update_for_command(
        "Removing bzr dir {0}".format(bzr_path),
        rm(bzr_path, r=True, f=True)
    )

    try:
        logger.update_for_command(
            "Creating BZR repo",
            bzr('init-repo', bzr_path)
        )
    except ErrorReturnCode, sh_error:
        logger.update('init-repo returned error code {0}. Message: {1}'.format(
            str(sh_error.exit_code), sh_error.message
        ))

    # Update the BZR repo with commits from git
    logger.update_for_command(
        "Entering bzr repo",
        cd(bzr_path)
    )

    logger.update_for_command(
        "Updating BZR repo",
        bzr(
            git('-C', git_path, 'fast-export', M=True, all=True),
            'fast-import', '-'
        )
    )

    logger.update_for_command(
        "Pushing BZR changes",
        bzr.push(bzr_url, overwrite=True, directory="trunk")
    )

    return logger.log
