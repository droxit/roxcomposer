droxIT - mosaic
===============
This is droxits microservice framework repository. It yields a python framework to set up microservices easily.

Status
----------
Dev:
.. image:: https://circleci.com/gh/droxit/mosaic/tree/dev.svg?style=svg&circle-token=8abde3cd460a4a044d7c3de054e757853e03a6c3
    :target: https://circleci.com/gh/droxit/mosaic/tree/dev
Master:
.. image:: https://circleci.com/gh/droxit/mosaic/tree/master.svg?style=svg&circle-token=8abde3cd460a4a044d7c3de054e757853e03a6c3
    :target: https://circleci.com/gh/droxit/mosaic/tree/master

Dependencies
----------
Please execute 

>>> pip3.5 install -r requirements.txt

to install all python requirements.

Setup
----
To setup the framework and to use it, you can use our local pip package on gru. Please execute the following command

>>> pip3.5 install -i http://localhost:4040/droxit/dev mosaic

Remember that you need to open an ssh tunnel to gru, to use this command.

Further documentation
---------------------
For further documentation please consider reading the `Handbook
https://droxit.atlassian.net/wiki/spaces/PROJ/pages/74088468/Handbook` _.

Build Config
---------
To configure builds along the the Continuous Integration pipeline please have a look at the 
`.circleci/config.yml`. 
