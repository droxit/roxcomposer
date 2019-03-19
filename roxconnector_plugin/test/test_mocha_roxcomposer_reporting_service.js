//
// test the ROXcomposer reporting service
//
// devs@droxit.de - droxIT GmbH
//
// Copyright (c) 2019 droxIT GmbH
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
}, {
	'path': 'exists',
        'params': {
            'name': 'basic_reporting',
            'ip': '127.0.0.1',
            'port': 1236
	}
}
];

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

    describe("basic_reporting", function() {
        it('Setting up a pipeline with invalid service jsons should return malformed error with code >= 400', function (done) {
            mc.set_pipeline({name: 'blorp', services: [{'service': 'html_generator'}, {'service': 'file_writer'}]}, ()=>{});
            mc.shutdown_service({name: 'basic_reporting'}, function(err, msg) {
                expect(err).to.be(null);
            });
            mc.get_msg_status({}, (err, msg) => {
                if(err.code >= 400){
                    done()
                } else {
                    done(err);
                }
            });
        });
    });
});