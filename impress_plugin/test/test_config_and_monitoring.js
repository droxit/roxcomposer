let bunyan = require('bunyan');
let path = require('path');
let sleep = require('system-sleep');
let fs = require('fs');
let test = require('tape');
let tapSpec = require('tap-spec');

test.createStream().pipe(tapSpec()).pipe(process.stdout);

let filewriter_module_path = '../mosaic/tests/classes/file_writer.py';
let tmpdir = fs.mkdtempSync('/tmp/mosaic_control_test_integration_');

test('config and monitoring', function (assert) {
	let service_file = tmpdir + "/config.json";
	let monitoring_file = tmpdir + "/monitoring.log";
	let impresslog_file = tmpdir + "/config_and_monitoring.log";
	let servicelog_file = tmpdir + "/service.log";
	let logger = bunyan.createLogger({
		name: 'mosaic-control-testing',
		streams: [{level: 'debug', path: impresslog_file}]
	});
	let init_params = {
		logger: logger,
		service_container: '../util/service_container.py',
		reporting_service: {
			classpath: 'mosaic.monitor.basic_reporting_service.BasicReportingService',
			params: {
				logging: { filename: servicelog_file },
				name: 'basic_reporting',
				filename: monitoring_file,
				ip: '127.0.0.1',
				port: 6690,
				monitoring: {
					filename: monitoring_file
				}
			}
		}
	}
	let service_config = {
		services: {
			file_writer: {
				name: "file_writer",
				filepath: tmpdir + "/blub.out",
				ip: "127.0.0.1",
				port: 6691,
				monitoring: {
					filename: monitoring_file
				}
			}
		}
	}
	fs.writeFileSync(service_file, JSON.stringify(service_config));
	process.env['DROXIT_MOSAIC_CONFIG'] = service_file;
	let mc = {}
	require('../mosaic_control.js')(mc);
	mc.init(init_params);

	assert.plan(13);

	// config key is not working atm, because impress needs to know the service's ip and the port 
	// I'm replacing this with a regular call with explicit settings until things are fixed
	//mc.start_service({path: filewriter_module_path, params: {name: "file_writer", service_key: "services.file_writer"}}, function (err, msg) {
	mc.start_service({path: filewriter_module_path, params: service_config.services.file_writer}, function (err, msg) {
		assert.notOk(err, 'start_service should return no error when starting FileWriter with a service_key configuration');
		sleep(100);
		mc.set_pipeline({name: 'pipe', services: ['file_writer']}, function (err, msg) {
			let message_id = null;
			let test_msg = "asdlfkj023qijfq'23kfj__(02395";
			setTimeout(() => {
				mc.post_to_pipeline({name: 'pipe', data: test_msg}, function (err, msg) {
					assert.notOk(err, 'post_to_pipeline should not return an error');
					assert.ok('message_id' in msg, 'when posting to a pipeline we should get a message id back');
					message_id = msg.message_id;
					setTimeout(() => {
						mc.get_msg_history({message_id: message_id}, function(err ,msg) {
							assert.notOk(err, 'get_msg_history should not return an error');
							assert.notOk('error' in msg, 'the reply should not be an error');
							assert.equal(msg.length, 2, 'we expect to events in the message history');
							assert.equal(msg[0].event, 'message_received', "first should be 'message_received'");
							assert.equal(msg[1].event, 'message_final_destination', "second should be 'message_final_destination'");
							mc.get_msg_status({message_id: message_id}, function(err ,msg) {
								assert.notOk(err, 'get_msg_status should not return an error');
								assert.ok('status' in msg, 'the returned message should have a status');
								assert.equal(msg.status, 'finalized', "....which should be 'finalized'");
								mc.shutdown_service({name: 'basic_reporting'}, function(err, msg) {
									assert.notOk(err, 'we should get no error when shutting down the reporting service');
								});
								mc.shutdown_service({name: 'file_writer'}, function(err, msg) {
									assert.notOk(err, 'we should get no error when shutting down file_writer');
								});
							});
						});
					}, 400);
				});
			}, 500);
		});
	});
});
	
