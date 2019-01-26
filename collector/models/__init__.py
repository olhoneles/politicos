from .candidacies import setup_index as candidacies
from .politicians import setup_index as politicians, setup_index_template
from .cities import setup_index as cities
from .political_parties import setup_index as political_parties


def setup(years):
    "Setup all indexes & templates that ES needs to work"
    candidacies()
    for y in years:
        politicians(y)
    setup_index_template()
    cities()
    political_parties()
