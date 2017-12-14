let bunyan = require('bunyan');
let path = require('path');
let sleep = require('system-sleep');
let fs = require('fs');
let test = require('tape');
let tapSpec = require('tap-spec');

test.createStream().pipe(tapSpec()).pipe(process.stdout);

let logger = bunyan.createLogger({
				name: 'mosaic-control-testing',
				streams: [{level: 'fatal', path: '/dev/null'}]
			});
let filewriter_module_path = '../mosaic/tests/classes/file_writer.py';
let tmpdir = fs.mkdtempSync('/tmp/mosaic_control_test_integration');

test('service startup and control', function (assert) {
	let filepath = tmpdir + "/file_writer.out";
	let filewriter_params = {name: 'fwriter', ip: '127.0.0.1', port: 6789, filepath: filepath};
	let test_msg = 'test _mesage from hell';
	let mc = {}
	require('../mosaic_control.js')(mc);
	mc.init({logger: logger});

	assert.plan(12);
	mc.start_service({path: filewriter_module_path, params: filewriter_params}, function (err, msg) {
		assert.notOk(err, "start_service should not return an error");
		sleep(200);
		mc.get_services(null, function(err, msg) {
			assert.notOk(err, "get_services should not return an error");
			assert.deepEqual(msg, {fwriter: {path: filewriter_module_path, params: filewriter_params}}, "the started service should be listed with it's parameters");
			mc.set_pipeline({name: 'pipe', services: ['fwriter']}, function (err, msg) {
				assert.notOk(err, 'creating a pipeline with the new service should not produce an error');
				mc.get_pipelines(null, function (err, msg) {
					assert.notOk(err, 'get_pipelines should not produce an error');
					assert.deepEqual(msg, {pipe: {services: ['fwriter'], active: true}}, 'our created pipeline should be present');
					mc.post_to_pipeline({name: 'pipe', data: test_msg}, function (err, msg) {
						assert.notOk(err, 'post_to_pipeline should not produce an error');
						sleep(200);
						assert.equal(fs.readFileSync(filepath, 'utf8'), test_msg, 'the file_writer service should have written our test message into the file');
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
							}, 200);
						});
					});
				});
			});
		});
	});
});

