"""Default datasets included with borg_parser"""

import pkg_resources


def water_energy():
    """
    Water/Energy trade-off dataset

    Returns
    -------
    stream : _io.BufferedReader
        Stream of trade-off dataset
    """
    stream = pkg_resources.resource_stream(__name__, 'example_runtime/water_energy.txt')
    return stream
