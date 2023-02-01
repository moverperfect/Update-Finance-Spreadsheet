import os
import json


def read_secrets() -> dict:
    """Read secrets from secrets.json and return dictionary"""
    filename = os.path.join("secrets.json")
    try:
        with open(filename, mode="r", encoding="UTF-8") as filereader:
            return json.loads(filereader.read())
    except FileNotFoundError:
        return {}
