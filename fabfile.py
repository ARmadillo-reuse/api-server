from __future__ import with_statement
from fabric.api import env, settings, local, run, cd, abort
from fabric.contrib.console import confirm

env.hosts = ['armadillo.xvm.mit.edu']

def test():
    with settings(warn_only=False):
        result = local('"./manage.py" test' )
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
    code_dir = "/home/armadillo/server-%s"%("stable" if stable else "unstable")
    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            git_origin = "https://github.com/ARmadillo-reuse/api-server.git"
            run("git clone %s %s" % (git_origin, code_dir))
            
    with cd(code_dir):
        run("git pull origin %s" % branch)
        local("python manage.py migrate %s" % app)
        local("python manage.py test")