"""
php serialize / unserialize implementation in Python
http://code.google.com/p/php-serialize/
"""
try:
    from _speedups import serialize, unserialize, PHP_Class
#except (ImportError, AttributeError):
except ImportError:
    from core import serialize, unserialize, PHP_Class
