let expect = require('expect.js');
let describe = require('mocha').describe;
let bunyan = require('bunyan');
let it = require('mocha').it;
let path = require('path');
let sleep = require('system-sleep');
let fs = require('fs');
let mc = {};
require('../mosaic_control.js')(mc);

let logger = bunyan.createLogger({
				name: 'mosaic-control-testing',
				streams: [{level: 'fatal', path: '/dev/null'}]
			});

describe('mosaic control integration tests', function () {
    let tmpdir = fs.mkdtempSync('/tmp/mosaic_control_test_integration');
    mc.init({logger: logger});
	describe('service startup and control', function () {
        let filepath = tmpdir + "/file_writer.out";
        let filewriter_params = {name: 'fwriter', ip: '127.0.0.1', port: 6789, filepath: filepath};
        let filewriter_module_path = '../mosaic/tests/classes/file_writer.py';
        let test_msg = 'test _mesage from hell'
		it('should return no error when starting FileWriter with proper arguments', function (done) {
			mc.start_service({path: filewriter_module_path, params: filewriter_params}, function (err, msg) {
				if (err)
					done(err);
				else
					done();
			});
		});
        it('should list the service in the services', function () {
            mc.get_services(null, function(err, msg) {
                expect(err).to.be(null);
                expect(msg).to.eql({fwriter: {path: filewriter_module_path, params: filewriter_params}});
            });
		});
        it('should be able to create a pipeline', function () {
			mc.set_pipeline({name: 'pipe', services: ['fwriter']}, function (err, msg) {
                expect(err).to.be(null);
			});
		});
        it('should list the pipeline in pipelines', function () {
			mc.get_pipelines(null, function (err, msg) {
                expect(err).to.be(null);
                expect(msg).to.eql({pipe: {services: ['fwriter'], active: true}});
			});
		});
        it('should be able to post a message to the pipeline', function () {
            sleep(400);
			mc.post_to_pipeline({name: 'pipe', data: test_msg}, function (err, msg) {
                expect(err).to.be(null);
			});
		});
        it('should have written the test message into the output file', function () {
            sleep(300);
            expect(fs.readFileSync(filepath, 'utf8')).to.be(test_msg);
		});
        it('should be able to shutdown the service', function () {
            mc.shutdown_service({name: 'fwriter'}, function(err, msg) {
                expect(err).to.be(null);
            });
		});
        it('services should now be empty', function () {
            mc.get_services(null, function(err, msg) {
                expect(err).to.be(null);
                expect(msg).to.eql({});
            });
		});
        it('the pipeline should be inactive', function () {
            mc.get_pipelines(null, function(err, msg) {
                expect(err).to.be(null);
                expect(msg.pipe.active).to.be(false);
            });
		});
        it('posting to the pipeline should return an error', function () {
            mc.post_to_pipeline({name: 'pipe', data: 'alfkajdf'}, function(err, msg) {
                expect(err.code).to.be.greaterThan(399);
            });
		});
	});
});
