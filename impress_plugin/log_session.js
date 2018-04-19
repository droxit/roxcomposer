//
// Class LogSession: Session management for log observation
// a log session has a uuid and 
//
// devs@droxit.de - droxIT GmbH
//
// Copyright (c) 2018 droxIT GmbH
//

let uuid = require('uuid/v4');
let logobs = require('./log_observer.js');

module.exports = LogSession;

function LogSession(lines) {
	this.id = uuid();
	this.nlines = lines;
	this.lines = [];
	this.filters = [];
	this.receive_lines = receive_lines.bind(this);
	this.watch_files = watch_files.bind(this);
	this.unwatch_files = unwatch_files.bind(this);
	this.cleanup = cleanup.bind(this);
	this.get_lines = get_lines.bind(this);
	this.logobs = new logobs(this.receive_lines);
}

function watch_files(files) {
	return Promise.all(this.logobs.register.apply(this.logobs, files));
}

function unwatch_files(files) {
	this.logobs.unregister(files);
}

function receive_lines(lines) {
	let ln = lines;
	for (i in this.filters)
		ln = ln.filter(this.filters[i]);
	if (ln.length) {
		this.lines = this.lines.concat(lines);
		if (this.lines.length > this.nlines) {
			this.lines.splice(0, this.lines.length - this.nlines);
		}
	}
}

function get_lines() {
	let lines = this.lines;
	this.lines = [];

	return lines;
}

function cleanup() {
	this.logobs.unregister();
	this.lines = [];
}

