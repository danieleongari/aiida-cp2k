from .atomic_convention1 import spin, basis_set, pseudo
from aiida.orm.data.parameter import ParameterData
from aiida.work import workfunction as wf

def dict_merge(dct, merge_dct):
    """ Taken from https://gist.github.com/angstwad/bf22d1822c38a92ec0a9
    Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
    updating only top-level keys, dict_merge recurses down into dicts nested
    to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
    ``dct``.
    :param dct: dict onto which the merge is executed
    :param merge_dct: dct merged into dct
    :return: None
    """
    import collections
    for k, v in merge_dct.iteritems():
        if (k in dct and isinstance(dct[k], dict)
                and isinstance(merge_dct[k], collections.Mapping)):
            dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]

def get_atom_kinds(structure):
    kinds = []
    all_atoms = set(structure.get_ase().get_chemical_symbols())
    for a in all_atoms:
        kinds.append({
            '_': a,
            'BASIS_SET': basis_set[a],
            'POTENTIAL': pseudo[a],
            'MAGNETIZATION': spin[a] * 2.0,
            })
    return kinds

default_options = {
    "resources": {
        "num_machines": 1,
        "num_mpiprocs_per_machine": 1,
    },
    "max_wallclock_seconds": 1 * 60 * 60,
    }

empty_pd = ParameterData(dict={}).store()

disable_printing_charges_dict = {
    'FORCE_EVAL': {
        'DFT': {
            'PRINT':{
                'MULLIKEN': {
                    '_': 'OFF',
                    },
                'LOWDIN': {
                    '_': 'OFF',
                    },
                'HIRSHFELD': {
                    '_': 'OFF',
                    },
                },
            },
        },
    }

@wf
def merge_ParameterData(p1, p2):
    p1_dict = p1.get_dict()
    p2_dict = p2.get_dict()
    dict_merge(p1_dict, p2_dict)
    return ParameterData(dict=p1_dict).store()
