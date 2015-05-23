from fabric.api import *
from fabric.contrib.files import exists


LOCAL_DIR = "/tmp/metaltrenches_deploy/"

env.user = "www-data"
env.webroot = "/www/metaltrenches/"
env["disable_known_hosts"] = True

app_name = "metaltrenches"
app_path = "/www/{app_name}".format(app_name=app_name)
app_venv_source = "/var/venvs/{app_name}/bin/activate".format(app_name=app_name)
app_settings = "metaltrenches.settings.local"


@hosts(["metaltrenches.local"])
def install():
    cmd = "cd {app_path} && " \
          "source {app_venv_source} && " \
          "pip install -r requirements.txt && " \
          "npm install"
    args = dict(app_path=app_path, app_venv_source=app_venv_source)
    run(cmd.format(**args))


@hosts(["metaltrenches.local"])
def migrate():
    cmd = "cd {app_path} && " \
          "source {app_venv_source} && " \
          "python manage.py migrate --settings {app_settings} --noinput"
    args = dict(app_path=app_path, app_venv_source=app_venv_source, app_settings=app_settings)
    run(cmd.format(**args))


@hosts(["metaltrenches.local"])
def reindex():
    cmd = "cd {app_path} && " \
          "source {app_venv_source} && " \
          "python manage.py reindex --settings {app_settings}"
    args = dict(app_path=app_path, app_venv_source=app_venv_source, app_settings=app_settings)
    run(cmd.format(**args))


@hosts(["metaltrenches.local"])
def test():
    cmd = "cd {app_path} && " \
          "source {app_venv_source} && " \
          "python manage.py test --settings {app_settings}"
    args = dict(app_path=app_path, app_venv_source=app_venv_source, app_settings=app_settings)
    run(cmd.format(**args))


@hosts(["metaltrenches.local"])
def collectstatic():
    cmd = "cd {app_path} && " \
          "source {app_venv_source} && " \
          "python manage.py collectstatic --settings {app_settings} --noinput"
    args = dict(app_path=app_path, app_venv_source=app_venv_source, app_settings=app_settings)
    run(cmd.format(**args))


@hosts(["metaltrenches.local"])
def reload():
    ini_path = "/etc/uwsgi-emperor/vassals/{app_name}.ini".format(app_name=app_name)
    if exists(ini_path):
        run("touch {ini_path}".format(ini_path=ini_path))
