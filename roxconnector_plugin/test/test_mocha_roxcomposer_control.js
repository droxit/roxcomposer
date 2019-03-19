//
// Test Classe test_roxcomposer_control: standard test for roxcomposer functionalities
//
// devs@droxit.de - droxIT GmbH
//
// Copyright (c) 2018 droxIT GmbH
//
let expect = require('expect.js');
let describe = require('mocha').describe;
let bunyan = require('bunyan');
let it = require('mocha').it;
let path = require('path');
let sleep = require('system-sleep');
let fs = require('fs');
let os = require('os');
let mockery = require('mockery');
let tmp = os.tmpdir();
const { sep } = require('path');

let logger = bunyan.createLogger({
	name: 'roxcomposer-control-testing',
	streams: [{level: 'fatal', path: '/dev/null'}]
});

Spawn = function () {
	this.ev_map = {};
	this.on = (function(ev, cb) {
		if (ev in this.ev_map)
			this.ev_map[ev].push(cb);
		else
			this.ev_map[ev] = [cb];
		return this;
	}).bind(this);

	this.kill = (function(sig) {
		if (sig === 'SIGTERM' && ('exit' in this.ev_map))
			this.ev_map.exit.forEach(cb => cb(0, 'SIGTERM'));
	}).bind(this);
}

let spawnMock = {
	spawn: function(...args) {
		return new Spawn();
	}
}

let fsMock = {
	accessSync: function (path) {
		if (path === 'exists')
			return true;

		throw "file not found";
	},
	statsSync: function (path) {
		return { isDirectory: false };
	},
	readFileSync: function (path) {
		if (path === 'pipe_file.json')
			return '{"name": "pipe_test", "services": ["html_generator_test", "file_writer_test"]}';
		else
			throw "file not found";
	}
}

mockery.registerMock('child_process', spawnMock);
mockery.registerMock('fs', fsMock);

let pipeline_config = {"name": "pipe_test", "services": ["html_generator_test", "file_writer_test"]};
let mc;

describe('roxcomposer_control', function () {

	before(() => { mockery.enable({warnOnUnregistered: false}); });
	after(() => { mockery.disable(); });
	beforeEach(() => { mc = {}; require('../roxcomposer_control.js')(mc); mc.init({logger: logger}); });

	describe('new roxcomposer_control()', function () {
		it('should work without passing any arguments', function () {
			mc = {};
			require('../roxcomposer_control.js')(mc);
			mc.init();
		});
	});

	describe('start_service() errors', function () {
		it('should raise an exception if invoked without proper arguments', function () {
			expect(mc.start_service).to.throwError();
		});
		it('should raise an exception if invoked without a callback function', function () {
			expect(mc.start_service).withArgs({}).to.throwError();
		});
		it('should raise an exception if cb is not a function', function () {
			expect(mc.start_service).withArgs({}, {}).to.throwError();
		});
		it('should return an error code >= 400 when invoked without a path or classpath in args', function (done) {
			mc.start_service({}, function (err) {
				if (err.code >= 400)
					done();
				else
					done(err);
			});
		});
		it('should return an error code >= 400 when invoked with a classpath without initializing a class loader path', function (done) {
			mc.start_service({classpath: 'not_important'}, function (err) {
				if (err.code >= 400)
					done();
				else
					done(err);
			});
		});
		it('should return an error code >= 400 when invoked without a non-existing path in args', function (done) {
			mc.start_service({path: '/bogus/path/from/hell', params: {}}, function (err) {
				if (err.code >= 400)
					done();
				else
					done(err);
			});
		});
	});

	describe('post_to_pipeline() errors', function () {
		it('should return an error code >= 400 when invoked with an invalid pipeline name', function (done) {
			mc.post_to_pipeline({pipeline: 'blorp'}, function (err) {
				if (err.code >= 400)
					done();
				else
					done(err);
			});
		});
	});

	describe('delete_pipeline() errors', function () {
		it('should return an error code >= 400 when invoked without a pipeline name', function (done) {
			mc.delete_pipeline({}, function (err) {
				if (err.code >= 400)
					done();
				else
					done(err);
			});
		});
		it('should return an error code >= 400 when invoked with an pipeline name that does not exist', function (done) {
			mc.delete_pipeline({'name': 'blorp'}, function (err) {
				if (err.code >= 400)
					done();
				else
					done(err);
			});
		});

		it('should return an object with a message that pipe was deleted', function (done) {
			mc.start_service({
				'path': 'exists',
				'params': {
					'name': 'html_generator',
					'ip': '127.0.0.1',
					'port': 1234
				}
			}, () => {});
			mc.set_pipeline({name: 'test', services: ['html_generator']}, () => {});

			mc.delete_pipeline({'name': 'test'}, function (err, res) {
				if (expect(res.message).to.eql("pipeline [test] deleted") && err === null)
					done();
				else
					done(res);
			});
		});

	});

	describe('set_pipeline() errors', function () {
		it('should return an error code >= 400 when invoked without services parameter', function (done) {
			mc.set_pipeline({name: 'blorp'}, function (err) {
				if (err.code >= 400)
					done();
				else
					done(err);
			});
		});
		it('should return an error code >= 400 when invoked with an empty service array', function (done) {
			mc.set_pipeline({name: 'blorp', services: []}, function (err) {
				if (err.code >= 400)
					done();
				else
					done(err);
			});
		});
		it('should return an error code >= 400 when invoked with a a non-existant service in service array', function (done) {
			mc.set_pipeline({name: 'blorp', services: ['no-there']}, function (err) {
				if (err.code >= 400)
					done();
				else
					done(err);
			});
		});
	});
	describe('set_pipeline()', function () {
		it('should contain an active state when a pipeline is created', function (done) {
			mc.start_service({
				'path': 'exists',
				'params': {
					'name': 'html_generator',
					'ip': '127.0.0.1',
					'port': 1234
				}
			}, function (err) {
				if (err) {
					done(err);
					return;
				}
			});
			mc.start_service({
				'path': 'exists',
				'params': {
					'name': 'file_writer',
					'ip': '127.0.0.1',
					'port': 2345
				}
			}, function (err) {
				if (err) {
					done(err);
					return;
				}
			});
			mc.set_pipeline({name: 'blorbblub', services: ['html_generator', 'file_writer']}, function (err) {
				if (err === null) {
					mc.get_pipelines({}, (args, pipelines) => {
						if (pipelines['blorbblub']['active']) {
							done();
						}
					});
				} else {
					done(err);
				}
			})
		});
	});

	describe('shutdown() errors', function () {
		it('should raise an exception if invoked without proper arguments', function () {
			expect(mc.shutdown_service).to.throwError();
		});
		it('should raise an exception if invoked without a callback function', function () {
			expect(mc.shutdown_service).withArgs({}).to.throwError();
		});
		it('should raise an exception if cb is not a function', function () {
			expect(mc.shutdown_service).withArgs({}, {}).to.throwError();
		});
		it('should return an error code >= 400 when invoked with a non-existent service', function (done) {
			mc.shutdown_service({'name': 'blurblurb'}, function (err) {
				if (err && err.code >= 400) {
					done();
				} else {
					done(err)
				}
			});
		});
	});

	describe('load_and_start_pipeline()', function () {
		it('should return an error code >= 400 when invoked without pipeline_path parameter', function (done) {
			mc.load_and_start_pipeline({}, function (err) {
				if (err.code >= 400)
					done();
				else
					done(err);
			});
		});
		it('should return an error code >= 400 when invoked with an empty pipeline_path', function (done) {
			mc.load_and_start_pipeline({pipe_path: ' ', services: []}, function (err) {
				if (err.code >= 400)
					done();
				else
					done(err);
			});
		});
		it('should return an error code >= 400 when invoked with a a non-existant pipeline_path', function (done) {
			mc.load_and_start_pipeline({pipe_path: 'dsdasd'}, function (err) {
				if (err.code >= 400)
					done();
				else
					done(err);
			});
		});

		it('should work with default values', function (done) {
			let default_values = {
				"logging": {
					"logpath": "pipeline.log",
					"level": "INFO"
				},
				"monitoring": {
					"filename": "monitoring.log",
					"monitor_class": "roxcomposer.monitor.basic_monitoring.BasicMonitoring"
				}
			}
			let mc_def = {};
			require('../roxcomposer_control.js')(mc_def);
			mc_def.init({logger: logger, default: default_values});

			mc_def.start_service({
				'path': 'exists',
				'params': {
					'name': 'html_generator_default',
					'ip': '127.0.0.1',
					'port': 1772
				}
			}, function (err) {
				if (err && err.code === 400) {
					done(err);
					return;
				}

				mc_def.get_services({}, (err, services) => {
					if (err) {
						done(err);
					} else {
						if ((!services['html_generator_default']['params'].hasOwnProperty("logging")) ||
							(!services['html_generator_default']['params'].hasOwnProperty("monitoring")) ) {
							done("Default values are not passed.");
						} else
							done()
					}
				});
			});

		});

		it('should contain an active state when a pipeline is created', function (done) {
			let service_startup_error = false;
			mc.start_service({
				'path': 'exists',
				'params': {
					'name': 'html_generator_test',
					'ip': '127.0.0.1',
					'port': 1235
				}
			}, function (err) {
				if (err && err.code === 400) {
					done(err);
					return;
				}
			});
			mc.start_service({
				'path': 'exists',
				'params': {
					'name': 'file_writer_test',
					'ip': '127.0.0.1',
					'port': 3456
				}
			}, function (err) {
				if (err && err.code === 400) {
					done(err);
					service_startup_error = true;
				}
			});

			if(service_startup_error == false) {
				mc.load_and_start_pipeline({pipe_path: 'pipe_file.json'}, function (err) {
					if (err === null) {
						mc.get_pipelines({}, (args, pipelines) => {
							if (pipelines['pipe_test']['active']) {
								done();
							}
						});
					} else {
						done(err);
					}
				});
			}
			sleep(100);
			if(service_startup_error == false)
				mc.shutdown_service({'name': 'html_generator_test'}, function (err) {});
			mc.shutdown_service({'name': 'file_writer_test'}, function (err) {});
		});
	});
});

