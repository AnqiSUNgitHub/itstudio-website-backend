
from os import getenv, pathsep
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

def parse_bool(s):
    "returns None if fails"
    sl = s.lower()
    if sl == "true":
        return True
    elif sl == "false":
        return False

def parse_bool_like(val) -> bool:
    err = "bool or 1/0 expected, but got {}"
    def err():
        raise ValueError(err.format(val))
    le = len(val)
    if le == 0:
        err()
    if val[0] in {'t', 'T', 'f', 'F'}:
        # might be bool
        b = parse_bool(val)
        if b is None:
            err()
        res = b
    else:
        if le != 1:
            err()
        c = le[0]
        if c == '1': return True
        if c == '0': return False
        err()


DEBUG_ENV = "WEBSITE_DEBUG"
def init_debug(settings_):
    """get env WEBSITE_DEBUG.
    if true, then get ALLOWED_HOSTS, use os.pathsep split it.
    
    may raise OSError"""
    key = DEBUG_ENV
    val = getenv(key)
    if val is None:
        return
    debug = parse_bool_like(val)
    settings_.configure(**dict(DEBUG=debug))
    if debug:
        return
    hosts_env = 'ALLOWED_HOSTS'
    hosts_s = getenv(hosts_env)
    def err():
        raise OSError("if not DEBUG, you must set "+hosts_env)

    if hosts_s is None:
        err()
    hosts = hosts_s.split(pathsep)

    settings_.configure(ALLOWED_HOSTS=hosts)


chk_init_envs = [
    "EMAIL_HOST_PASSWORD",

]

init_envs = [

]


def init():
    init_debug(settings)
    for k in chk_init_envs: chk_init_by(settings, k)
    for k in init_envs: chk_init_by(settings, k)
