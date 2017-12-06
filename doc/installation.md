# Obtaining the package

You will need the mosaic installation package (a compressed tar archive) - which is obtainable only through the droxIT Lapteva & Baumgärtner GmbH

## System prerequesites

* a Linux/Unix based deployment environment
* Python version >= 3.6 (https://www.pyhton.org)
* pip3 (usually provided alongside Python on most distributions)
* NodeJS >= 6.x (the NodeJS executable is expected to be called node. If this is not the case please make sure to create a symlink or bash alias to the real executable under that name)
* npm (https://www.npmjs.org)

## Setup

To get up and running you need to unpack the tar archive and change into the newly created mosaic folder:

```bash
tar xf mosaic-demo.tar.gz
cd mosaic
```

### Python class only

If you only want to use the service base class and construct your own infrastructure around it you can just install the Python code package:

```bash
pip3 install --user packages/mosaic-0.2.0.tar.gz
```

The `--user` flag can be omitted if you have super user rights and want to install the package to the system wide location. Now you can simply use the service base class inside your project. See the development section of this handbook for details.

### The whole package

If you want to install the control process alongside the Python package simply call the install script:

```bash
./install.sh --user
```

Again the `--user` flag can be omitted (see above).

The command will install the mosaic Python package via `pip` and pull all the Node.JS dependencies with `npm`. The package ships with a basic configuration for the REST interface and the control process can be started with the `start_server.sh` script.


