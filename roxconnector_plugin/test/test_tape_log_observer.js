//
// Test Classe test_roxcomposer_control: standard test for roxcomposer functionalities
//
// |------------------- OPEN SOURCE LICENSE DISCLAIMER -------------------|
// |                                                                      |
// | Copyright (C) 2019  droxIT GmbH - devs@droxit.de                     |
// |                                                                      |
// | This program is free software: you can redistribute it and/or modify |
// | it under the terms of the GNU General Public License as published by |
// | the Free Software Foundation, either version 3 of the License, or    |
// | (at your option) any later version.                                  |
// |                                                                      |
// | This program is distributed in the hope that it will be useful,      |
// | but WITHOUT ANY WARRANTY; without even the implied warranty of       |
// | MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the         |
// | GNU General Public License for more details.                         |
// |                                                                      |
// | You have received a copy of the GNU General Public License           |
// | along with this program. See also <http://www.gnu.org/licenses/>.    |
// |                                                                      |
// |----------------------------------------------------------------------|
//

let os = require('os');
let bunyan = require('bunyan');
let path = require('path');
let sleep = require('system-sleep');
let fs = require('fs');
let test = require('tape');
let tapSpec = require('tap-spec');
let tmp = os.tmpdir();
const { sep } = require('path');

let mc  = {};
test.createStream().pipe(tapSpec()).pipe(process.stdout);

fs.mkdtemp(`${tmp}${sep}`, (err, tmpdir) => {
	if (err){
		throw err;
	}

	let roxcomposer_config = {
		services: {
			basic_reporting: {
				classpath: "roxcomposer.monitor.basic_reporting_service.BasicReportingService",
				params: {
					logging: {
						logpath: path.join(tmpdir, "pipeline.log")
					},
					name: "basic_reporting",
					filename: "monitoring.log",
					ip: "127.0.0.1",
					port: 6690,
					monitoring: {
						filename: path.join(tmpdir, "monitoring.log")
					}
				}
			},
			file_writer: {
				classpath: "roxcomposer.tests.classes.file_writer.FileWriter",
				params: {
					name: "file_writer",
					ip: "127.0.0.1",
					port: 4001,
					filepath: "roxcomposer_demo.html",
					logging: {
						logpath: path.join(tmpdir, "service.log"),
						level: "INFO"
					}
				}
			},
			image_adder: {
				classpath: "roxcomposer.tests.classes.image_adder.ImageAdder",
				params: {
					name: "image_adder",
					ip: "127.0.0.1",
					port: 4003,
					image: "./assets/droxit.jpg",
					logging: {
						logpath: path.join(tmpdir, "service.log"),
						level: "INFO"
					}
				}
			},
			html_generator: {
				classpath: "roxcomposer.tests.classes.html_generator.HtmlGenerator",
				params: {
					name: "html_generator",
					ip: "127.0.0.1",
					port: 4002,
					logging: {
						logpath: path.join(tmpdir, "service.log"),
						level: "INFO"
					}
				}
			}
		},
		pipelines: {
			pipe1: {
				services: [
					'html_generator',
					'image_adder',
					'file_writer'
				],
				active: true
			}
		}
	}

	require('../roxcomposer_control.js')(mc);
	let logger = bunyan.createLogger({
		name: 'roxcomposer-control-testing',
		streams: [{level: 'fatal', path: '/dev/null'}]
	});
	mc.init({logger: logger, service_container: '../util/service_container.py'});
	mc.load_services_and_pipelines(roxcomposer_config, function (err, ret) {
		if(ret.errors.length) {
			console.error('unable to setup services and pipelines');
			console.error(ret.errors);
			process.exit(1);
		} else {
			console.log('test services initiated');
			test('log observer endpoint', run_tests);
		}
	});
});

let cleanup = (t) => {
	mc.shutdown_service({ name: "html_generator" },(err)=>{
		t.notOk(err, 'shutdown html_generator');
	});
	mc.shutdown_service({ name: "image_adder" }, (err) => {
		t.notOk(err, 'shutdown image_adder');
	});
	mc.shutdown_service({ name: "file_writer" }, (err)=>{
		t.notOk(err, 'shutdown file_writer');
	});
	mc.shutdown_service({ name: "basic_reporting" }, (err)=>{
		t.notOk(err, 'shutdown basic_reporting');
	});

	setTimeout(() => process.exit(0), 100);
}

function run_tests(t) {
	setTimeout(() => {
		t.plan(22);
		let promises = [];

		promises.push(new Promise((resolve, reject) => {
			mc.create_log_observer({}, function (err, ret) {
				t.ok(err, "creating a log observer without parameters should return an error"); // TEST
				resolve();
			});
		}));
		promises.push(new Promise((resolve, reject) => {
			mc.create_log_observer({ lines: 10 }, function (err, ret) {
				t.ok(err, "creating a log observer without a timeout should return an error"); // TEST
				resolve();
			});
		}));
		promises.push(new Promise((resolve, reject) => {
			mc.create_log_observer({ timeout: 10 }, function (err, ret) {
				t.ok(err, "creating a log observer without the lines parameter should return an error"); // TEST
				resolve();
			});
		}));
		promises.push(new Promise((resolve, reject) => {
			mc.delete_log_observer({sessionid: 'wrong id'}, (err, ret) => {
				t.ok(err, "deleting the session with an invalid session id should return an error"); // TEST
				resolve();
			});
		}));
		promises.push(new Promise((resolve, reject) => {
			mc.delete_log_observer({}, (err, ret) => {
				t.ok(err, "deleting the session without arguments should return an error"); // TEST
				resolve();
			});
		}));
		promises.push(new Promise((resolve, reject) => {
			mc.create_log_observer({ lines: 10, timeout: 300 }, function (err, ret) {
				t.notOk(err, 'creating a log observer with proper arguments should not return an error'); // TEST
				t.ok('sessionid' in ret, "create_log_observer should return a sessionid"); // TEST
				mc.delete_log_observer({sessionid: ret.sessionid}, (err, ret) => {
					t.notOk(err, "deleting the session should not produce an error"); // TEST
					resolve();
				});
			});
		}));
		promises.push(new Promise((resolve, reject) => {
			mc.create_log_observer({ lines: 10, timeout: 300, services: ["html_generator", "image_adder"] }, function (err, ret) {
				t.notOk(err, 'we should not get an error when creating a log observer with files to observe'); // TEST
				t.ok('sessionid' in ret, "create_log_observer should return a sessionid when invoked with a services parameter"); // TEST
				mc.post_to_pipeline({name: 'pipe1', data: 'some random text'}, (err, _) => {
					t.notOk(err, 'post_to_pipeline should not produce an error'); // TEST
					setTimeout(() => {
						mc.get_log_lines({sessionid: ret.sessionid}, (err, r) => {
							t.notOk(err, 'get_log_lines should not return an error'); // TEST
							t.ok('loglines' in r, 'get_log_lines should return an object with a loglines field'); // TEST
							t.ok(r.loglines.length >= 2, 'there should be at least 3 loglines present in the returned object'); // TEST
							let servs = new Set(['html_generator', 'image_adder']);
							let all_match = r.loglines.map(line => { l = JSON.parse(line); return servs.has(l.service); }).reduce((a,b) => a && b, true);
							t.ok(all_match, 'all returned lines should be from the correct services'); // TEST
							mc.delete_log_observer({'sessionid': ret.sessionid, services: ['html_generator']}, (err, r) => {
								t.notOk(err, 'removing one services from log observation should not cause an error'); // TEST
								mc.post_to_pipeline({name: 'pipe1', data: 'have some more data'}, () => {
									setTimeout(() => {
										mc.get_log_lines({sessionid: ret.sessionid}, (err, r) => {
											t.notOk(err, 'get_log_lines should not return an error'); // TEST
							                                let servs = new Set(['html_generator']);
							                                let all_match = r.loglines.map(line => { l = JSON.parse(line); return !servs.has(l.service); }).reduce((a,b) => a && b, true);
											t.ok(all_match, 'no lines from the removed service should appear'); // TEST
											resolve();
										});
									}, 500);
								});
							});
						});
					}, 500);
				});
			});
		}));

		Promise.all(promises).then(() => cleanup(t), () => cleanup(t)).catch(e => cleanup(t));
	}, 500);
}
