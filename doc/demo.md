# How does roxcomposer work?

If you don't have installed roxcomposer so far please read the [installation](installation.md) manual.

First of all we need to start up `roxconnector` the api-server, to get the roxcomposer-CLI (Command Line Interface) going. So 
please navigate to `$ROXCOMPOSER_DEMO_HOME` and execute the start\_server shell script:
```bash
	./start_server.sh
``` 

After the server has started, we need services. The roxcomposer-demo package contains a couple of services you can use 
located at `$ROXCOMPOSER_DEMO_HOME/services`: 

1. We start services with the roxcomposer-CLI in the terminal (at `$ROXCOMPOSER_HOME/cli`)

	```bash
		./roxcomposer-cli start_service html_generator
	```
	```bash 
		./roxcomposer-cli start_service file_writer
	```
2. You can check if the services are working and registered to the control process
	```bash
		./roxcomposer-cli services
	```
	Usually there is a service running called `basic_reporting`. This is an internal service to get monitoring 
	information.
3. The services collaborate in pipelines, which you can set, like shown below:
	```bash
		./roxcomposer-cli set_pipeline pipe-demo html_generator file_writer
	```
4. To check if the pipeline is created correctly, please type:
	```bash
		./roxcomposer-cli pipelines
	```
5. If you have finished managing your services, you can send messages to the pipelines. Basically the first service in
	a pipleine is receiving the message you have sent. So keep in mind, that the order of the services matter. Anyway
	this is how you post messages to pipelines.
	```bash
		./roxcomposer-cli post_to_pipeline pipe-demo "Hello World!"
	```
6. To make sure everything worked as expected in roxcomposer-demo example, please check if the `api-server` folder contains
	an `index.html` file.
7. Open the file in the browser of your choice, to see your "Hello World!" greetings.


