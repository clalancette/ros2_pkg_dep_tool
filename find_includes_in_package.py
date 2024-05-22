import argparse
import os
import sys
import time
from typing import List

import yaml


class Symbols:
    __slots__ = ('symbol_map', 'empty_token', 'namespace_depth')

    def __init__(self, symbol_map: dict, empty_token: str, namespace_depth: int):
        self.symbol_map = symbol_map
        self.empty_token = empty_token
        self.namespace_depth = namespace_depth


def find_type(single_token: str, symbol_map: Symbols) -> set:
    # In case this is just the empty namespace token, the actual type is
    # probably on thenext line.  Since this entire utility is line-oriented,
    # there is no good way to get that.  Just ignore these; we may drop an
    # include here or there, but it is really not a big deal.
    if single_token != symbol_map.empty_token:
        if single_token.startswith(symbol_map.empty_token):
            double_colon_split = single_token.split('::')
            # Only look up to the depth specified
            first = '::'.join(double_colon_split[:symbol_map.namespace_depth])
            if first not in symbol_map.symbol_map:
                print(first)
            else:
                if symbol_map.symbol_map[first]:
                    return set([symbol_map.symbol_map[first]])

    return set()


def search_for_namespaces(full_path: str, symbol_maps: List[Symbols]) -> None:
    print(full_path)
    include_set = set()

    lines = []
    with open(full_path, 'r') as infp:
        for line in infp:
            lines.append(line)

    # This is a 3-pass algorithm.
    # In the first pass, we look for all tokens with '::' in them, as that designates
    # some C++ construct that we need dependencies for.

    in_c_comment = False
    for line in lines:
        # Skip C++ style comment
        if line.lstrip().startswith('//'):
            continue

        if not in_c_comment:
            if line.lstrip().startswith('/*'):
                if not '*/' in line.lstrip():
                    in_c_comment = True
                continue
        else:
            if '*/' in line:
                in_c_comment = False
            continue

        # TODO(clalancette): Also skip when inside of strings?

        # TODO(clalancette): Also deal with 'using'

        if not '::' in line:
            continue

        commas = line.strip().replace('(', ',').replace(')', ',').replace('<', ',').replace('>', ',').replace(' ', ',').replace(';', ',').replace('{', ',').replace('}', ',').replace('&', ',').replace('...', ',')

        split = commas.split(',')
        for s in split:
            if not '::' in s:
                continue

            for symbol_map in symbol_maps:
                found_type = find_type(s, symbol_map)
                if found_type:
                    include_set = include_set.union(find_type(s, symbol_map))
                    break

    #print(include_set)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--types', nargs='+', required=False, default=[], help='A YAML file containing the types we should look for and produce while parsing')
    parser.add_argument('package_path', help='Path to the package to find dependencies for')

    options = parser.parse_args()

    symbol_maps = []
    for t in options.types:
        with open(t, 'r') as infp:
            data = yaml.safe_load(infp)
            symbol_map = {}
            if data['symbols'] is not None:
                for symbol in data['symbols']:
                    symbol_map[symbol['symbol_name']] = symbol['include']
            symbol_maps.append(Symbols(symbol_map, data['empty_token'], data['namespace_depth']))

    for (dirpath, dirnames, filenames) in os.walk(options.package_path):
        for f in filenames:
            extension = os.path.splitext(f)[1]
            if extension not in ('.cpp', '.cxx', '.cc', '.h', '.hpp'):
                continue

            search_for_namespaces(os.path.join(dirpath, f), symbol_maps)


if __name__ == '__main__':
    sys.exit(main())
