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

mockery.registerMock('child_process', spawnMock);




    describe('roxcomposer log-observation', function () {
        before(() => { mockery.enable({warnOnUnregistered: false}); });
        after(() => { mockery.disable(); });
        beforeEach(() => { mc = {}; require('../roxcomposer_control.js')(mc); mc.init({logger: logger, service_container: './roxcomposer_control.js'}); });

        it('should not crash when we have garbled input', function (done) {
            fs.mkdtemp(`${tmp}${sep}`, (err, tmpdir) => {
                if (err) {
                    throw err;
                }
                let logfile = path.join(tmpdir, 'testlog.log');
                fs.writeFileSync(logfile, '{"invalid": "f..fdf\n');

                mc.start_service(
                    {
                        'classpath': 'dlfkdfjl', 
                        'params': {
                            'name': 'test_service',
                            'logging': {
                                'logpath': logfile
                            }
                        }
                    },
                    (err) => {
                        expect(err).to.be(null);
                        mc.create_log_observer({lines: 10, timeout: 120}, (err, ret) => {
                            mc.post_services_to_logsession({'sessionid': ret.sessionid, 'services': ['test_service']}, (err, ml) => {
                                expect(err).to.be(null);
                                fs.writeFileSync(logfile, '{"invalid": "f..fdf\n', {'flag': 'a'});
                                setTimeout(() => {
                                    mc.delete_log_observer({'sessionid': ret.sessionid}, (err) => {
                                        done(err);
                                    });
                                }, 100);
                            });
                        });
                    });
            });
        });
});
