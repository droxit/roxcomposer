//
// LogObserver - Watch logfiles and notify registered callbacks
//
// devs@droxit.de - droxIT GmbH
//
// Copyright (c) 2018 droxIT GmbH
//
// usage: const logobs = require('./log_observer');
//        let observer = new logobs(callback);
//        observer.register(file1, file2, ...);
//        /* callback will be called with new log lines as they arrive */
//        /* unregister when you're done */
//        observer.unregister(file1, file2, ...);


let fs = require('fs');
let _files = {};

// constructor
module.exports = function (cb) {
	this.register = register.bind(this);
	this.unregister = unregister.bind(this);
	this.files = new Set();
	this.cb = cb;
}

// add files to be watched
function register(...files) {
	let proms = []; 
	files.forEach((f) => {
		if (this.files.has(f))
			return;
		if (!(f in _files)) {
			_files[f] = new FileListener();
			proms.push(_files[f].watch(f));
		} else {
			proms.push(Promise.resolve());
		}
		_files[f].subscribers.add(this);
		this.files.add(f);
	});

	return proms;
}

// remove files from watch list
function unregister(...files) {
	// if called without any arguments we unregister all files
	if (files.length == 0)
		files = this.files;

	files.forEach((f) => {
		if (this.files.has(f) && (f in _files)) {
			_files[f].subscribers.delete(this);
			this.files.delete(f);

			if (_files[f].subscribers.size === 0) {
				_files[f].cleanup();
				delete _files[f];
			}
		}
	});
}

// class for observing a single file - takes an optional buffer size
function FileListener(bufsize=2048) {
	this.cleanup = cleanup_listener.bind(this);
	this.subscribers = new Set();
	this.watcher = null;
	this.fd = null;
	this.watch = watch_file.bind(this);
	this.bufsize = bufsize; 
	this.buffer = Buffer.alloc(bufsize);
}

// watch a file
function watch_file(file) {
	let p = new Promise((resolve, reject) => {
		fs.open(file, 'r', (err, fd) => {
			if (err) {
				reject(err);
				return;
			}

			this.fd = fd;

			let offset = 0;
			fs.stat(file, (err, stats) => {
				if (err) {
					reject(err);
					return;
				}
				resolve();
				// skip to the end of the file
				let position = stats.size;
				this.watcher = fs.watch(file, {}, (eventType, _) => {
					if (eventType === 'change') {
						fs.read(fd, this.buffer, offset, this.bufsize - offset, position, (err, bytesRead) => {
							position += bytesRead;
							ret = read_lines(this.buffer.toString('utf-8', 0, offset + bytesRead));
							offset = this.buffer.write(ret.rest);
							this.subscribers.forEach((s) => {
								s.cb(ret.lines);
							});
						});
					}
				});
				this.watcher.on('error', (err) => { console.error(err); });
			});
		});
	});

	return p;
}

// cleanup 
function cleanup_listener() {
	this.watcher.close();
	fs.close(this.fd, () => {});
	this.watcher = null;
	this.fd = null;
}

// take a string and return all lines that end in a newline and the rest in { lines: [...], rest: "..." }
function read_lines(lines) {
	let ret = { rest: "", lines: [] };

	if (lines.length === 0)
		return ret;

	ret.lines = lines.split("\n");

	ret.rest = ret.lines.pop();

	return ret;
}

