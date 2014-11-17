from os.path import isdir, join

from sh import bzr, cd, git, rm

from wsgi_helpers import Logger


def sync_git_to_bzr(project_name, git_user, repositories_dir):
    """
    Using the provided {repositories_dir},
    pull down the git project from github
    (git@github.com:{git_user}/{project_name}.git),
    export all commits to a bzr repository,
    and push to launchpad at lp:{project_name}.

    If the launchpad repo already exists, this will fail the first time
    because the history will be entirely different from the existing history.
    Therefore, after running this the first time and getting an error,
    `cd {project_name}-bzr/` and run `bzr push --overwrite`.

    From then on, every subsequent time you run this, for the same
    repository directory, it should work fine.
    """

    git_dir = join(repositories_dir, project_name + '-git')
    bzr_dir = join(repositories_dir, project_name + '-bzr')
    git_url = 'git@github.com:{0}/{1}.git'.format(git_user, project_name)
    bzr_url = 'lp:~bzr-sync/{0}/trunk'.format(project_name)

    logger = Logger()

    # Clone the git repo, or pull if it exists
    if not isdir(git_dir):
        logger.update(
            "Cloning " + git_url,
            git.clone(git_url, git_dir)
        )
    else:
        logger.update(
            "Pulling {0} changes".format(project_name),
            git('-C', git_dir, 'pull')
        )

    # Always delete and recreate the bzr repo
    logger.update(
        "Removing bzr dir {0}".format(bzr_dir),
        rm(bzr_dir, r=True, f=True)
    )

    logger.update(
        "Creating BZR repo",
        bzr('init-repo', bzr_dir)
    )

    # Update the BZR repo with commits from git
    cd(bzr_dir)
    logger.update(
        "Updating BZR repo",
        bzr(
            git('-C', git_dir, 'fast-export', M=True, all=True),
            'fast-import', '-'
        )
    )

    logger.update(
        "Pushing BZR changes",
        bzr.push(bzr_url, overwrite=True, directory='trunk')
    )

    return logger.log
