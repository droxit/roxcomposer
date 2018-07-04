//
// Class roxcomposer control: ROXconnector control plugin for ROXcomposer
//
// devs@droxit.de - droxIT GmbH
//
// Copyright (c) 2018 droxIT GmbH
//

let fs = require('fs');
let bunyan = require('bunyan');
let spawn = require('child_process').spawn;
let net = require('net');
let uuid = require('uuid/v4');
let path = require('path');
let roxcomposer_message = require('./roxcomposer_message.js');
let config_loader = require('./config_loader.js');
let LogSession = require('./log_session.js');

function __roxcomposer_control_private() {
	this.processes = {};
	this.services = {};
	this.pipelines = {};
	this.logger;
	this.service_container_path;
	this.reporting_service;
	this.logsessions = {};
	this.init = init.bind(this);
	this.check_args = check_args.bind(this);
	this.start_service = start_service.bind(this);
	this.create_roxcomposer_message = create_roxcomposer_message.bind(this);
	this.read_roxcomposer_message = read_roxcomposer_message.bind(this);
	this.post_to_pipeline = post_to_pipeline.bind(this);
	this.get_services = get_services.bind(this);
	this.get_pipelines = get_pipelines.bind(this);
	this.set_pipeline = set_pipeline.bind(this);
	this.shutdown_service = shutdown_service.bind(this);
	this.post_to_report_service = post_to_report_service.bind(this);
	this.get_msg_history = get_msg_history.bind(this);
	this.get_msg_status = get_msg_status.bind(this);
	this.dump_services_and_pipelines = dump_services_and_pipelines.bind(this);
	this.load_services_and_pipelines = load_services_and_pipelines.bind(this);
	this.load_and_start_pipeline = load_and_start_pipeline.bind(this);
	this.load_pipeline_json_file = load_pipeline_json_file.bind(this);
	this.start_pipeline = start_pipeline.bind(this);
	this.create_log_observer = create_log_observer.bind(this);
	this.check_services_and_logs = check_services_and_logs.bind(this);
	this.add_services_to_logsession = add_services_to_logsession.bind(this);
	this.set_logsession_timeout = set_logsession_timeout.bind(this);
	this.delete_log_observer = delete_log_observer.bind(this);
	this.get_log_lines = get_log_lines.bind(this);
	this.post_services_to_logsession = post_services_to_logsession.bind(this);
	this.default;
}

module.exports = function (container) {
	let mcp = new __roxcomposer_control_private();
	container['init'] = mcp.init;
	container['start_service'] = mcp.start_service;
	container['shutdown_service'] = mcp.shutdown_service;
	container['get_services'] = mcp.get_services;
	container['get_pipelines'] = mcp.get_pipelines;
	container['set_pipeline'] = mcp.set_pipeline;
	container['post_to_pipeline'] = mcp.post_to_pipeline;
	container['get_msg_history'] = mcp.get_msg_history;
	container['get_msg_status'] = mcp.get_msg_status;
	container['dump_services_and_pipelines'] = mcp.dump_services_and_pipelines;
	container['load_services_and_pipelines'] = mcp.load_services_and_pipelines;
	container['load_and_start_pipeline'] = mcp.load_and_start_pipeline;
	container['create_log_observer'] = mcp.create_log_observer;
	container['delete_log_observer'] = mcp.delete_log_observer;
	container['get_log_lines'] = mcp.get_log_lines;
	container['post_services_to_logsession'] = mcp.post_services_to_logsession;
};

/**
 * intialize this plugin
 * args needs to contain IP, port and the beginning of the portrange for the micro services
 **/
function init(args) {
	if (args && ('logger' in args))
		this.logger = args.logger;
	else
		this.logger = bunyan.createLogger({name: 'roxcomposer_control'});

	if (args && ('service_container' in args))
		this.service_container_path = args.service_container;

	if (this.service_container_path) {
		try {
			fs.accessSync(this.service_container_path);
		} catch (e) {
			let msg = `unable to access service container module at ${this.service_container_path} - ${e.message}`;
			throw new Error(msg);
		}
	}

	if (args && ('reporting_service' in args)) {
		this.start_service(args.reporting_service, (err) => {
			if (err) {
				let msg = err.message;
				throw new Error(msg);
			}
			this.reporting_service = args.reporting_service.params.name;
		});
	}

	this.service_config = false;
	if (args && ('default' in args)) {
		this.default = args.default;
	}

	try {
		this.service_config = new config_loader();
	} catch(e) {
		this.logger.fatal({error: e}, 'unable to load service config file');
		process.exit(1);
	}
}

/**
 * check arguments for the presence of fields
 * returns a list of missing fields
 **/
function check_args(args, fields) {
	let missing = fields.filter(f => !(f in args));
	if (missing.length)
		return `missing fields: [${missing.join(", ")}]`;
	else
		return false;
}

/**
 * spawn a new service
 * args need to contain the name of the service and the path to the service module
 **/
function start_service(args, cb) {
	this.logger.debug({args: args}, 'start_service called');
	let opt;

	// LOTS of argument checking ahead

	// basic stuff
	if (args === undefined)
		throw TypeError("start_service: 'args' must be a dictionary");
	if (typeof cb !== 'function')
		throw TypeError("start_service: 'cb' must be a function");

	// we either need a path to load the service module from ....
	if ('path' in args) {
		try {
			fs.accessSync(args.path);
			opt = [args.path];
		} catch (e) {
			cb({'code': 400, 'message': `start_service: path does not exist - ${args.path}`});
			return;
		}
	// ... or a classpath to utilize the python class loading utilities
	} else if ('classpath' in args) {
        if (this.service_container_path) {
		    opt = [this.service_container_path, args.classpath];
        } else {
		    cb({'code': 400, 'message': 'start_service: classpath argument given but path to service loader is not configured'});
		    return;
        }
	} else {
		cb({'code': 400, 'message': 'start_service: either a module path or a service class must be specified'});
		return;
	}

	if (!('params' in args)) {
		cb({'code': 400, 'message': 'start_service: params must be given - even if they are empty'});
		return;
	}

	// if a service key is present we try to retrieve the config via the config_loader and look up the key
	// this is necessary for the plugin to know the service's address
	if ('service_key' in args.params) {
		if ('config_file' in args.params) {
			let c;
			try {
				c = new config_loader(args.params.config_file);
			} catch(e) {
				cb({'code': 400, 'message': `start_service: unable to load config file ${args.params.config_file} - ${e}`});
				return;
			}
			try {
				args.params = c.get_item(args.params.service_key);
			} catch(e) {
				this.logger.error({error: e, key: args.params.service_key, config_file: args.params.config_file}, 'tried to access invalid service key in service config');
				cb({'code': 400, 'message': `invalid service key provided: ${args.params.service_key}`});
				return;
			}
		} else if (this.service_config) {
			try {
				args.params = this.service_config.get_item(args.params.service_key);
			} catch(e) {
				this.logger.error({error: e, key: args.params.service_key}, 'tried to access invalid service key in service config');
				cb({'code': 400, 'message': `invalid service key provided: ${args.params.service_key}`});
				return;
			}
		} else {
			cb({'code': 400, 'message': 'start_service: service key was provided but service config is not loaded'});
			return;
		}
	}

	if (!('name' in args.params)) {
		cb({'code': 400, 'message': 'start_service: a service name must be given'});
		return;
	}

	if (args.params.name in this.services) {
		cb({'code': 400, 'message': 'start_service: a service with that name already exists'});
		return;
	}

	for(let my_service in this.services) {
		if ((this.services[my_service].params.port == args.params.port) && (this.services[my_service].params.ip == args.params.ip)) {
			cb({'code': 400, 'message': `start_service: service ${my_service} is already registered under this address  (${args.params.ip},${args.params.port}`});
				return;
			}
	}

    // add default values if given to params if logging or monitoring is not set
    if(this.hasOwnProperty('default')) {
        if (!args.params.hasOwnProperty('logging') && this.default.hasOwnProperty('logging'))
            args.params.logging = this.default.logging;
        if (!args.params.hasOwnProperty('monitoring') && this.default.hasOwnProperty('monitoring'))
            args.params.monitoring = this.default.monitoring;
    }

	if (args.params.hasOwnProperty('logging') && args.params.logging.hasOwnProperty('logpath')) {
		try {
			let stats = fs.statSync(args.params.logging.logpath);

			if (stats && stats.isDirectory()) {
				args.params.logging.logpath = path.join(args.params.logging.logpath, `${args.params.name}.log`);
			}
		} catch(e) {
			let dir = path.parse(args.params.logging.logpath).dir;
			if (dir.length) {
				try {
					fs.statSync(dir);
				} catch (e) {
					cb({'code': 400, 'message': `start_service: logpath parent directory ${args.params.logging.logpath} is unaccessible ${e}`});
					return;
				}
			}
		}
	}

	// now we actually start the child process
	let name = args.params.name;
	let params = args.params;
	opt.push(JSON.stringify(params));
	this.services[name] = args

	this.logger.debug({opts: opt}, 'spawning process');

	this.processes[name] = spawn('python3', opt, {stdio: 'inherit'})
		.on('exit', (code, signal) => {
			// service exit callback
			this.logger.info({service: name, exit_code: code}, "service exited");

			// if a service receives the signal to shudtdown - set all pipelines to inactive if it conains the service
			// that shuts down
			if (signal === 'SIGTERM') {
				this.logger.info({service: name, exit_code: code}, "service terminated by user");
				for (let pl in this.pipelines) {
					for (let i=0; i < this.pipelines[pl]['services'].length; i++) {
						if (this.pipelines[pl]['services'][i] === name) {
							this.pipelines[pl]['active'] = false;
							break;
						}
					}
				}
			}

			delete this.processes[name];
			delete this.services[name];
		})
		.on('error', (e) => {
			delete this.services[name];
			this.logger.error({error: e, args: args}, "unable to spawn service");
		});

    //activate all pipelines that include this service and have no inactive services
	Object.entries(this.pipelines)
		.filter(([pname, x]) => x.active === false)
		.filter(([pname, x]) => x.services.indexOf(name) != -1)
		.forEach(([pname, x]) => {
			let should_be_active = x.services.map(x => x in this.services).reduce( (x, y) => x && y, true );
			if (should_be_active)
				this.pipelines[pname].active = true;
		});

	cb(null, {'message': `service [${name}] created`});
}

/**
 * construct a roxcomposer message object given a pipeline and payload (data)
 **/
function create_roxcomposer_message(pline, data) {
	let msg = new roxcomposer_message.Message();

	for (let s in pline)
		msg.add_service(pline[s]);

	msg.set_payload(data);

	return msg;
}

/**
 * read a roxcomposer message from its binary representation
 **/
function read_roxcomposer_message(msg) {
	let m = roxcomposer_message.deserialize(msg);
	return m.get_payload();
}

/**
 * send a message into a pipeline
 * args = { 'name': pipeline_name, 'data': "..." }
 **/
function post_to_pipeline(args, cb) {
	if (!(args.name in this.pipelines)) {
		cb({'code': 400, 'message': 'no pipeline with that name'});
		return;
	}

	let pline = this.pipelines[args.name];

	if (pline.active === false) {
		cb({'code': 400, 'message': `pipeline ${args.name} is inactive`});
		return;
	}

	let servs;
	try {
		servs = pline.services.map( (x) => {
			let s = this.services[x];
			return new roxcomposer_message.Service(s.params.ip, s.params.port);
		});
	} catch (e) {
		this.logger.error({error: e}, 'invalid service in pipeline');
		cb({'code': 500, 'message': `pipeline is broken: ${e}`});
	}
	let msg = create_roxcomposer_message(servs, args.data);

	let socket = new net.Socket();
	let start = this.services[pline.services[0]];
	this.logger.debug({name: pline.services[0], ip: start.params.ip, port: start.params.port}, 'attempting connection to service');
	socket.connect({port: start.params.port, host: start.params.ip}, () => {
		this.logger.info({message_id: msg.id, pipeline: args.name}, 'message posted to pipeline');
		let packet = msg.serialize();
		socket.end(packet);
		cb(null, {'message': 'pipeline initiated', 'message_id': msg.id});
	});
	socket.on('error', (e) => {
		this.logger.error({error: e, service: { name: pline.services[0], ip: start.params.ip, port: start.params.port }}, 'unable to connect to service');
		cb({'code': 500, 'message': 'internal server error'});
	});
}

/**
 * get the list of active services
 * no args required
 **/
function get_services(args, cb) {
	cb(null, this.services);
}

/**
 * get the list of defined pipelines
 * no args required
 **/
function get_pipelines(args, cb) {
	cb(null, this.pipelines);
}

/**
 * define a pipeline of services
 * args = { 'name': "...", 'pipeline': [ ... service names ... ] }
 **/
function set_pipeline(args, cb) {
	if (!('services' in args)) {
		let msg = 'set_pipeline: service array missing from arguments';
		this.logger.error({args: args}, msg);
		cb({'code': 400, 'message': msg});
		return;
	}
	if (!('name' in args)) {
		let msg = 'set_pipeline: pipeline name not provided';
		this.logger.error({args: args}, msg);
		cb({'code': 400, 'message': msg});
		return;
	}
	if (!Array.isArray(args.services)) {
		let msg = 'set_pipeline: args.services must be an array';
		this.logger.error({args: args}, msg);
		cb({'code': 400, 'message': msg});
		return;
	}
	if (args.services.length === 0) {
		let msg = 'set_pipeline: args.services must not be empty';
		this.logger.error({args: args}, msg);
		cb({'code': 400, 'message': msg});
		return;
	}
	for (let s in args.services) {
		if (!(args.services[s] in this.services)) {
			let msg = `set_pipeline: no service with name [${args.services[s]}]`;
			this.logger.error(msg);
			cb({'code': 400, 'message': msg});
			return;
		}
	}

	let pipeline_services = args.services;
	this.pipelines[args.name] = {
		'services': pipeline_services,
		'active': true
	};
	cb(null, {'message': `pipeline [${args.name}] created`});
}

/**
 * shutdown a service
 * args = { 'name': "..." }
 **/
function shutdown_service(args, cb) {
	if (args === undefined)
		throw TypeError("shutdown: 'args' must be a dictionary");
	if (typeof cb !== 'function')
		throw TypeError("shutdown: 'cb' must be a function");

	if (args.name in this.services) {
		let proc = this.processes[args.name];
		proc.kill('SIGTERM');
		cb(null, {'message': 'service stopped - all pipelines, them with this service work, are now inactive'});
	} else {
		cb({'code': 400, 'message': `shutdown: service unknown ${args.name}`});
	}
}

/**
 * contact the reporting service
 * funcname: command to be performed by the reporting service
 * args: arguments depending on funcname
 **/
function post_to_report_service(funcname, args, cb) {
	// we open a socket to receive the answer from the reporting service
	let server = new net.createServer((c) => {
		// will only be closed when the last active connection has been closed
		// but this way we don't have to do it later
		server.close();
		let chunks = [];
		c.on('data', (chunk) => {
			chunks.push(chunk); 
		});
		c.on('end', () => {
			let doc = Buffer.concat(chunks);

			let msg;
			try {
				msg = read_roxcomposer_message(doc);
				let d = JSON.parse(msg);
				cb(null, d);
			} catch(e) {
				let errmsg = `unable to parse report service answer: ${e} - ${msg}`;
				this.logger.error({msg: doc}, errmsg );
			}
		});
	});
	server.listen(0, '0.0.0.0', () => {
		let socket = net.createConnection( this.services[this.reporting_service].params.port, this.services[this.reporting_service].params.ip, () => {
			let addr = socket.address();
			let pline = [ new roxcomposer_message.Service(this.services[this.reporting_service].params.ip, this.services[this.reporting_service].params.port), new roxcomposer_message.Service(server.address().address, server.address().port) ];
			let msg = create_roxcomposer_message(pline, JSON.stringify({'function': funcname, 'args': args}));
			let packet = msg.serialize();
			socket.end(packet);
		}).on('error', (e) => {
			server.close();
			let errmsg = "unable to connect to reporting service";
			this.logger.error({error: e}, errmsg);
			throw(errmsg);
		});
	});
	server.on('error', (e) => {
		let errmsg = 'socket listening for report service answer encountered an error';
		this.logger.error({error: e}, errmsg );
		server.close();
		throw(errmsg);
	});
}

/**
 * retrieve the message trace for a specific message
 * args = { TODO: do some argument checking }
 **/
function get_msg_history(args, cb) {
	if (this.reporting_service)
		try {
			this.post_to_report_service("get_msg_history", args, cb);
		} catch (e) {
			cb({code: 500, message: e});
		}

	else
		cb({'code': 400, 'message': 'no reporting service has been configured'});
}

/**
 * retrieve the message status for a specific message
 * args = { TODO: do some argument checking }
 **/
function get_msg_status(args, cb) {
	if (this.reporting_service)
		try {
			this.post_to_report_service("get_msg_status", args, cb);
		} catch (e) {
			cb({code: 500, message: e});
		}
	else
		cb({'code': 400, 'message': 'no reporting service has been configured'});
}

/**
 * dump the currently active services and pipeline definitions
 * args = {}
 **/
function dump_services_and_pipelines(args, cb) {
	cb(null, { services: this.services, pipelines: this.pipelines });
}

/**
 * restore a dump created by dump_services_and_pipelines
 * args = dump
 **/
function load_services_and_pipelines(args, cb) {
	let skipped_services = [];
	let started_services = [];
	let set_pipelines = [];
	let skipped_pipelines = [];
	let errors = [];
	let promises = [];

	if ('services' in args) {
		for (let s in args.services) {
			if (s in this.services)
				skipped_services.push(s);
			else {
				promises.push(new Promise((resolve) => {
					this.start_service(args.services[s], (err, msg) => {
						if (err) {
							errors.push(err);
						} else {
							started_services.push(s);
						}
						resolve();
					});
				}));
			}
		}
	}

	Promise.all(promises).then(() => {
		promises = [];
		if ('pipelines' in args) {
			for (let p in args.pipelines) {
				if(!('active' in args.pipelines[p]) || args.pipelines[p].active) {
					promises.push(new Promise((resolve) => {
						this.set_pipeline({name: p , services: args.pipelines[p].services }, (err, msg) => {
							if (err) {
								errors.push(err);
							} else {
								set_pipelines.push(p);
							}
							resolve();
						});
					}));
				} else {
					skipped_pipelines.push(p);
				}
			}
		}
	});

	Promise.all(promises).then(() => {
		cb(null, {
			services_started: started_services,
			services_skipped: skipped_services,
			set_pipelines: set_pipelines,
			skipped_pipelines: skipped_pipelines,
			errors: errors
		});
	});
}

// args = { 'pipe_path': "<absolute_path>"}
function load_and_start_pipeline(args, cb) {
	if (!('pipe_path' in args)) {
		let msg = 'load_and_start_pipeline: path_pipeline_config_file missing from arguments';
		this.logger.error({args: args}, msg);
		cb({'code': 400, 'message': msg});
		return;
	}

    let pipe_path = args.pipe_path;
    let my_pipeline = load_pipeline_json_file(pipe_path, cb);
    this.start_pipeline(my_pipeline, cb);
}

//String pipe_path = <absolute_path_to_pipeline_config_file>
function load_pipeline_json_file(pipe_path, cb) {
    const fs = require('fs');
    try {
        let pipeline_json = fs.readFileSync(pipe_path);
        let pipeline = JSON.parse(pipeline_json);
        return pipeline;
    }catch (e) {
		cb({code: 400, message: e });
    }
}

// args = { 'name': <pipeline_name>, 'services': [ ... service names ... ] }
function start_pipeline(args, cb) {
    return(this.set_pipeline(args, cb));
}

/**
 * start a new session for log observation
 **/
function create_log_observer(args, cb) {
	let missing = check_args(args, ['lines', 'timeout']);
	if (missing) {
		cb({code: 400, message: missing});
		return;
	}

	let l = new LogSession(args.lines);
	this.logsessions[l.id] = { session: l, services: new Set(), timeout: args.timeout * 1000 };

	if ('services' in args) {
		this.add_services_to_logsession(l.id, args.services).
			then(
				ml => {
					ml.sessionid = l.id;
					cb(null, ml);
				},
				error => {
					cb({code: 400, message: error});
				}
			).
			catch(error => {
				cb({code: 400, message: error});
			});
	} else {
		cb(null, {sessionid: l.id});
	}

	this.set_logsession_timeout(l.id);
}

/*
 * check a list of services whether they exist and have a log file configured
 **/
function check_services_and_logs(services) {
	let set = new Set(services);
	let missing_services = services.filter(s => !(s in this.services));
	missing_services.forEach(s => set.delete(s));

	let without_log = Array.from(set).filter(s => !(('logging' in this.services[s].params) && ('logpath' in this.services[s].params.logging)));
	without_log.forEach(s => set.delete(s));

	return { 'ok': Array.from(set), 'missing': missing_services, 'without_log': without_log };
}

/*
 * endpoint handler for adding services to a log session
 **/
function post_services_to_logsession(args, cb) {
	let missing = check_args(args, ['sessionid', 'services']);
	if (missing) {
		cb({code: 400, message: missing});
		return;
	}

	if (!Array.isArray(args.services) || args.services.length == 0) {
		cb({code: 400, message: "services parameter needs to be a non-empty array"})
		return;
	}

	let sid = args.sessionid;
	this.add_services_to_logsession(sid, args.services).
		then(
			ml => { ml.sessionid = sid; cb(null, ml) },
			error => cb({code: 400, message: error})
		).
		catch(error => cb({code: 400, message: error}));
}

/*
 * add services to an existing log session
 **/
function add_services_to_logsession(sessionid, services) {
	let l = this.logsessions[sessionid];
	if (!l)
		return Promise.reject(`session ${sessionid} invalid/timed out`);

	ml = this.check_services_and_logs(services);

	if (ml.ok.length == 0) {
		ret = "no valid services provided: ";
		if (ml.missing.length)
			ret += `missing services: [${ml.missing.join(", ")}] `;
		if (ml.without_log.length)
			ret += `services without logfile: [${ml.without_log.join(", ")}]`;
		return Promise.reject(ret);
	}

	ml.ok.forEach(s => l.services.add(s));
	this.logger.info(ml, 'adding services to watcher');

	l.session.filters[0] = service_log_filter(Array.from(l.services.values()));
	return new Promise((resolve, reject) => {
		l.session.watch_files(ml.ok.map(s => this.services[s].params.logging.logpath)).then(() => resolve(ml), reject);
	});
}

/*
 * create a reqexp for service log line filtering
 * assumes that a service will put 'service:servicenam' into its log lines
 **/
function service_log_filter(services) {
	// WARNING: this depends on the service log format - changing the layout may break this
	// when every service get its own log file we won't need this crutch anymore
        let service_set = new Set(services);
	return line => { let o = JSON.parse(line); return ('service' in o) && service_set.has(o.service); }
}

/**
 * set or refresh a timeout for session cleanup
 **/
function set_logsession_timeout(sessionid) {
	let l = this.logsessions[sessionid];
	if ('timerid' in l)
		clearTimeout(l.timerid);

	l.timerid = setTimeout(() => {
		l.session.cleanup();
		delete this.logsessions[l];
	}, l.timeout);
}

/**
 * remove services from observation or delete the whole session
 * this was put into the same function in order to provide a single endpoint
 * DELETE log_observer
 * for both operations
 * args = { sessionid: "...", services: [....] }
 * the services parameter is optional, if present the services are removed from observation
 * otherwise the whole session is deleted
 **/
function delete_log_observer(args, cb) {
	let missing = check_args(args, ['sessionid']);
	if (missing) {
		cb({code: 400, message: missing});
		return;
	}

	if (! (args.sessionid in this.logsessions)) {
		cb({code: 400, message: `invalid/timed out sessionid ${args.sessionid}`});
		return;
	}

	let l = this.logsessions[args.sessionid];

	if ('services' in args) {
		try {
			this.check_services_and_logs(args.services);
		} catch(e) {
			cb({ code: 400, message: e});
			return;
		};
		for (s in args.services)
			l.services.delete(args.services[s]);
		l.session.filters[0] = service_log_filter(Array.from(l.services.values()));
		let keep = new Set(Array.from(l.services.values()).map(s => this.services[s].params.logging.logpath));
		let remove = args.services.map(s => this.services[s].params.logging.logpath);
		remove = remove.filter(f => !keep.has(f));
		if (remove.length)
			l.session.unwatch_files(remove);
	} else {
		if ('timerid' in l)
			clearTimeout(l.timerid);
		l.session.cleanup();
		delete this.logsessions[args.sessionid];
	}

	cb(null, {ok: args.sessionid});
}

/*
 * receive the gathered lines from a logsession
 * args = { sessionid: "..." }
 **/
function get_log_lines(args, cb) {
	let missing = check_args(args, ['sessionid']);
	if (missing) {
		cb({code: 400, message: missing});
		return;
	}

	if (!(args.sessionid in this.logsessions)) {
		cb({code: 400, message: 'sessionid invalid or session expired'});
		return;
	}

	let lines = this.logsessions[args.sessionid].session.get_lines();
	cb(null, { loglines: lines });
}

