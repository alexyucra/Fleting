from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("fleting")
except PackageNotFoundError:  # rodando do código-fonte sem instalar
    __version__ = "0.0.0-dev"