import argparse
import os
import sys
import time
from typing import List, Optional

import yaml


class Symbol:
    __slots__ = ('include', 'package_name', 'target_name')

    def __init__(self, include: str, package_name: str, target_name: str):
        self.include = include
        self.package_name = package_name
        self.target_name = target_name


class Symbols:
    __slots__ = ('symbols', 'empty_token', 'namespace_depth', 'use_angle_brackets')

    def __init__(self, symbols: dict, empty_token: str, namespace_depth: int, use_angle_brackets: bool):
        self.symbols = symbols
        self.empty_token = empty_token
        self.namespace_depth = namespace_depth
        self.use_angle_brackets = use_angle_brackets


def find_type(single_token: str, symbol_map: Symbols) -> Optional[Symbol]:
    # In case this is just the empty namespace token, the actual type is
    # probably on the next line.  Since this entire utility is line-oriented,
    # there is no good way to get that.  Just ignore these; we may drop an
    # include here or there, but it is really not a big deal.
    if single_token != symbol_map.empty_token:
        if single_token.startswith(symbol_map.empty_token):
            double_colon_split = single_token.split('::')
            # Only look up to the depth specified
            first = '::'.join(double_colon_split[:symbol_map.namespace_depth])
            if first in symbol_map.symbols:
                if symbol_map.symbols[first]:
                    return symbol_map.symbols[first]

    return None


def search_for_namespaces(full_path: str, public: bool, symbol_maps: List[Symbols], print_missing_symbols: bool) -> None:
    print(full_path)

    include_groups = {}
    targets = set()
    exports = set()

    with open(full_path, 'r') as infp:
        in_c_comment = False
        for line in infp:
            stripped_line = line.strip()

            # Skip C++ style comments
            if stripped_line.startswith('//'):
                continue

            # Skip C-style comments
            if not in_c_comment:
                if stripped_line.startswith('/*'):
                    if not '*/' in stripped_line:
                        in_c_comment = True
                    continue
            else:
                if '*/' in line:
                    in_c_comment = False
                continue

            # TODO(clalancette): Also skip when inside of strings?

            # Skip all lines that don't have '::' in them.  Because of namespaces,
            # this means we might miss some dependencies, but it shouldn't matter too much.
            if not '::' in stripped_line:
                continue

            commas = stripped_line.replace('(', ',').replace(')', ',').replace('<', ',').replace('>', ',').replace(' ', ',').replace(';', ',').replace('{', ',').replace('}', ',').replace('&', ',').replace('...', ',').replace('!', ',')

            split = commas.split(',')
            for s in split:
                if not '::' in s:
                    continue

                for symbol_map in symbol_maps:
                    found_type = find_type(s, symbol_map)
                    if found_type is not None:
                        if symbol_map not in include_groups:
                            include_groups[symbol_map] = set()
                        include_groups[symbol_map].add(found_type.include)
                        if found_type.target_name:
                            targets.add(found_type.target_name)
                        if found_type.package_name:
                            exports.add(found_type.package_name)
                        break
                else:
                    if print_missing_symbols:
                        print(f'  ==> Missing symbol for {s}')

    print('Includes')
    for symbol_map, include_set in include_groups.items():
        for header in sorted(include_set):
            if symbol_map.use_angle_brackets:
                print(f'  #include <{header}>')
            else:
                print(f'  #include "{header}"')
        print('')

    if public:
        print('Public Targets')
    else:
        print('Private Targets')
    for target in sorted(targets):
        print(f'  {target}')

    if public:
        print('Exports')
        for export in sorted(exports):
            print(f'  {export}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--print-missing-symbols', required=False, action='store_true', default=False, help='Print symbols that could not be resolved')
    parser.add_argument('-t', '--types', nargs='+', required=False, default=[], help='A YAML file containing the types that should be examined while parsing')
    parser.add_argument('package_path', help='Path to the package to find dependencies for')

    options = parser.parse_args()

    symbol_maps = []
    for t in options.types:
        with open(t, 'r') as infp:
            data = yaml.safe_load(infp)
            symbols = {}
            if data['symbols'] is not None:
                for symbol in data['symbols']:
                    symbols[symbol['symbol_name']] = Symbol(symbol['include'], symbol['package_name'], symbol['target_name'])

            symbol_maps.append(Symbols(symbols, data['empty_token'], data['namespace_depth'], data['use_angle_brackets']))

    if not 'package.xml' in os.listdir(options.package_path):
        print(f'"{options.package_path}" does not contain a "package.xml" file')
        return 1

    for (dirpath, dirnames, filenames) in os.walk(options.package_path):
        for f in filenames:
            full_path = os.path.join(dirpath, f)
            public = False
            extension = os.path.splitext(full_path)[1]
            if extension in ('.h', '.hpp'):
                # possibly public
                no_initial = full_path.removeprefix(options.package_path)
                if no_initial.startswith('include'):
                    public = True
                else:
                    public = False
            elif extension in ('.cpp', '.cxx', '.cc'):
                # private
                public = False
            else:
                continue

            search_for_namespaces(full_path, public, symbol_maps, options.print_missing_symbols)

    return 0


if __name__ == '__main__':
    sys.exit(main())
