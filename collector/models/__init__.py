from .candidacies import setup_index as candidacies
from .cities import setup_index as cities
from .political_parties import setup_index as political_parties


def setup(years):
    "Setup all indexes & templates that ES needs to work"
    candidacies()
    cities()
    political_parties()
