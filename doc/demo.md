#How does mosaic work?
Is mosaic already installed and server work? --> read installation.md

We need services, you can use the demo service from mosaic ($MOSAIC_HOME/services, for example
- html_generator
- file_writer


1-. We start the services with the mosaic-client in the terminal (at $MOSAIC_HOME)
--> ./mosaic-cli start_service html_generator
RESPONSE: deploying html_generator {"message":"service [html_generator] created"}
--> ./mosaic-cli start_service file_writer
RESPONSE: deploying file_writer {"message":"service [file_writer] created"}

2-. You can check if the services work
--> ./mosaic-cli services
RESPONSE: {"basic_reporting":{"params":{"logging":{"filename":"pipeline.log"},
           "name":"basic_reporting","filename":"monitoring.log","ip":"127.0.0.1","port":6690,"monitoring":{"filename":"monitoring.log"}}},
           "file_writer":{"params":{"name":"file_writer","ip":"127.0.0.1","port":5001}},
           "html_generator":{"params":{"name":"html_generator","ip":"127.0.0.1","port":5002}}}

NOTICE:
theirs services are there --> file_writer and html_generator
basic_reporting -What's that? --> there are internal mosaic services for the monitoring and logging

3-. We build one pipeline (for example)
--> ./mosaic-cli set_pipeline pipe-demo html_generator file_writer
RESPONSE: {"message":"pipeline [pipe-demo] created"}

4-. You can check if the pipeline are built
--> ./mosaic-cli pipelines
RESPONSE: {"pipe-demo":{"services":["html_generator","file_writer"],"active":true}}

5-. We sent a message to the pipeline
--> ./mosaic-cli post_to_pipeline pipe-demo "funktioniert oder nicht"
RESPONSE: {"message":"pipeline initiated","message_id":"49e7f379-43fe-4d2a-99f3-3012c498c613"}

6-. You can check if the index.html file exist :-)
--> Go to $MOSAIC_HOME/api-server and there is a index.html with your message
--> Open in a browser the $MOSAIC_HOME/api-server/index.html File and you can see your message

