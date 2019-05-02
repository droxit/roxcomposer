/*
 * Test Classe test_roxcomposer_control: standard test for roxcomposer functionalities
 *
 * |------------------- OPEN SOURCE LICENSE DISCLAIMER -------------------|
 * |                                                                      |
 * | Copyright (C) 2019  droxIT GmbH - devs@droxit.de                     |
 * |                                                                      |
 * | This file is part of ROXcomposer.                                    |
 * |                                                                      |
 * | ROXcomposer is free software: you can redistribute it and/or modify  |
 * | it under the terms of the GNU Lesser General Public License as       |
 * | published by the Free Software Foundation, either version 3 of the   |
 * | License, or (at your option) any later version.                      |
 * |                                                                      |
 * | This program is distributed in the hope that it will be useful,      |
 * | but WITHOUT ANY WARRANTY; without even the implied warranty of       |
 * | MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the         |
 * | GNU General Public License for more details.                         |
 * |                                                                      |
 * | You have received a copy of the GNU Lesser General Public License    |
 * | along with this program. See also <http://www.gnu.org/licenses/>.    |
 * |                                                                      |
 * |----------------------------------------------------------------------|
 */

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
