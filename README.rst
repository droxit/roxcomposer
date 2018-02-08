droxIT - mosaic
===============
This is droxits microservice framework repository. It yields a python framework to set up microservices easily.

Status
------
Dev:

.. image:: https://circleci.com/gh/droxit/mosaic/tree/dev.svg?style=svg&circle-token=8abde3cd460a4a044d7c3de054e757853e03a6c3
    :target: https://circleci.com/gh/droxit/mosaic/tree/dev

Master:

.. image:: https://circleci.com/gh/droxit/mosaic/tree/master.svg?style=svg&circle-token=8abde3cd460a4a044d7c3de054e757853e03a6c3
    :target: https://circleci.com/gh/droxit/mosaic/tree/master

Dependencies
----------
Please execute 

>>> pip3.6 install -r requirements.txt

to install all python requirements.

Setup
-----
To setup the framework and to use it, you can use our local pip package on gru. Please execute the following command

>>> pip3.6 install -i http://localhost:4040/droxit/dev mosaic

Remember that you need to open an ssh tunnel to gru, to use this command.

Version
-------
The version is detailed in the VERSION file. setup.py will take the version from there in order to generate the package version.
Development versions get the version that is intended for the later release suffixed with 'dev' and a build number. This is done
automatically by CircleCI during deployment. If you wish to change the version locally either change the VERSION file or set the
environment variable MOSAIC_VERSION before calling setup.py.

Further documentation
---------------------
For further documentation please consider reading the `Handbook
<https://github.com/droxit/mosaic/blob/dev/doc/handbook.md>`_.

Build Config
------------
To configure builds along the the Continuous Integration pipeline please have a look at the 
`.circleci/config.yml`. 

Running Tests
-------------
In order to run tests, please use

python3 setup.py test

and

cd impress_plugin && npm test

Deploy Config
-------------

ENV VAR 'DROXIT_MOSAIC_CONFIG' to configure service's params


Build Tasks
-----------
    >>> ./build_mosaic_demo_local.sh <MOSAIC_PACKAGE_PATH> <IMPRESS_PLUGIN_PATH>

e.g

    >>> ./build_mosaic_demo_local.sh ./dist/mosaic-*.tar.gz impress_plugin

Deploy Tasks
------------
    >>> ./deploy_mosaic_demo_local.sh <MOSAIC_DEMO_PATH>

e.g

    >>> ./deploy_mosaic_demo_local.sh ../../test_installation/

Build & Deploy Tasks
--------------------
    >>> ./build_deploy_mosaic_demo_local.sh <RELATIVE_MOSAIC_PACKAGE_PATH> <RELATIVE_IMPRESS_PLUGIN_PATH> <RELATIVE_MOSAIC_DEMO_PATH>

e.g

    >>> ./build_deploy_mosaic_demo_local.sh ./dist/mosaic-*.tar.gz impress_plugin ../../test_installation/
