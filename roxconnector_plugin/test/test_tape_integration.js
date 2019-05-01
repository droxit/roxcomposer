//
// Test Classe test_integration
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
const { sep } = require('path');

test.createStream().pipe(tapSpec()).pipe(process.stdout);

let logger = bunyan.createLogger({
				name: 'roxcomposer-control-testing',
				streams: [{level: 'fatal', path: '/dev/null'}]
			});
let filewriter_module_path = path.join('..', 'roxcomposer', 'tests', 'classes', 'file_writer.py');
let tmp = os.tmpdir();
fs.mkdtemp(`${tmp}${sep}`, (error, tmpdir) => {
	if (error) {
		throw error;
	}
	test('service startup and control', function (assert) {
		let filepath = path.join(tmpdir, "file_writer.out");
		let filewriter_params = {name: 'fwriter', ip: '127.0.0.1', port: 6889, filepath: filepath,
			logging: {
			"logpath": "pipeline.log",
				"level": "DEBUG"}
	};
		let test_msg = 'test _mesage from hell';
		let mc = {};
		require('../roxcomposer_control.js')(mc);
		mc.init({logger: logger});

		assert.plan(20);
		mc.start_service({path: filewriter_module_path, params: filewriter_params}, function (err, msg) {
			assert.notOk(err, "start_service should not return an error");
			sleep(500);
			mc.get_services(null, function(err, msg) {
				assert.notOk(err, "get_services should not return an error");
				assert.deepEqual(msg, {fwriter: {path: filewriter_module_path, params: filewriter_params}}, "the started service should be listed with it's parameters");
				mc.set_pipeline({name: 'pipe', services: ['fwriter']}, function (err, msg) {
					assert.notOk(err, 'creating a pipeline with the new service should not produce an error');
					mc.get_pipelines(null, function (err, msg) {
						assert.notOk(err, 'get_pipelines should not produce an error');
						assert.deepEqual(msg, {pipe: {services: [{'service': 'fwriter'}], active: true}}, 'our created pipeline should be present');
						mc.post_to_pipeline({name: 'pipe', data: test_msg}, function (err, msg) {
							assert.notOk(err, 'post_to_pipeline should not produce an error');
							sleep(500);
							assert.equal(fs.readFileSync(filepath, 'utf8'), test_msg, 'the file_writer service should have written our test message into the file');
							mc.dump_services_and_pipelines(null, (err, dump) => {
								dump = JSON.parse(JSON.stringify(dump));
								assert.deepEqual(dump.pipelines, { pipe: { services: [{'service': 'fwriter'}], active: true }}, 'pipe should be in the services and pipelines dump');
								assert.ok('fwriter' in dump.services, '...so should be fwriter');
								mc.shutdown_service({name: 'fwriter'}, function(err, msg) {
									assert.notOk(err, 'shutdown_service should not return an error');
									setTimeout(() => {
										mc.get_services(null, function(err, msg) {
											assert.deepEqual(msg, {}, 'get_services should now be empty');
										});
										mc.get_pipelines(null, function(err, msg) {
											assert.notOk(msg.pipe.active, 'the pipeline should now be deactivated');
										});
										mc.post_to_pipeline({name: 'pipe', data: 'alfkajdf'}, function(err, msg) {
											assert.ok(err.code >= 399, 'posting to the pipeline should return an error');
										});
										setTimeout(() => {
											mc.load_services_and_pipelines(dump, (err, msg) => {
												assert.notOk(err, 'restoring the previous state should not produce an error');
												mc.get_services(null, function(err, msg) {
													assert.notOk(err, "get_services should not return an error");
													assert.deepEqual(msg, {fwriter: {path: filewriter_module_path, params: filewriter_params}}, "the started service should be listed with it's parameters");
													mc.get_pipelines(null, function (err, msg) {
														assert.notOk(err, 'get_pipelines should not produce an error');
														assert.deepEqual(msg, {pipe: {services: [{'service': 'fwriter'}], active: true}}, 'our previously created pipeline should be present');
														mc.shutdown_service({name: 'fwriter'}, function(err, msg) {
															assert.notOk(err, 'shutdown_service should not return an error');
														});
													});
												});
											});
										}, 100);
									}, 200);
								});
							});
						});
					});
				});
			});
		});
	});
});
