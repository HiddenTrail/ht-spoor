"""Complete an address typed without http:// or https://, the way a browser does.

People type `localhost:3000` or `shop.example/sale`. A browser quietly adds the
scheme, but the rest of Spoor needs a real URL: the map store files a map under
the URL's host, the sandbox check recognises a local target from it, and a saved
login is found by it. Without a scheme none of those can find the host (a map is
then filed under an empty site name, and a local target isn't recognised as
local). So the commands that take an address complete it first.

The choice is generic (§0), decided by the host alone: this computer and private
network addresses (`localhost`, `*.localhost`, loopback and private IPs, and
single-word intranet names) get `http://`, since local servers rarely serve
HTTPS. Every other host gets `https://`. An address that already names a scheme
is returned unchanged.
"""

from __future__ import annotations

import ipaddress
from urllib.parse import urlsplit

#: Hostname endings that only exist on a local machine or network.
_LOCAL_SUFFIXES = (".localhost", ".local", ".internal", ".lan", ".home.arpa")


def _is_local(host: str) -> bool:
    if host == "localhost" or host.endswith(_LOCAL_SUFFIXES):
        return True
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        # A hostname: a single word (no dot) is an intranet name, never public.
        return "." not in host
    return address.is_loopback or address.is_private or address.is_link_local


def complete_address(address: str) -> str:
    """`address` with a scheme: unchanged if it has one, else http:// or https://.

    Empty input is returned as is, for the caller to report as missing.
    """
    address = address.strip()
    if not address or "://" in address:
        return address
    host = (urlsplit("//" + address).hostname or "").lower()
    scheme = "http" if _is_local(host) else "https"
    return f"{scheme}://{address}"
