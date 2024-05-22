import os
import sys
import time

cpp_type_to_include_map = {
    'std::abs': 'cmath',
    'std::acos': 'cmath',
    'std::alignment_of': 'type_traits',
    'std::all_of': 'algorithm',
    'std::any_of': 'algorithm',
    'std::array': 'array',
    'std::async': 'future',
    'std::atan': 'cmath',
    'std::atan2': 'cmath',
    'std::atomic': 'atomic',
    'std::atomic_load': 'atomic',
    'std::atomic_store': 'atomic',
    'std::back_inserter': 'iterator',
    'std::bad_alloc': 'stdexcept',
    'std::basic_string': 'string',
    'std::basic_string_view': 'string_view',
    'std::begin': '',
    'std::bind': 'functional',
    'std::ceil': 'cmath',
    'std::cerr': 'iostream',
    'std::chrono': 'chrono',
    'std::chrono_literals': 'chrono',
    'std::clamp': 'algorithm',
    'std::conditional': 'type_traits',
    'std::condition_variable': 'condition_variable',
    'std::copy': 'algorithm',
    'std::copy_n': 'algorithm',
    'std::copysign': 'cmath',
    'std::cos': 'cmath',
    'std::cout': '<iostream>',
    'std::ctime': 'ctime',
    'std::declval': 'utility',
    'std::defer_lock': 'mutex',
    'std::deque': 'deque',
    'std::distance': 'iterator',
    'std::dynamic_pointer_cast': 'memory',
    'std::enable_if': 'type_traits',
    'std::end': '',
    'std::endl': 'ostream',
    'std::equal': 'algorithm',
    'std::equal_to': 'functional',
    'std::exception': 'exception',
    'std::exit': 'cstdlib',
    'std::fabs': 'cmath',
    'std::false_type': 'type_traits',
    'std::filesystem': 'filesystem',
    'std::fill': 'algorithm',
    'std::fill_n': 'algorithm',
    'std::find': 'algorithm',
    'std::find_if': 'algorithm',
    'std::fixed': 'ios',
    'std::floor': 'cmath',
    'std::fmod': 'cmath',
    'std::for_each': 'algorithm',
    'std::forward': 'utility',
    'std::forward_as_tuple': 'tuple',
    'std::forward_iterator_tag': 'iterator',
    'std::free': 'cstdlib',
    'std::function': 'functional',
    'std::future': 'future',
    'std::future_status': 'future',
    'std::get': 'tuple',
    'std::getenv': 'cstdlib',
    'std::hash': '',
    'std::hypot': 'cmath',
    'std::ifstream': 'fstream',
    'std::initializer_list': 'initializer_list',
    'std::integral_constant': 'type_traits',
    'std::invalid_argument': 'stdexcept',
    'std::is_default_constructible': 'type_traits',
    'std::is_enum': 'type_traits',
    'std::is_floating_point_v': 'type_traits',
    'std::is_integral': 'type_traits',
    'std::is_integral_v': 'type_traits',
    'std::is_nothrow_move_assignable': 'type_traits',
    'std::is_nothrow_move_constructible': 'type_traits',
    'std::is_nothrow_swappable': 'type_traits',
    'std::is_same': 'type_traits',
    'std::is_same_v': 'type_traits',
    'std::is_trivially_copyable': 'type_traits',
    'std::is_trivially_destructible': 'type_traits',
    'std::is_void': 'type_traits',
    'std::isalnum': 'cctype',
    'std::isinf': 'cmath',
    'std::isfinite': 'cmath',
    'std::isnan': 'cmath',
    'std::istreambuf_iterator': 'iterator',
    'std::launch': 'future',
    'std::list': 'list',
    'std::literals': '',
    'std::lock_guard': 'mutex',
    'std::logic_error': 'stdexcept',
    'std::malloc': 'cstdlib',
    'std::make_heap': 'algorithm',
    'std::make_pair': 'utility',
    'std::make_shared': 'memory',
    'std::make_tuple': 'tuple',
    'std::make_unique': 'memory',
    'std::map': 'map',
    'std::max': 'algorithm',
    'std::max_align_t': 'cstddef',
    'std::max_element': 'algorithm',
    'std::memcpy': 'cstring',
    'std::memset': 'cstring',
    'std::min': 'algorithm',
    'std::move': 'utility',
    'std::mt19937': 'random',
    'std::mutex': 'mutex',
    'std::next': 'iterator',
    'std::none_of': 'algorithm',
    'std::normal_distribution': 'random',
    'std::nullopt': 'optional',
    'std::numeric_limits': 'limits',
    'std::ofstream': 'fstream',
    'std::optional': 'optional',
    'std::ostream': 'ostream',
    'std::ostringstream': 'sstream',
    'std::out_of_range': 'stdexcept',
    'std::overflow_error': 'stdexcept',
    'std::pair': 'utility',
    'std::piecewise_construct': 'utility',
    'std::piecewise_construct_t': 'utility',
    'std::placeholders': 'functional',
    'std::pop_heap': 'algorithm',
    'std::pow': 'cmath',
    'std::prev': 'iterator',
    'std::promise': 'future',
    'std::priority_queue': 'queue',
    'std::ptrdiff_t': 'cstddef',
    'std::push_heap': 'algorithm',
    'std::random_device': 'random',
    'std::recursive_mutex': 'mutex',
    'std::replace': 'algorithm',
    'std::replace_if': 'algorithm',
    'std::remove_all_extents': 'type_traits',
    'std::remove': 'algorithm',
    'std::remove_if': 'algorithm',
    'std::reverse': 'algorithm',
    'std::reverse_iterator': 'iterator',
    'std::rint': 'cmath',
    'std::round': 'cmath',
    'std::runtime_error': 'stdexcept',
    'std::scoped_lock': 'mutex',
    'std::set': 'set',
    'std::setprecision': 'iomanip',
    'std::shared_future': 'future',
    'std::shared_ptr': 'memory',
    'std::sin': 'cmath',
    'std::size_t': 'cstddef',
    'std::sort': 'algorithm',
    'std::sqrt': 'cmath',
    'std::static_pointer_cast': 'memory',
    'std::stoul': 'string',
    'std::strerror': 'cstring',
    'std::string': 'string',
    'std::string_view': 'string_view',
    'std::stringstream': 'sstream',
    'std::swap': 'utility',
    'std::thread': 'thread',
    'std::this_thread': 'thread',
    'std::tie': 'tuple',
    'std::time_t': 'ctime',
    'std::to_string': 'string',
    'std::tolower': 'cctype',
    'std::transform': 'algorithm',
    'std::true_type': 'type_traits',
    'std::tuple': 'tuple',
    'std::uint8_t': 'cstdint',
    'std::uint32_t': 'cstdint',
    'std::underlying_type': 'type_traits',
    'std::uniform_int_distribution': 'random',
    'std::unique_lock': 'mutex',
    'std::unique_ptr': 'memory',
    'std::unordered_map': 'unordered_map',
    'std::unordered_set': 'unordered_set',
    'std::vector': 'vector',
    'std::weak_ptr': 'memory',
}


def search_for_namespaces(full_path: str):
    print(full_path)
    include_set = set()

    with open(full_path, 'r') as infp:
        in_c_comment = False
        for line in infp:
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

                # In case this is a lone 'std::', the actual type is on the next
                # line.  But since this entire utility is line-oriented, there is
                # no good way to get that.  Just ignore these; we may drop an include
                # on the floor, but it is really not a big deal.
                if s == 'std::':
                    continue

                if s.startswith('std::'):
                    # We only want to look at the std:: and the first part
                    double_colon_split = s.split('::')
                    first = '::'.join(double_colon_split[:2])
                    if first not in cpp_type_to_include_map:
                        print(first)
                    else:
                        if cpp_type_to_include_map[first]:
                            include_set.add(cpp_type_to_include_map[first])

    print(include_set)


def main():
    if len(sys.argv) != 2:
        print('Usage: %s <package_path>' % (sys.argv[0]))
        return 1

    package_path = sys.argv[1]

    for (dirpath, dirnames, filenames) in os.walk(package_path):
        for f in filenames:
            extension = os.path.splitext(f)[1]
            if extension not in ('.cpp', '.cxx', '.cc', '.h', '.hpp'):
                continue

            search_for_namespaces(os.path.join(dirpath, f))


if __name__ == '__main__':
    sys.exit(main())
