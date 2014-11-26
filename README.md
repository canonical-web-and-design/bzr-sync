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
$ python server
Serving on port 9052...
```

And then trigger the script to sync github projects to launchpad  by visiting:

```
http://0.0.0.0:9052/?token={auth-token};project={your-project}
```

This will attempt to synchronise `git@github.com:{git_user}/{your-project}` to `lp:{your-project}`.

NB: The user that runs the server must have permission to access both the github and launchpad repositories.

Serving with gunicorn
---

Gunicorn is a fully-fledged HTTP server. If you want to use Gunicorn instead of pure WSGI:

``` bash
gunicorn -b 0.0.0.0:9052 wsgi:application
```
