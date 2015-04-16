from functools import wraps
from flask import Response, request
import ldap
from cciscloud.config import LDAP_URI


def check_user(username, password):
    return True
    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
    ldap.set_option(ldap.OPT_X_TLS_DEMAND, True)
    conn = ldap.initialize(LDAP_URI)
    try:
        conn.start_tls_s()
        bind_val = conn.simple_bind_s("uid=%s,ou=People,dc=ccs,dc=neu,dc=edu" % username, password)
        if bind_val:
            return True
    except ldap.LDAPError, e:
        print e.message
    finally:
        conn.unbind()
    return False


def authenticate():
    return Response('Please login with your CCIS credentials', 401, {'WWW-Authenticate': 'Basic realm="CCIS Login"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_user(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
