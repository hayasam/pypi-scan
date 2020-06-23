""" Functions that group lower-level functions and represent separate code paths

These are the main related functionalities that can be called in main.py
"""

from filters import filter_by_package_name_len, whitelist
from scrapers import get_all_packages, get_top_packages
from utils import (
    create_suspicious_package_dict,
    store_squatting_candidates,
    create_potential_squatter_names,
)


def mod_squatters(module, max_distance):
    """ Check if a particular package name has potential squatters

    Prints any potential typosquatters for specified module

    INPUTS:
    module: name to check for typosquatting
    max_distance: maximum edit distance to check for typosquatting
    """

    module_in_list = [module]
    package_names = get_all_packages()
    squat_candidates = create_suspicious_package_dict(
        package_names, module_in_list, max_distance
    )
    # Print results
    print("Checking " + module + " for typosquatting candidates.")
    # Check for no typosquatting candidates
    if len(squat_candidates[module]) == 0:
        print("No typosquatting candidates found.")
    else:
        for i, candidate in enumerate(squat_candidates[module]):
            print(str(i) + ": " + candidate)


def names_to_defend(module_name):
    """ Print out module names that might merit defending

    INPUT:
    --module_name: Initial module name to protect from typosquatting
    """
    print(
        f'Here is a list of similar names--measured by keyboard distance--to "{module_name}":'
    )
    names = create_potential_squatter_names(module_name)
    for i, name in enumerate(names):
        print(f"{i}:", name)


def top_mods(max_distance, top_n, min_len, stored_json):
    """ Check top packages for typosquatters

    Prints top packages and any potential typosquatters

    INPUTS:
    max_distance: maximum edit distance to check for typosquatting
    top_n: the number of top packages to retrieve
    min_len: a minimum length of characters
    stored_json: a flag to denote whether to used stored top packages json
    """

    # Get list of potential typosquatters
    package_names = get_all_packages()
    top_packages = get_top_packages(top_n=top_n, stored=stored_json)
    filtered_package_list = filter_by_package_name_len(top_packages, min_len=min_len)
    squat_candidates = create_suspicious_package_dict(
        package_names, filtered_package_list, max_distance
    )
    post_whitelist_candidates = whitelist(squat_candidates)
    store_squatting_candidates(post_whitelist_candidates)

    # Print all top packages and potential typosquatters
    print("Number of top packages to examine: " + str(len(squat_candidates)))
    cnt_potential_squatters = 0
    for i in post_whitelist_candidates:
        print(i, ": ", post_whitelist_candidates[i])
        cnt_potential_squatters += len(post_whitelist_candidates[i])
    print("Number of potential typosquatters: " + str(cnt_potential_squatters))