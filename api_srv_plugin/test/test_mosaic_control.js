let expect = require('expect.js');
let describe = require('mocha').describe;
let bunyan = require('bunyan');
let it = require('mocha').it;
let path = require('path');
let mc = {};
require('../mosaic_control.js')(mc);

describe('mosaic_control', function () {
	describe('init()', function () {
		it('should work without passing any arguments', function () {
			mc.init();
		});
	});
	describe('init()', function () {
		it('should work with a bunyan logger', function () {
			let logger = bunyan.createLogger({
				name: 'mosaic-control-testing',
				streams: [{level: 'fatal', path: '/dev/null'}]
			});
			mc.init({logger: logger});
		});
	});
	describe('start_service()', function () {
		it('should raise an exception if invoked without proper arguments', function () {
			expect(mc.start_service).to.throwError();
		});
		it('should raise an exception if invoked without a callback function', function () {
			expect(mc.start_service).withArgs({}).to.throwError();
		});
		it('should raise an exception if cb is not a function', function () {
			expect(mc.start_service).withArgs({}, {}).to.throwError();
		});
		it('should should return an error code >= 400 when invoked without a path or classpath in args', function (done) {
			mc.start_service({}, function (err) {
				if (err.code >= 400)
					done();
				else
					done(err);
			});
		});
		it('should should return an error code >= 400 when invoked without a non-existing path in args', function (done) {
			mc.start_service({path: '/bogus/path/from/hell', params: {}}, function (err) {
				if (err.code >= 400)
					done();
				else
					done(err);
			});
		});
	});
	describe('post_to_pipeline()', function () {
		it('should should return an error code >= 400 when invoked with an invalid pipeline name', function (done) {
			mc.post_to_pipeline({pipeline: 'blorp'}, function (err) {
				if (err.code >= 400)
					done();
				else
					done(err);
			});
		});
	});
	describe('set_pipeline()', function () {
		it('should should return an error code >= 400 when invoked without services parameter', function (done) {
			mc.set_pipeline({name: 'blorp'}, function (err) {
				if (err.code >= 400)
					done();
				else
					done(err);
			});
		});
		it('should should return an error code >= 400 when invoked with an empty service array', function (done) {
			mc.set_pipeline({name: 'blorp', services: []}, function (err) {
				if (err.code >= 400)
					done();
				else
					done(err);
			});
		});
		it('should should return an error code >= 400 when invoked with a a non-existant service in service array', function (done) {
			mc.set_pipeline({name: 'blorp', services: ['no-there']}, function (err) {
				if (err.code >= 400)
					done();
				else
					done(err);
			});
		});
		// TODO comment in if circleCi container can handle python and node at once
		// it('should contain an active state when a pipeline is created', function (done) {
		// 	mc.start_service({
		// 		'path': path.resolve(__dirname, '../../mosaic/tests/classes/html_generator.py'),
		// 		'params': {
		// 			'name': 'html_generator',
		// 			'ip': '127.0.0.1',
		// 			'port': 1234
		// 		}
		// 	}, function (err) {
		// 		if (err && err.code === 400) {
		// 			done(err);
		// 		}
		// 	});
		// 	mc.start_service({
		// 		'path': path.resolve(__dirname, '../../mosaic/tests/classes/file_writer.py'),
		// 		'params': {
		// 			'name': 'file_writer',
		// 			'ip': '127.0.0.1',
		// 			'port': 2345
		// 		}
		// 	}, function (err) {
		// 		if (err && err.code === 400) {
		// 			done(err);
		// 		}
		// 	});
		// 	mc.set_pipeline({name: 'blorbblub', services: ['html_generator', 'file_writer']}, function (err) {
		// 		if (err === null) {
		// 			mc.get_pipelines({}, (args, pipelines) => {
		// 				if (pipelines['blorbblub']['active']) {
		// 					done();
		// 				}
		// 			});
		// 		} else {
		// 			done(err);
		// 		}
		// 	})
		// });
	});
	describe('shutdown()', function () {
		it('should raise an exception if invoked without proper arguments', function () {
			expect(mc.shutdown_service).to.throwError();
		});
		it('should raise an exception if invoked without a callback function', function () {
			expect(mc.shutdown_service).withArgs({}).to.throwError();
		});
		it('should raise an exception if cb is not a function', function () {
			expect(mc.shutdown_service).withArgs({}, {}).to.throwError();
		});
		// TODO comment in if services started above are running
		// it('should return an error code >= 400 when invoked with a non-existent service', function (done) {
		// 	mc.shutdown_service({'name': 'blurblurb'}, function (err) {
		// 		if (err && err.code >= 400) {
		// 			done();
		// 		} else {
		// 			done(err)
		// 		}
		// 	});
		// });
		// it('should shutdown a test service', function (done) {
		// 	mc.shutdown_service({'name': 'html_generator'}, function (err) {
		// 		if (err && err.code >= 400) {
		// 			done(err);
		// 		} else {
		// 			done();
		// 		}
		// 	});
		// });
		// it('should shutdown the last test service and set its\' pipeline state to inactive', function (done) {
		// 	mc.shutdown_service({'name': 'file_writer'}, function (err) {
		// 		if (err && err.code >= 400) {
		// 			done(err);
		// 		} else {
		// 			mc.get_pipelines({}, (args, pipelines) => {
		// 				if (!pipelines['blorbblub']['active']) {
		// 					done();
		// 				} else {
		// 					done('Pipeline was not set to inactive');
		// 				}
		// 			});
		// 		}
		// 	});
		// })
	});
});
