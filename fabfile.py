from __future__ import with_statement
from fabric.api import env, settings, local, run, cd, abort, prefix
from fabric.contrib.console import confirm

env.hosts = ['armadillo@armadillo.xvm.mit.edu']

def test():
    with settings(warn_only=False):
        result = local('"./manage.py" test')
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")

def commit():
    local("git add -p && git commit")

def push():
    local("git push")

def prepare_deploy():
    test()
    commit()
    push()

def deploy(app="web_api", stable=False):
    branch = "master" if stable else "dev"
    environment = "server-" + ("stable" if stable else "unstable")
    code_dir = "/home/armadillo/%s" % environment

    with prefix('WORKON_HOME=$HOME/.virtualenvs'):
        with prefix('source /usr/local/bin/virtualenvwrapper.sh'):
            with prefix('workon %s' % environment):
                with cd(code_dir):
                    run("git pull origin %s" % branch)
                    run("python manage.py migrate %s" % app)
                    run("python manage.py test")