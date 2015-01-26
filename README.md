Bazaar Sync
===

A light python script and WSGI server application for synchronizing github projects (in git) to launchpad (in bzr).

Setup
---

You create a settings file at `settings.py` containing:

``` bash
auth_token = '{a-long-random-string}'
error_email_recipients = '{comma-separated-email-addresses}'
error_email_sender = '{whatever-you-like}'
```

Example settings are contained in [example.settings.py](example.settings.py).

Usage
---

You can run the simple WSGI server:

``` bash
$ python wsgi.py
Serving on port 9052...
```

And then trigger the script to sync github projects to launchpad  by visiting:

```
http://0.0.0.0:9052/?token={auth-token}&git_url={git-ssh-url}&bzr_url={bzr-host-url}
```

This will attempt to synchronise `{git_user}` (e.g. `git@github.com/username/repository`) to `{bzr_url}`(e.g. `lp:your-project`).

NB: The user that runs the server must have permission to access both the github and launchpad repositories.

Serving with gunicorn
---

Gunicorn is a fully-fledged HTTP server. If you want to use Gunicorn instead of pure WSGI:

``` bash
gunicorn -b 0.0.0.0:9052 wsgi:application
```

NB: You should really serve the app over HTTPS by providing the `--keyfile` and `--certfile` options to `gunicorn` - this will keep your `{auth-token}` secure.
