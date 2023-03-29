import os
import imp

from .auth_sys import require_auth


def load_from(directory, flask_app, **special_references):
    "Load url-rules from <directory> and append rules to <flask.app>."

    # Make sure we're in flask-app directory.
    os.chdir(flask_app.root_path)

    # Walk through <directory> and look for *.py files.
    for path, dirs, files in os.walk(directory):
        for file in files:
            if not file.endswith('.py'):
                continue

            # Load *.py files as python modules.
            file_path = os.path.join(path, file)
            mod = imp.load_source(file.rstrip('.py'), file_path)

            # If there isn't any <get> or <post> function in <mod>, drop it!
            # Else, the module contains instructions for routing HTTP requests.
            if not 'get' in dir(mod) and not 'post' in dir(mod):
                continue

            # Work on the url-rule that'll be appended to the app url-rule-map.
            # We need two information, a URL and a `view function`...

            # A rule's url is its file-path in <directory>, unless <mod> has
            # the special <alt_path> variable defined.
            if 'alt_path' in dir(mod):
                url = os.path.join(path, mod.alt_path)
            else:
                url = os.path.join(path, file.rpartition('.py')[0])

            url = url.lstrip(directory)        \
                     .replace('__root__', '/') \
                     .replace('\\', '/')       \
                     .replace('//', '/')

            # Now, start building the `view function`...
            # The view function must have a name, we'll use the rule's own URL.
            # NOTE: we cannot just simply <url> for the view function name
            #       since it can contain some special flask routing variables.
            name = os.path.join(path, file)     \
                .rpartition('.py')[0]    \
                .replace('\\', '/')      \
                .replace('__root__', '') \
                .lstrip(directory)

            # View functions can require certain authentication to
            # allow/disallow some clients from accessing the url-content.
            # Firstly, we need to read the defined <requires> variable and
            # prepare a list of 'required authentication keys' to be used by
            # the auth-sys.
            if 'requires' in dir(mod):
                if type(mod.requires) == tuple or type(mod.requires) == list:
                    req = mod.requires
                else:
                    req = (mod.requires,)
            else:
                req = ()

            # Now, create the view functions by wrapping <mod>'s own <get> and
            # <post> functions using <core.authentication_system.require_auth>.
            if 'get' in dir(mod):
                get = require_auth(req, mod.get)
            if 'post' in dir(mod):
                post = require_auth(req, mod.post)

            # We've built the view functions, time to add the url-rule!
            # NOTE: since we can't have two view functions with the same name
            #       we'll append a special ':p' string to the post-view-function
            #       name to distinguish it from the get-view-function.
            if 'get' in dir(mod):
                flask_app.add_url_rule(url, name, get, methods=['GET'])
            if 'post' in dir(mod):
                flask_app.add_url_rule(
                    url, name + ':p', post, methods=['POST'])

            # Finally, pass some `special references` to <mod> to allow the
            # <get> and <post> functions to use them; we'll append these
            # references from the passed dict <special_references> to the
            # module's own globals.
            mod.__dict__.update(special_references)

    return
