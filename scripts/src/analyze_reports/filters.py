import logging
import os

FILTER_FILE_NAME = "filters.txt"
GLOBAL_FILTER_PATH = "global_filters.txt"


def read_sample_filters(sample_path):
    try:
        with open(os.path.join(sample_path, FILTER_FILE_NAME), "r") as f_file:
            return f_file.read().split("\n")
    except OSError:
        logging.info(f"Didn't find filters for '{sample_path}'")
        return []


def read_global_filters():
    try:
        with open(GLOBAL_FILTER_PATH, "r") as f_file:
            res = list(
                filter(
                    lambda fltr: len(fltr) > 0,
                    f_file.read().split("\n"),
                )
            )
    except OSError:
        logging.info(f"Didn't find global_filters at '{GLOBAL_FILTER_PATH}'")
        return []

    logging.info(f"global_filters are '{res}'")
    return res
