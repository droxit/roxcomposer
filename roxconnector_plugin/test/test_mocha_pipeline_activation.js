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
let mockery = require('mockery');

let mc = {};


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

mockery.registerMock('child_process', spawnMock);

describe('pipeline activation/deactivation', function () {

	before(() => { mockery.enable({warnOnUnregistered: false}); });
	after(() => { mockery.disable(); });
	beforeEach(() => {
		mc = {};
		require('../roxcomposer_control.js')(mc);
	});

	it('pipelines should only be active when all of their services are active', function () {
		mc.init({logger: logger});
		let s1_args = {
			path: 'roxcomposer_control.js', // we need an existing file
			params: {
			    name: 's1',
				ip: '127.0.01',
				port: 1234
			}
		}

		let s2_args = {
			path: 'roxcomposer_control.js', // we need an existing file
			params: {
			    name: 's2',
				ip: '127.0.01',
				port: 1235
			}
		}
		mc.start_service(s1_args, (err, msg) => {expect(err).to.be(null);});
		mc.start_service(s2_args, (err, msg) => {expect(err).to.be(null);});
		mc.set_pipeline({ name: 'p', services: ['s1', 's2']}, (err, msg) => {expect(err).to.be(null);});
		mc.get_pipelines(null, (err, pipelines) => {
			expect(err).to.be(null);
			expect(pipelines.p.active).to.be(true);
			mc.shutdown_service({name: 's1'}, (err, msg) => {
				expect(err).to.be(null);
				mc.get_pipelines(null, (err, pipelines) => {
					expect(err).to.be(null);
					expect(pipelines.p.active).to.be(false);
				});
				mc.shutdown_service({name: 's2'}, (err, msg) => {
					expect(err).to.be(null);
					mc.get_pipelines(null, (err, pipelines) => {
						expect(err).to.be(null);
						expect(pipelines.p.active).to.be(false);
						mc.start_service(s1_args, (err, msg) => {
							expect(err).to.be(null);
							mc.get_pipelines(null, (err, pipelines) => {
								expect(err).to.be(null);
								expect(pipelines.p.active).to.be(false);
								mc.start_service(s2_args, (err, msg) => {
									expect(err).to.be(null);
									mc.get_pipelines(null, (err, pipelines) => {
										expect(err).to.be(null);
										expect(pipelines.p.active).to.be(true);
									});
								});
							});
						});
					});
				});
			});
		});
	});
});
