//
// Test Classe test_roxcomposer_control: standard test for roxcomposer functionalities
//
// |------------------- OPEN SOURCE LICENSE DISCLAIMER -------------------|
// |                                                                      |
// | Copyright (C) 2019  droxIT GmbH - devs@droxit.de                     |
// |                                                                      |
// | This file is part of ROXcomposer.                                    |
// |                                                                      |
// | ROXcomposer is free software: you can redistribute it and/or modify  |
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
const {
	sep
} = require('path');

let logger = bunyan.createLogger({
	name: 'roxcomposer-control-testing',
	streams: [{
		level: 'fatal',
		path: '/dev/null'
	}]
});

Spawn = function() {
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

let Socket = function(){
    this.connect = function(x, cb) {
        cb();
	};
	this.end =  function(...args) {

	};
	this.on = function(...args) {

	};
}

let spawnMock = {
	spawn: function(...args) {
		return new Spawn();
	}
}

let netMock = {
	Socket: function() {
	    return new Socket();
	}
}

let fsMock = {
	accessSync: function(path) {
		if (path === 'exists')
			return true;

		throw "file not found";
	},
	statsSync: function(path) {
		return {
			isDirectory: false
		};
	},
	readFileSync: function(path) {
		if (path === 'pipe_file.json')
			return '{"name": "pipe_test", "services": ["html_generator_test", "file_writer_test"]}';
		else
			throw "file not found";
	}
}

mockery.registerMock('child_process', spawnMock);
mockery.registerMock('fs', fsMock);
mockery.registerMock('net', netMock);

let pipeline_config = {"name": "pipe_test", "services": ["html_generator_test", "file_writer_test"]};
let mc;


let running_services = [{
	'path': 'exists',
        'params': {
            'name': 'html_generator',
            'ip': '127.0.0.1',
            'port': 1234
	}
}, {
	'path': 'exists',
        'params': {
            'name': 'file_writer',
            'ip': '127.0.0.1',
            'port': 1235
	}
}];

describe("service_parameter tests", function() {

	before(() => { mockery.enable({warnOnUnregistered: false}); });
	after(() => { mockery.disable(); });
	beforeEach(() => {
	    mc = {};
	    require('../roxcomposer_control.js')(mc);
	    mc.init({logger: logger});

	    running_services.forEach((rs) => {
			mc.start_service(rs, () => {});
		});
	});
	afterEach(() => {
	    running_services.forEach((rs) => {
			mc.shutdown_service(rs, () => {});
		});
	});

    describe("set_pipeline() errors when setting with service params", function() {
        it('Setting up a pipeline with invalid service jsons should return malformed error with code >= 400', function (done) {
            mc.set_pipeline({name: 'test', services: [['service', 'html_generator', 'params', 'someparam']]}, function (err) {
                if (err.code >= 400) {
                    done()
                } else {
                    done(err);
                }
            })
        });

        it('Check if setting up a pipeline with service objects works (without params)', function (done) {

            mc.set_pipeline({name: 'blorbblub', services: [{'service': 'html_generator'}, {'service': 'file_writer'}]}, function (err) {
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

        it('Check if setting up a pipeline with service objects works (with params)', function (done) {
            mc.set_pipeline({name: 'blorbblub2', services: [{'service': 'html_generator', 'params': 'someparam'}]}, function (err) {
                if (err === null) {
                    mc.get_pipelines({}, (args, pipelines) => {
                        if (pipelines['blorbblub2']['active']) {
                            done();
                        }
                    });
                } else {
                    done(err);
                }
            })
        });
    });

    describe('post_to_pipeline() errors when having set the pipeline with service params', function () {
		it('posting to pipe should return message: pipeline initiated', function () {
			mc.set_pipeline({name: 'blorp', services: [{'service': 'html_generator'}, {'service': 'file_writer'}]}, (err2)=>{
			    expect(err2).to.be(null);
                mc.post_to_pipeline({name: 'blorp'}, function (err, res) {
                    expect(err).to.be(null);
                    expect(res).to.have.property('message','pipeline initiated');
                    expect(res).to.have.property('message_id');
                });
            });
		});
	});
});
