

This is the command line interface for the [python-gardenlinux-lib](https://github.com/gardenlinux/python-gardenlinux-lib/) library. Logic is implemented in the library, this is just the CLI wrapper. 

- OCI publishing  🏗️🟡 -  80% done
- Parse features  - 🔴 0% done
    - validate cname
    - extract features from cname sorted by type  
    - check if a feature is included in a given cname
    - more
- Garden Version - 🔴 0% done
- Apt Repository parsing - 🔴 20% done
    - 
 
# Example Usage
```
# Compare two garden linux apt repositories
glcli apt compare --version_a 1592.0 --version_b 1602.0
# prints list of tuples (package name, pkg version of version_a, pkg version of version_b)
```
