## System prerequesites

* a Linux/Unix based deployment environment
* Python version >= 3.6 (https://www.pyhton.org)
* pip3 (usually provided alongside Python on most distributions)
* NodeJS >= 6.x (the NodeJS executable is expected to be called node. If this is not the case please make sure to create a symlink or bash alias to the real executable under that name)
* npm (https://www.npmjs.org)

# Building the package

The project contains a Makefile with targets for package building and deployment:

| command | description |
| --- | ---- |
| make python-package | build only the python package containing only the base functionality. The package will be placed in `dist` |
| make demo-package   | build a whole demo system with all interlocking parts into one archive in `build` |
| make deploy-demo    | deploy the demo (build it if needed) to a directory. The script will prompt for the target location. During this step the ROXconnector package will be downloaded and if needed access credentials will be prompted for |

## Setup

To deploy a built demo archive you have to unpack it:

```bash
tar xpf roxcomposer-demo-0.4.0.tar.gz
cd roxcomposer-demo-0.4.0
```

and use the `install.sh` to pull the project dependencies:

```bash
./install.sh --user
```

The command will install the roxcomposer Python package via `pip` and pull all the Node.JS dependencies with `npm`.

The `--user` flag can be omitted if you have super user rights and want to install the package to the system wide location. Now you can simply use the service base class inside your project. See the development section of this handbook for details.


### Python class only

If you only want to use the service base class and construct your own infrastructure around it you can just install the Python code package:

```bash
pip3 install --user roxcomposer-0.4.0.tar.gz
```

The `--user` flag can be omitted (see above).

