import logging

_logger = logging.getLogger(__file__)


def call_warn(*args, **kwargs):
    _logger.warn(*args, **kwargs)

def call_fatal(*args, **kwargs):
    _logger.fatal(*args, **kwargs)
