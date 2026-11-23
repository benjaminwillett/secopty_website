"""Production entry point: refuses to start with an unsafe configuration.

    waitress-serve --listen=127.0.0.1:8080 --threads=8 --trusted-proxy=127.0.0.1
        --trusted-proxy-headers="x-forwarded-for x-forwarded-proto x-forwarded-host"
        --clear-untrusted-proxy-headers wsgi:app          (one command line)

waitress removes X-Forwarded-* headers from untrusted peers, so behind a reverse proxy
the --trusted-proxy flags are required (with NETOPTY_TRUST_PROXY=1) for HTTPS detection
and the per-visitor rate limit. Use a single waitress process: the rate limit is in memory.
"""
import logging
import sys

from server import create_app, env_config, production_problems

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")

_problems = production_problems(env_config())
if _problems:
    for p in _problems:
        logging.getLogger("netopty_site").error("configuration: %s", p)
    sys.exit("Netopty site: refusing to start with an unsafe configuration (see the log above).")

app = create_app()
if not env_config()["SMTP_HOST"]:
    logging.getLogger("netopty_site").warning(
        "NETOPTY_SMTP_HOST is not set: the enquiry form will tell visitors their message was not sent")
