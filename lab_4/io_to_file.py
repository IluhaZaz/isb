import json

from logging import Logger
from typing import Dict


class FileHandler:

    @staticmethod
    def read_bytes(file: str, logger: Logger) -> bytes:

        """Read bytes from file"""

        res = b''
        try:
            with open(file, 'rb') as f:
                res = f.read()
        except:
            logger.critical("Can't open input file")
        return res


    @staticmethod
    def write_bytes(path: str, text: bytes, logger: Logger) -> None:

        """Writes bytes to file"""

        try:
            with open(path, "wb") as file:
                file.write(text)
        except Exception:
            logger.critical("Can't open output json file")


    @staticmethod
    def read_file(file: str, logger: Logger) -> str:

        """Reads data from file"""

        res = ""
        try:
            with open(file, mode = "r", encoding = "utf-8") as f:
                res = f.read()
        except:
            logger.critical("Can't open input file")
        return res


    @staticmethod
    def write_to_file(file: str, text: str, logger: Logger) -> None:

        """Writes data to file"""

        try:
            with open(file, mode = "w", encoding = "utf-8") as f:
                f.write(text)
        except:
            logger.critical("Can't open output file")


    @staticmethod
    def write_to_json(d: Dict[str, str], file: str, logger: Logger) -> None:

        """Writes data to json"""

        try:
            with open(file, mode = "w", encoding = "utf-8") as f:
                json.dump(d, f, ensure_ascii = False, indent=4)
        except:
            logger.critical("Can't open output json file")


    @staticmethod
    def read_json(file: str, logger: Logger) -> Dict[str, str]:

        """Reads data from json"""

        try:
            with open(file, mode = "r", encoding = "utf-8") as f:
                return json.loads(f.read())
        except:
            logger.critical("Can't open input json file")
            return {}
    