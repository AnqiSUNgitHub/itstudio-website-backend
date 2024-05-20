
from os import getenv
from django.conf import settings


def init_by(settings_, key):
    "do nothing if env `key` is not set."
    val = getenv(key)
    if val is not None:
        settings_.configure(**{key: val})


def chk_init_by(settings_, key):
    "Raises OSError if env `key` is not set."
    val = getenv(key)
    if val is not None:
        settings_.configure(**{key: val})
    else:
        raise OSError("the envvar '"+key+"' is not set, cannot send email")


chk_init_envs = [
    "EMAIL_HOST_PASSWORD",

]

init_envs = [
    "DEBUG",

]


def init():
    for k in chk_init_envs: chk_init_by(settings, k)
    for k in init_envs: chk_init_by(settings, k)
