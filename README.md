# ros2_pkg_dep_tool

This repository houses a tool to look at a ROS 2 package and suggest dependencies.
In particular, it will suggest the `#include` lines each file needs, the CMake targets that are needed for each file (PUBLIC and PRIVATE), and the dependencies that should be exported via `ament_export_dependencies` for this package.

## Dependencies

This package only depends on PyYAML; you can generally get it by doing `apt-get install python3-yaml`, or by doing `pip install yaml`.

## Usage

Note that the package only works on ROS 2 packages, specifically those that have a `package.xml` file at their top-level.

Also note that the tool needs a database of symbols to includes/package names in order to find anything to do.
This repository has a number of these databases of symbols, but you will likely hae to add your own.

To run this tool against a package, you would do:

```
python3 find_deps_in_pkg.py -t *.yaml -- <path_to_pkg>
```

It will then tokenize every file individually, and print out for each one the includes, targets, and exports.
Note that many of the includes will already be in the file; as it stands, the tool isn't smart enough to only add missing ones.

You can also have it print out every single token it couldn't map to something; this is useful if you want to expand the database:

```
python3 find_deps_in_pkg.py -p -t *.yaml -- <path_to_pkg>
```

Generally, the output of the tool should be incorporated into the individual files, the package.xml, and the CMakeLists.txt.
