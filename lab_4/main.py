import logging

from functions import find_number

from io_to_file import FileHandler


if __name__ == "__main__":

    logger = logging.getLogger(__name__)

    constants = FileHandler.read_json("constants.json", logger)

    find_number(constants["hash"], constants["last_4_nums"], constants["bins"], "card_number.txt", logger)