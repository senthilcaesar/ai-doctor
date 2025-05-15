"""
Script to inspect the serpapi package and its contents.
"""

import serpapi
import inspect

# Print the package version
print(f"serpapi version: {getattr(serpapi, '__version__', 'unknown')}")

# Print the package path
print(f"serpapi path: {serpapi.__file__}")

# Print the available attributes and methods
print("\nAvailable attributes and methods:")
for name in dir(serpapi):
    if not name.startswith('__'):
        attr = getattr(serpapi, name)
        if inspect.isfunction(attr) or inspect.isclass(attr):
            print(f"  {name}: {type(attr).__name__}")
        else:
            print(f"  {name}: {type(attr).__name__}")

# Try to find search-related functions
print("\nSearch for search-related functions:")
search_functions = [name for name in dir(serpapi) if 'search' in name.lower()]
for name in search_functions:
    attr = getattr(serpapi, name)
    print(f"  {name}: {type(attr).__name__}")

# Print module docstring
print("\nModule docstring:")
print(serpapi.__doc__)
