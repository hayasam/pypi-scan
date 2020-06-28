"""
Utility functions that perform actions related to typosquatting

These are the important misfits. They don't fit in elsewhere but these
functions need to be in a module somewhere.
"""

import collections
import os
import time

import json
from mrs_spellings import MrsWord

import constants
from filters import distance_calculations

MAX_DISTANCE = constants.MAX_DISTANCE


def create_suspicious_package_dict(
    all_packages, top_packages, max_distance=MAX_DISTANCE
):
    """Examine all top packages for typosquatters.

	Loop through all top packages and check for instances of
	typosquatting.

	INPUTS:
	--all_packages: list of all package names
	--top_package: package name to perform comparison
	--max_distance: maximum edit distance to check for typosquatting

	OUTPUTS:
	--suspicious_packages: an ordered dict of the top packages (key)
	and potential typosquatters (value)
	"""
    suspicious_packages = collections.OrderedDict()

    for top_package in top_packages:
        close_packages = distance_calculations(top_package, all_packages, max_distance)
        suspicious_packages[top_package] = close_packages

    return suspicious_packages


def store_squatting_candidates(squat_candidates):
    """Persist results of squatting candidate search.

	Dump typosquatter candidate list to a json file. Store
	with time-stamped file name to results folder.

	INPUT:
	--squat_candidates: A dic of the top packages and their
	potential typosquatters
	"""

    timestamp = time.strftime("%d-%b-%Y-%H-%M-%S", time.localtime())
    full_file_name = timestamp + "-record" + ".json"
    file_name = os.path.join("results", full_file_name)
    with open(file_name, "w") as path:
        json.dump(squat_candidates, path)


def create_potential_squatter_names(module_name):
    """Create a set of potential typosquatting names

	Given a module name, create a set of potential typosquatting
	names based on qwerty distance, a measure of how close keys
	are to each other. This is a more sophisticated measure of
	keyboard key distance than levenshtein distance.

	INPUT:
	--module_name: a name for a module

	OUTPUT:
	--potential_squatter_set: a list of potential typosquatting name
	"""

    potential_candidates = MrsWord(module_name).qwerty_swap()
    potential_candidates_joined = " ".join(potential_candidates)
    potential_candidates_set = set(potential_candidates_joined.split(" "))
    return potential_candidates_set
