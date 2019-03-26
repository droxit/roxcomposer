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
