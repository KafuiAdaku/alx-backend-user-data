#!/usr/bin/env python3
"""Logging module"""
import logging
from typing import List
import mysql.connector
import os
import re
from typing import List


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    returns the log message obfuscated

    Args:
        fields: a list of strings representing all fields to obfuscate
        redaction: a string representing by what the field will be obfuscated
        message: a string representing the log line
        separator: a string representing by which character is
                   separating all fields in the log line (message)

    Returns: the log message obfuscated
    """
    for field in fields:
        message = re.sub(rf"{field}=.+?{separator}",
                         f"{field}={redaction}{separator}", message)
    return message


def get_logger() -> logging.Logger:
    """
    returns a logging object
    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    stream.setFormatter(formatter)
    logger.addHandler(stream)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    returns a connector to the database
    """
    return mysql.connector.connect(
        user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=os.getenv('PERSONAL_DATA_DB_NAME')
    )


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        filter values in incoming log records using filter_datum
        """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)
