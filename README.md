Bazaar Sync
===

A light python script and WSGI server application for synchronizing github projects (in git) to launchpad (in bzr).

Setup
---

You should set the settings at the top of `server.py`:

``` bash
auth_token = '{a-long-random-string}'
git_user = '{the-github-account}'
error_email_recipient = '{your-email-address}'
error_email_sender = '{whatever-you-like}'
```

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
