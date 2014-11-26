# Core
from os.path import abspath, dirname, join

# Modules
from wsgiref.simple_server import make_server
from sh import ErrorReturnCode

# Local
from wsgi_helpers import query_params
from bzr_sync import sync_git_to_bzr
from error_handlers import email_sh_error
from settings import auth_token, error_email_recipients, error_email_sender


def application(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    output = ""

    params = query_params(environ)

    token = params.get('token', '')
    bzr_url = params.get('bzr_url')
    git_url = params.get('git_url')

    if token == auth_token:
        if bzr_url:
            try:
                output = sync_git_to_bzr(
                    git_url=git_url,
                    bzr_url=bzr_url
                )
            except ErrorReturnCode as error:
                email_sh_error(
                    sh_error=error,
                    email_dir=join(dirname(abspath(__file__)), 'errors'),
                    sender_email=error_email_sender,
                    recipient_emails=error_email_recipients,
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

if __name__ == "__main__":
    httpd = make_server('', 9052, application)
    print "Serving on port 9052..."
    httpd.serve_forever()