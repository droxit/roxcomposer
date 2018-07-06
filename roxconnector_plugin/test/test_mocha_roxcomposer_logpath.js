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

Spawn = function () {
	this.on = (function(ev, cb) { return this; }).bind(this);
}

let spawnMock = {
	spawn: function(...args) {
		return new Spawn();
	}
}

mockery.registerMock('child_process', spawnMock);

describe('logpath settings', function () {

	before(() => { mockery.enable({warnOnUnregistered: false}); });
	after(() => { mockery.disable(); });
	beforeEach(() => {
		mc = {};
		require('../roxcomposer_control.js')(mc);
	});

	it('without logpath without default', function () {
		mc.init();
		let serv_args = {
			path: 'roxcomposer_control.js', // we need an existing file
			params: {
			    name: 'test-service',
				ip: '127.0.01',
				port: 1234
			}
		}
		mc.start_service(serv_args, (err, msg) => {
			expect(err).to.be(null);
			mc.get_services(null, (err, services) => {
				expect(err).to.be(null);
				expect(services['test-service']).to.eql(serv_args);
			});
		});
	});
	it('with logpath pointing to a valid file', function () {
		mc.init();
		let serv_args = {
			path: 'roxcomposer_control.js', // we need an existing file
			params: {
			    name: 'test-service',
				ip: '127.0.01',
				port: 1234,
				logging: { logpath: 'roxcomposer_control.js' }
			}
		}
		mc.start_service(serv_args, (err, msg) => {
			expect(err).to.be(null);
			mc.get_services(null, (err, services) => {
				expect(err).to.be(null);
				expect(services['test-service']).to.eql(serv_args);
			});
		});
	});
	it('with logpath pointing to an existing directory', function () {
		mc.init();
		let serv_args = {
			path: 'roxcomposer_control.js', // we need an existing file
			params: {
			    name: 'test-service',
				ip: '127.0.01',
				port: 1234,
				logging: { logpath: '..' }
			}
		}
		mc.start_service(serv_args, (err, msg) => {
			expect(err).to.be(null);
			mc.get_services(null, (err, services) => {
				expect(err).to.be(null);
				expect(services['test-service'].params.logging.logpath).to.eql('../test-service.log');
			});
		});
	});
	it('with a default logpath set to an existing directory', function () {
		mc.init({ default: { logging: { logpath: '..' } } });
		let serv_args = {
			path: 'roxcomposer_control.js', // we need an existing file
			params: {
			    name: 'test-service',
				ip: '127.0.01',
				port: 1234,
			}
		}
		mc.start_service(serv_args, (err, msg) => {
			expect(err).to.be(null);
			mc.get_services(null, (err, services) => {
				expect(err).to.be(null);
				expect(services['test-service'].params.logging.logpath).to.eql('../test-service.log');
			});
		});
	});
	it('with a default logpath set to an non-existing file in an existing directory', function () {
		mc.init({ default: { logging: { logpath: '../loggi.log' } } });
		let serv_args = {
			path: 'roxcomposer_control.js', // we need an existing file
			params: {
			    name: 'test-service',
				ip: '127.0.01',
				port: 1234,
			}
		}
		mc.start_service(serv_args, (err, msg) => {
			expect(err).to.be(null);
			mc.get_services(null, (err, services) => {
				expect(err).to.be(null);
				expect(services['test-service'].params.logging.logpath).to.eql('../loggi.log');
			});
		});
	});
	it('with a default logpath set to a bogus path should fail', function () {
		mc.init({ default: { logging: { logpath: '/totally/bogus/loggi.log' } } });
		let serv_args = {
			path: 'roxcomposer_control.js', // we need an existing file
			params: {
			    name: 'test-service',
				ip: '127.0.01',
				port: 1234,
			}
		}
		mc.start_service(serv_args, (err, msg) => {
			expect(err).to.be.ok();
		});
	});
});
