//
// Class LogSession: Session management for log observation
// a log session has a uuid and buffers up to nlines lines
// accross all observed files
//
// devs@droxit.de - droxIT GmbH
//
// Copyright (c) 2018 droxIT GmbH
//

let uuid = require('uuid/v4');
let logobs = require('./log_observer.js');

module.exports = LogSession;

// constructor
function LogSession(nlines) {
	this.id = uuid();
	this.nlines = nlines;
	this.lines = [];
	this.filters = [];
	this.receive_lines = receive_lines.bind(this);
	this.watch_files = watch_files.bind(this);
	this.unwatch_files = unwatch_files.bind(this);
	this.cleanup = cleanup.bind(this);
	this.get_lines = get_lines.bind(this);
	this.logobs = new logobs(this.receive_lines);
}

// add files to observe to this session
function watch_files(files) {
	return Promise.all(this.logobs.register.apply(this.logobs, files));
}

// remove files from this session
function unwatch_files(files) {
	this.logobs.unregister(files);
}

// callback function for receiving lines from the LogObserver
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

// get buffered lines and clear buffer
function get_lines() {
	let lines = this.lines;
	this.lines = [];

	return lines;
}

// unregister all files from LogObserver and clear buffer
function cleanup() {
	this.logobs.unregister();
	this.lines = [];
}

