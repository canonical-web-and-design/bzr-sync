# Core
from os.path import abspath, dirname, join
from wsgiref.simple_server import make_server
from urllib import unquote

# Modules
import sh

# Local
import settings
from wsgi_helpers import query_params
from bzr_sync import sync_git_to_bzr
from error_handlers import email_sh_error


def application(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    output = ""

    params = query_params(environ)

    token = unquote(params.get('token', ''))
    bzr_url = unquote(params.get('bzr_url', ''))
    git_url = unquote(params.get('git_url', ''))

    if token == settings.auth_token:
        if bzr_url:
            try:
                output = sync_git_to_bzr(
                    git_url=git_url,
                    bzr_url=bzr_url
                )
            except sh.ErrorReturnCode as error:
                if 'error_email_recipients' in dir(settings):
                    email_sh_error(
                        sh_error=error,
                        email_dir=join(dirname(abspath(__file__)), 'errors'),
                        sender_email=settings.error_email_sender,
                        recipient_emails=settings.error_email_recipients,
                        subject="BZR Sync error syncing {0} to {1}".format(
                            git_url,
                            bzr_url
                        )
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
