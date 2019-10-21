/*
 * Class LogSession: Session management for log observation
 * a log session has a uuid and buffers up to nlines lines
 * accross all observed files
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

