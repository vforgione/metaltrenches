from fabric.api import *
from fabric.contrib.files import exists

env.user = 'www-data'
env.webroot = '/www/metaltrenches/'
env['disable_known_hosts'] = True

app_name = 'metaltrenches'
app_path = '/www/{app_name}'.format(app_name=app_name)
app_venv_source = '/var/venvs/{app_name}/bin/activate'.format(app_name=app_name)
app_settings = 'metaltrenches.settings.vagrant'

vagrant_host = 'metaltrenches.local'


@hosts([vagrant_host])
def pip_install():
    cmd = 'cd {app_path} && ' \
          'source {app_venv_source} && ' \
          'pip install -U -r requirements.txt'
    kwargs = dict(app_path=app_path, app_venv_source=app_venv_source)
    run(cmd.format(**kwargs))


@hosts([vagrant_host])
def npm_install():
    cmd = 'cd {app_path} && ' \
          'npm install'
    kwargs = dict(app_path=app_path)
    run(cmd.format(**kwargs))


@hosts([vagrant_host])
def bower_install():
    cmd = 'cd {app_path} && ' \
          'bower install'
    kwargs = dict(app_path=app_path)
    run(cmd.format(**kwargs))


@hosts([vagrant_host])
def install():
    pip_install()
    npm_install()
    bower_install()


@hosts([vagrant_host])
def make_migrations():
    cmd = 'cd {app_path} && ' \
          'source {app_venv_source} && ' \
          'python manage.py makemigrations --settings {app_settings}'
    kwargs = dict(app_path=app_path, app_venv_source=app_venv_source, app_settings=app_settings)
    run(cmd.format(**kwargs))


@hosts([vagrant_host])
def migrate():
    cmd = 'cd {app_path} && ' \
          'source {app_venv_source} && ' \
          'python manage.py migrate --settings {app_settings} --noinput'
    kwargs = dict(app_path=app_path, app_venv_source=app_venv_source, app_settings=app_settings)
    run(cmd.format(**kwargs))


@hosts([vagrant_host])
def create_superuser():
    cmd = 'cd {app_path} && ' \
          'source {app_venv_source} && ' \
          'python manage.py createsuperuser --settings {app_settings}'
    kwargs = dict(app_path=app_path, app_venv_source=app_venv_source, app_settings=app_settings)
    run(cmd.format(**kwargs))


@hosts([vagrant_host])
def test():
    cmd = 'cd {app_path} && ' \
          'source {app_venv_source} && ' \
          'python manage.py test --settings {app_settings}'
    kwargs = dict(app_path=app_path, app_venv_source=app_venv_source, app_settings=app_settings)
    run(cmd.format(**kwargs))


@hosts([vagrant_host])
def collect_static():
    cmd = 'cd {app_path} && ' \
          'source {app_venv_source} && ' \
          'python manage.py collectstatic --settings {app_settings} --noinput'
    kwargs = dict(app_path=app_path, app_venv_source=app_venv_source, app_settings=app_settings)
    run(cmd.format(**kwargs))


@hosts([vagrant_host])
def flush_cache():
    run("echo 'flush_all' | nc localhost 11211")


@hosts([vagrant_host])
def restart_uwsgi():
    ini_path = '/etc/uwsgi-emperor/vassals/{app_name}.ini'.format(app_name=app_name)
    if exists(ini_path):
        run('touch {ini_path}'.format(ini_path=ini_path))


@hosts([vagrant_host])
def reload():
    flush_cache()
    restart_uwsgi()
