//
// Test Classe test_config_and_monitoring: standard test for login and monitoring functionalities from roxcomposer
//
// devs@droxit.de - droxIT GmbH
//
// Copyright (c) 2018 droxIT GmbH
//

let bunyan = require('bunyan');
let path = require('path');
let sleep = require('system-sleep');
let fs = require('fs');
let test = require('tape');
let tapSpec = require('tap-spec');
let os = require('os');
let logobs = require('../log_observer');
const EventEmitter = require('events');
const { sep } = require('path');
const { exec } = require('child_process');

test.createStream().pipe(tapSpec()).pipe(process.stdout);

let tmp = os.tmpdir();
fs.mkdtemp(`${tmp}${sep}`, (error, tmpdir) => {
	if (error) {
		throw error;
	}

	test('log observation', function (assert) {
		assert.plan(5);
		let logpath1 = path.join(tmpdir, "log1.log");
		let logpath2 = path.join(tmpdir, "log2.log");
		let emitter = new EventEmitter();

		let lines = [];

		let l = new logobs((ls) => {
			lines = ls;
			emitter.emit('lines_received');
		});

		// should be skipped by the log observer so the contents are irrelevant
		fs.writeFileSync(logpath1, "alfkja[30-r9u203fij3o2kj230ifju2fj");
		fs.writeFileSync(logpath2, "alfkja[30-r9u2kj230ifju2fj");

		proms = l.register(logpath1, logpath2);
		Promise.all([proms[logpath1], proms[logpath2]]).then(
			() => { assert.ok(true, "the promises for registering the files resolved"); },
			() => { console.log(proms); assert.ok(false, "the promises for registering the files did not resolve"); }
		);

		proms = l.register(logpath1, logpath2);
		Promise.all([proms[logpath1], proms[logpath2]]).then(
			() => { assert.ok(true, "the promises for re-registering the files resolved"); },
			() => { console.log(proms); assert.ok(false, "the promises for re-registering the files did not resolve"); }
		);

		let line = "this is a full line\nthis is a partial";
		let expected = ["this is a full line"];

		emitter.on('lines_received', () => {
			assert.deepEqual(lines, expected, "full lines should be returned, and partial lines skipped");
		});

		let n = 1;
		let interval = 200;

		setTimeout(() => {
			exec(`echo -n '${line}' >> ${logpath1}`);
		}, n++ * interval);

		setTimeout(() => {
			line = ' line';
			expected = ["this is a partial line"];
			exec(`echo '${line}' >> ${logpath1}`);
		}, n++ * interval);

		setTimeout(() => {
			l.unregister(logpath1, logpath2);
		}, n++ * interval);

		setTimeout(() => {
			let p = l.register('bogus/path');
			Promise.all(p).then(() => { assert.ok(false, 'returned promise should not be resolved'); }, () => { assert.ok(true, 'promise for opening non existant file was rejected'); });
		}, n++ * interval);
	});
});
