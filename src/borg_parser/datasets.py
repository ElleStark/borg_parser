"""Default datasets included with borg_parser
    May 2023 E Stark: added runtime file datasets for Borg-RW practice runs"""


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

def BorgRW_400fe_noC_8T():
    """
    Practice Borg-RW run trade-off dataset: random_DNF_8 traces as selected by Reclamation.
    All constraints removed
    Max function evaluations set to 400
    See: formulation_NoConstraints_400FEs.xml

    Returns
    -------
    stream : _io.BufferedReader
        Stream of trade-off dataset
    """
    stream = pkg_resources.resource_stream(__name__, 'T1_FE400_8Traces/RunTime.Parsable.txt')
    return stream

def BorgRW_400fe_noC_4T():
    """
    Practice Borg-RW run trade-off dataset: 4 Stress Test traces (trace 1, 10, 20, and 30)
    All constraints removed
    Max function evaluations set to 400
    See: formulation_NoConstraints_400FEs_StressTest4.xml

    Returns
    -------
    stream : _io.BufferedReader
        Stream of trade-off dataset
    """
    stream = pkg_resources.resource_stream(__name__, 'T2_FE400_4Traces_StressTest_noC/RunTime.Parsable.txt')
    return stream

def BorgRW_200fe_allC_8T():
    """
    Practice Borg-RW run trade-off dataset: 4 Stress Test traces (trace 1, 10, 20, and 30)
    All constraints removed
    Max function evaluations set to 400
    See: formulation_NoConstraints_400FEs_StressTest4.xml

    Returns
    -------
    stream : _io.BufferedReader
        Stream of trade-off dataset
    """
    stream = pkg_resources.resource_stream(__name__, 'T0_FE200_allC_8Traces/RunTime.Parsable.txt')
    return stream