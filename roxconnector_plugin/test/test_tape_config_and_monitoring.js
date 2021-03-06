/*
 * Test Classe test_config_and_monitoring: standard test for login and monitoring functionalities from roxcomposer
 *
 * |------------------- OPEN SOURCE LICENSE DISCLAIMER -------------------|
 * |                                                                      |
 * | Copyright (C) 2019  droxIT GmbH - devs@droxit.de                     |
 * |                                                                      |
 * | This file is part of ROXcomposer.                                    |
 * |                                                                      |
 * | ROXcomposer is free software: you can redistribute it and/or modify  |
 * | it under the terms of the GNU Lesser General Public License as       |
 * | published by the Free Software Foundation, either version 3 of the   |
 * | License, or (at your option) any later version.                      |
 * |                                                                      |
 * | This program is distributed in the hope that it will be useful,      |
 * | but WITHOUT ANY WARRANTY; without even the implied warranty of       |
 * | MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the         |
 * | GNU General Public License for more details.                         |
 * |                                                                      |
 * | You have received a copy of the GNU Lesser General Public License    |
 * | along with this program. See also <http://www.gnu.org/licenses/>.    |
 * |                                                                      |
 * |----------------------------------------------------------------------|
 */

let bunyan = require('bunyan');
let path = require('path');
let sleep = require('system-sleep');
let fs = require('fs');
let test = require('tape');
let tapSpec = require('tap-spec');
let os = require('os');
const { sep } = require('path');

test.createStream().pipe(tapSpec()).pipe(process.stdout);

let filewriter_module_path = path.join('..', 'roxcomposer', 'tests', 'classes', 'file_writer.py');

let tmp = os.tmpdir();
fs.mkdtemp(`${tmp}${sep}`, (error, tmpdir) => {
	if (error) {
		throw error;
	}

	test('config and monitoring', function (assert) {
		let service_file = path.join(tmpdir, "config.json");
		let service_file2 = path.join(tmpdir, "config2.json");
		let monitoring_file = path.join(tmpdir, "monitoring.log");
		let roxcomposerlog_file = path.join(tmpdir, "config_and_monitoring.log");
		let servicelog_file = path.join(tmpdir, "service.log");
		let logger = bunyan.createLogger({
			name: 'roxcomposer-control-testing',
			streams: [{level: 'debug', path: roxcomposerlog_file}]
		});
		let init_params = {
			logger: logger,
			service_container: path.join('..', 'util', 'service_container.py'),
			default: { logging: { logpath: tmpdir } },
			reporting_service: {
				classpath: 'roxcomposer.monitor.basic_reporting_service.BasicReportingService',
				params: {
					logging: { logpath: servicelog_file },
					name: 'basic_reporting',
					filename: monitoring_file,
					ip: '127.0.0.1',
					port: 7123,
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
					filepath: path.join(tmpdir, "blub.out"),
					ip: "127.0.0.1",
					port: 6691,
					monitoring: {
						filename: monitoring_file
					}
				}
			}
		}

		let alternate_service_config = {
			services: {
				file_writer2: {
					name: "file_writer2",
					filepath: path.join(tmpdir, "blub.out"),
					ip: "127.0.0.1",
					port: 6791,
					monitoring: {
						filename: monitoring_file
					}
				}
			}
		}

		assert.plan(17);

		let mc = {}
		require('../roxcomposer_control.js')(mc);
		mc.init({logger: logger});
		mc.start_service({path: filewriter_module_path, params: {service_key: "services.i_dont_exist"}}, function (err, msg) {
			assert.ok(err, 'start_service should return an error when starting FileWriter with a service_key without a service config');
		});

		fs.writeFileSync(service_file, JSON.stringify(service_config));
		fs.writeFileSync(service_file2, JSON.stringify(alternate_service_config));
		process.env['DROXIT_ROXCOMPOSER_CONFIG'] = service_file;
		mc = {}
		require('../roxcomposer_control.js')(mc);
		mc.init(init_params);


		//mc.start_service({path: filewriter_module_path, params: service_config.services.file_writer}, function (err, msg) {
		mc.start_service({path: filewriter_module_path, params: {service_key: "services.i_dont_exist"}}, function (err, msg) {
			assert.ok(err, 'start_service should return an error when starting FileWriter with an invalid service_key');
		});
		mc.start_service({path: filewriter_module_path, params: {service_key: "services.file_writer"}}, function (err, msg) {
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
		mc.start_service({path: filewriter_module_path, params: {service_key: "services.file_writer2", config_file: service_file2}}, function (err, msg) {
			assert.notOk(err, 'start_service should return no error when starting FileWriter with a service_key configuration and explicit config file');
			sleep(300);
			mc.shutdown_service({name: 'file_writer2'}, function(err, msg) {
				assert.notOk(err, 'we should get no error when shutting down file_writer2');
			});
		});
	});
});

