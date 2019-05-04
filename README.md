***Deprecated and archived***

*We no longer use this, and it is no longer actively maintained.*

---

Bazaar Sync
===

A light python script and WSGI server application for synchronizing [Github](https://github.com) projects (in [Git](http://git-scm.com)) to [Launchpad](https://launchpad.net) (in [Bazaar](http://bazaar.canonical.com/en/)).

Setup
---

Once you've [cloned this repository](http://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository#Cloning-an-Existing-Repository), do the following:

``` bash
sudo apt install python-pip         # Install python and pip
pip install -r requirements.txt     # Install python dependencies
cp example-settings.py settings.py  # Create your settings file
```

Now customise `settings.py` with an auth-token, perhaps generated with `uuidgen`:

``` bash
auth_token = '{a-long-random-string}'
```

You then need to make sure the user who will be running this project has read access to any Github and write access to any Launchpad projects which you want to synchronise.

To make sure the user is setup with the correct configs and permissions to smoothly access Github and Launchpad without any user input, try doing the following manually before continuing:

- `git clone` a repository which you will want to sync
- `bzr branch` a repository which you will want to sync
- `bzr push :parent` from the `branch`ed repository, to make sure you can update repositories properly

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

### Serving with gunicorn

Gunicorn is a fully-fledged HTTP server. For any serious use, you probably want to run this service using `gunicorn`
 or a similar server.

*NB:* For non-local usage you should serve the app over HTTPS by providing the `--keyfile` and `--certfile` options to `gunicorn` - this will keep your `{auth-token}` secure.

``` bash
gunicorn --keyfile {path-to-keyfile} --certfile {path-to-certfile} -b 0.0.0.0:{port} wsgi:application
```
