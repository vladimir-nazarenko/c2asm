# Simple script to deploy static files to server
# see http://stackoverflow.com/questions/19053399/how-to-deploy-static-files-to-a-separated-machine
# usage: fab deploy_static

from fabric.api import *
from fabric.contrib import project

# Remote host
env.roledefs['static'] = ['developer@188.226.145.132']    

# Where the static files get collected locally. Your STATIC_ROOT setting.
env.local_static_root = '/var/www/html/c2asm.com'

# Where the static files should go remotely
env.remote_static_root = '/var/www/html'

@roles('static')
def deploy_static():
    local('../manage.py collectstatic')
    project.rsync_project(
        remote_dir = env.remote_static_root,
        local_dir = env.local_static_root,
        delete = True
    )
