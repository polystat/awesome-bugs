import logging
import os

FILTER_FILE_NAME = "filters.txt"
GLOBAL_FILTER_PATH = "global_filters.txt"


def read_sample_filters(sample_path):
    try:
        with open(os.path.join(sample_path, FILTER_FILE_NAME), "r") as f_file:
            return f_file.read().split("\n")
    except Exception as e:
        logging.info("Didn't find filters for '{}'".format(sample_path))
        return []


def read_global_filters():
    res = []

    try:
        with open(GLOBAL_FILTER_PATH, "r") as f_file:
            res = f_file.read().split("\n")
    except Exception as e:
        logging.info("Didn't global_filters '{}'".format(sample_path))
        return []

    logging.info("global_filters are '{}'".format(str(res)))
    return res
