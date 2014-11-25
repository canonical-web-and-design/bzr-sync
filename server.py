# Core
from os.path import abspath, dirname, join

# Modules
from wsgiref.simple_server import make_server
from sh import ErrorReturnCode

# Local
from wsgi_helpers import query_params
from bzr_sync import sync_git_to_bzr
from error_handlers import email_sh_error

# Options
auth_token = 'AUTH-TOKEN'
github_user = 'GIT-USER-ACCOUNT'
launchpad_user = 'BZR-USER-ACCOUNT'
error_email_recipient = 'YOUR_EMAIL'
error_email_sender = 'SENDING_EMAIL'

base_dir = dirname(abspath(__file__))


def application(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    output = ""

    params = query_params(environ)

    token = params.get('token', '')
    launchpad_branch = params.get('launchpad_h', 'trunk')
    project_name = params.get['project']
    launchpad_project_name = params.get('launchpad-project', project_name)

    if token == auth_token:
        if project_name:
            try:
                output = sync_git_to_bzr(
                    project_name=project_name,
                    launchpad_project_name=launchpad_project_name,
                    github_user=github_user,
                    launchpad_user=launchpad_user,
                    repositories_dir=join(base_dir, 'repositories'),
                    launchpad_branch=launchpad_branch
                )
            except ErrorReturnCode as error:
                email_sh_error(
                    sh_error=error,
                    email_dir=join(base_dir, 'errors'),
                    sender_email=error_email_sender,
                    recipient_email=error_email_recipient,
                    subject="BZR Sync error with {0}".format(params['project'])
                )
                raise error
        else:
            status = '400 Bad Request'
            output = "project_name not provided"
    else:
        status = '401 Unauthorized'
        output = "Invalid authorization token"

    start_response(status, headers)

    return [output]

httpd = make_server('', 9052, application)
print "Serving on port 9052..."
httpd.serve_forever()
