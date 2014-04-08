from __future__ import with_statement
from fabric.api import env, settings, local, run, cd, abort, prefix
from fabric.contrib.console import confirm
from fabric.exceptions import CommandTimeout

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

def deploy(state="unstable",app="web_api"):
    stable = state == "stable"
    branch = "master" if stable else "unstable"
    environment = "server-" + ("stable" if stable else "unstable")
    message = "Deploying branch %s to %s" % (branch, environment)
    print "======================================================"
    print ("==    %s  ==" % message.ljust(42))
    print "======================================================"
    code_dir = "/home/armadillo/%s" % environment

    with cd(code_dir):
        with prefix('WORKON_HOME=$HOME/.virtualenvs'):
            with prefix('source /usr/local/bin/virtualenvwrapper.sh'):
                with prefix('workon %s' % environment):
                    print "Updating remote code"
                    run("git pull origin %s" % branch)
                    print "Migrating database"
                    run("python manage.py migrate %s" % app)
                    print "Running tests"
                    run("python manage.py test")
                    print "Starting SMTP relay client"
                    try:
                        run("./smtp/client_server.sh", pty=False, timeout=2)
                    except CommandTimeout:
                        pass

        print "Restarting web server"
        run("touch armadillo_reuse/wsgi.py")

        print "======================================================"
        print "==                   All done!                      =="
        print "======================================================"
