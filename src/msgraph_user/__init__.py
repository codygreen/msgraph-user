# read version from installed package
from importlib.metadata import version
from .msgraph_user import GraphUser
__version__ = version("msgraph_user")