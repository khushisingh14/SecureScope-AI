from .burp import parse_burp
from .nikto import parse_nikto
from .nmap import parse_nmap
from .sslyze import parse_sslyze


PARSERS = {
    "nmap": parse_nmap,
    "burp": parse_burp,
    "nikto": parse_nikto,
    "sslyze": parse_sslyze,
}
