//
// Classe mosaic deploy: standard functionalities from mosaic
//
// devs@droxit.de - droxIT GmbH
//
// Copyright (c) 2018 droxIT GmbH
//

let fs = require('fs');
let bunyan = require('bunyan');
let spawn = require('child_process').spawn;
let net = require('net');
let mosaic_message = require('./mosaic_message.js');

function __mosaic_control_private() {
	this.processes = {};
	this.services = {};
	this.pipelines = {};
	this.logger;
	this.service_container_path;
	this.reporting_service;
}

module.exports = function (container) {
	let mcp = new __mosaic_control_private();
	container['init'] = init.bind(undefined, mcp);
	container['start_service'] = start_service.bind(undefined, mcp);
	container['shutdown_service'] = shutdown_service.bind(undefined, mcp);
	container['get_services'] = get_services.bind(undefined, mcp);
	container['get_pipelines'] = get_pipelines.bind(undefined, mcp);
	container['set_pipeline'] = set_pipeline.bind(undefined, mcp);
	container['post_to_pipeline'] = post_to_pipeline.bind(undefined, mcp);
	container['get_msg_history'] = get_msg_history.bind(undefined, mcp);
	container['get_msg_status'] = get_msg_status.bind(undefined, mcp);
	container['load_and_start_pipeline'] = load_and_start_pipeline.bind(undefined, mcp);
};

/**
 * intialize this plugin
 * args needs to contain IP, port and the beginning of the portrange for the micro services
 **/
function init(mcp, args) {
	if (args && ('logger' in args))
		mcp.logger = args.logger;
	else
		mcp.logger = bunyan.createLogger({name: 'mosaic_control'});

	if (args && ('service_container' in args))
		mcp.service_container_path = args.service_container;

	if (mcp.service_container_path) {
		try {
			fs.accessSync(mcp.service_container_path);
		} catch (e) {
			let msg = `unable to access service container module at ${mcp.service_container_path} - ${e.message}`;
			throw new Error(msg);
		}
	}

	if (args && ('reporting_service' in args)) {
		start_service(mcp, args.reporting_service, (err) => {
			if (err) {
				let msg = err.message;
				throw new Error(msg);
			}
			mcp.reporting_service = args.reporting_service.params.name;
		});
	}
}

/**
 * spawn a new service
 * args need to contain the name of the service and the path to the service module
 **/
function start_service(mcp, args, cb) {
	mcp.logger.debug({args: args}, 'start_service called');
	let opt;

	if (args === undefined)
		throw TypeError("start_service: 'args' must be a dictionary");
	if (typeof cb !== 'function')
		throw TypeError("start_service: 'cb' must be a function");

	if ('path' in args) {
		try {
			fs.accessSync(args.path);
			opt = [args.path];
		} catch (e) {
			cb({'code': 400, 'message': `start_service: path does not exist - ${args.path}`});
			return;
		}
	} else if ('classpath' in args) {
        if (mcp.service_container_path) {
		    opt = [mcp.service_container_path, args.classpath];
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

	if (!('name' in args.params)) {
		cb({'code': 400, 'message': 'start_service: a service name must be given'});
		return;
	}

	if (args.params.name in mcp.services) {
		cb({'code': 400, 'message': 'start_service: a service with that name already exists'});
		return;
	}

	for(let my_service in mcp.services) {
    	if ((mcp.services[my_service].params.port == args.params.port) && (mcp.services[my_service].params.ip == args.params.ip)) {
		    cb({'code': 400, 'message': `start_service: service ${my_service} is already registered under this address  (${args.params.ip},${args.params.port}`});
		    return;
        }
	}

	let name = args.params.name;
	let params = args.params;
	opt.push(JSON.stringify(params));
	mcp.services[name] = {};
	mcp.services[name].path = args.path;
	mcp.services[name].params = args.params;

	mcp.logger.debug({opts: opt}, 'spawning process');

	mcp.processes[name] = spawn('python3', opt, {stdio: 'inherit'})
		.on('exit', (code, signal) => {
			// service exit callback
			mcp.logger.info({service: name, exit_code: code}, "service exited");

			// if a service receives the signal to shudtdown - set all pipelines to inactive if it conains the service
			// that shuts down
			if (signal === 'SIGTERM') {
				mcp.logger.info({service: name, exit_code: code}, "service terminated by user");
				for (let pl in mcp.pipelines) {
					for (let i=0; i < mcp.pipelines[pl]['services'].length; i++) {
						if (mcp.pipelines[pl]['services'][i] === name) {
							mcp.pipelines[pl]['active'] = false;
							break;
						}
					}
				}
			}

			delete mcp.processes[name];
			delete mcp.services[name];
		})
		.on('error', (e) => {
			delete mcp.services[name];
			mcp.logger.error({error: e, args: args}, "unable to spawn service");
		});

    //activate all pipeline that include this service
    for (let pl in mcp.pipelines) {
	    for (let i=0; i < mcp.pipelines[pl]['services'].length; i++) {
	        if ((mcp.pipelines[pl]['services'][i] === name) && !mcp.pipelines[pl]['active']){
	            mcp.pipelines[pl]['active'] = true;
				break;
			}
		}
	}

	cb(null, {'message': `service [${name}] created`});
}

function create_mosaic_message(pline, data) {
	let msg = new mosaic_message.Message();

	for (let s in pline)
		msg.add_service(pline[s]);

	msg.set_payload(data);

	return msg;
}

function read_mosaic_message(msg) {
	let m = mosaic_message.deserialize(msg);
	return m.get_payload();
}

// args = { 'name': pipeline_name, 'data': "..." }
function post_to_pipeline(mcp, args, cb) {
	if (!(args.name in mcp.pipelines)) {
		cb({'code': 400, 'message': 'no pipeline with that name'});
		return;
	}

	let pline = mcp.pipelines[args.name];

	if (pline.active === false) {
		cb({'code': 400, 'message': `pipeline ${args.name} is inactive`});
		return;
	}

	let servs;
	try {
		servs = pline.services.slice(1).map( (x) => {
			let s = mcp.services[x];
			return new mosaic_message.Service(s.params.ip, s.params.port);
		});
	} catch (e) {
		mcp.logger.error({error: e}, 'invalid service in pipeline');
		cb({'code': 500, 'message': `pipeline is broken: ${e}`});
	}
	let msg = create_mosaic_message(servs, args.data);

	let socket = new net.Socket();
	let start = mcp.services[pline.services[0]];
	mcp.logger.debug({name: pline.services[0], ip: start.params.ip, port: start.params.port}, 'attempting connection to service');
	socket.connect({port: start.params.port, host: start.params.ip}, () => {
		let packet = msg.serialize();
		socket.end(packet);
		cb(null, {'message': 'pipeline initiated', 'message_id': msg.id});
	});
	socket.on('error', (e) => {
		mcp.logger.error({error: e, service: { name: pline.services[0], ip: start.params.ip, port: start.params.port }}, 'unable to connect to service');
		cb({'code': 500, 'message': 'internal server error'});
	});
}

// no args required
function get_services(mcp, args, cb) {
	cb(null, mcp.services);
}

// no args required
function get_pipelines(mcp, args, cb) {
	cb(null, mcp.pipelines);
}

// args = { 'name': "...", 'pipeline': [ ... service names ... ] }
function set_pipeline(mcp, args, cb) {
    mcp.logger.debug("###############set_pipeline=", args)
	if (!('services' in args)) {
		let msg = 'set_pipeline: service array missing from arguments';
		mcp.logger.error({args: args}, msg);
		cb({'code': 400, 'message': msg});
		return;
	}
	if (!Array.isArray(args.services)) {
		let msg = 'set_pipeline: args.services must be an array';
		mcp.logger.error({args: args}, msg);
		cb({'code': 400, 'message': msg});
		return;
	}
	if (args.services.length === 0) {
		let msg = 'set_pipeline: args.services must not be empty';
		mcp.logger.error({args: args}, msg);
		cb({'code': 400, 'message': msg});
		return;
	}
	for (let s in args.services) {
		if (!(args.services[s] in mcp.services)) {
			let msg = `set_pipeline: no service with name [${args.services[s]}]`;
			mcp.logger.error(msg);
			cb({'code': 400, 'message': msg});
			return;
		}
	}

	let pipeline_services = args.services;
	mcp.pipelines[args.name] = {
		'services': pipeline_services,
		'active': true
	};
	cb(null, {'message': `pipeline [${args.name}] created`});
}

// args = { 'name': "..." }
function shutdown_service(mcp, args, cb) {
	if (args === undefined)
		throw TypeError("shutdown: 'args' must be a dictionary");
	if (typeof cb !== 'function')
		throw TypeError("shutdown: 'cb' must be a function");

	if (args.name in mcp.services) {
		let proc = mcp.processes[args.name];
		proc.kill('SIGTERM');
		cb(null, {'message': 'service stopped - all pipelines, them with this service work, are now inactive'});
	} else {
		cb({'code': 400, 'message': `shutdown: service unknown ${args.name}`});
	}
}

function post_to_report_service(mcp, funcname, args, cb) {
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
				msg = read_mosaic_message(doc);
				let d = JSON.parse(msg);
				cb(null, d);
			} catch(e) {
				let errmsg = `unable to parse report service answer: ${e} - ${msg}`;
				mcp.logger.error({msg: doc}, errmsg );
			}
		});
	});
	server.listen(0, '0.0.0.0', () => {
		let socket = net.createConnection( mcp.services[mcp.reporting_service].params.port, mcp.services[mcp.reporting_service].params.ip, () => {
			let addr = socket.address();
			let pline = [ new mosaic_message.Service(server.address().address, server.address().port) ];
			let msg = create_mosaic_message(pline, JSON.stringify({'function': funcname, 'args': args}));
			let packet = msg.serialize();
			socket.end(packet);
		}).on('error', (e) => {
			server.close();
			let errmsg = "unable to connect to reporting service";
			mcp.logger.error({error: e}, errmsg);
			throw(errmsg);
		});
	});
	server.on('error', (e) => {
		let errmsg = 'socket listening for report service answer encountered an error';
		mcp.logger.error({error: e}, errmsg );
		server.close();
		throw(errmsg);
	});
}

function get_msg_history(mcp, args, cb) {
	if (mcp.reporting_service)
		try {
			post_to_report_service(mcp, "get_msg_history", args, cb);
		} catch (e) {
			cb({code: 500, message: e});
		}

	else
		cb({'code': 400, 'message': 'no reporting service has been configured'});
}

function get_msg_status(mcp, args, cb) {
	if (mcp.reporting_service)
		try {
			post_to_report_service(mcp, "get_msg_status", args, cb);
		} catch (e) {
			cb({code: 500, message: e});
		}
	else
		cb({'code': 400, 'message': 'no reporting service has been configured'});
}

// args = { 'pipe_path': "<absolute_path>"}
function load_and_start_pipeline(mcp, args, cb) {
	if (!('pipe_path' in args)) {
		let msg = 'load_and_start_pipeline: path_pipeline_config_file missing from arguments';
		mcp.logger.error({args: args}, msg);
		cb({'code': 400, 'message': msg});
		return;
	}

    let pipe_path = args.pipe_path;
    let my_pipeline = load_pipeline_json_file(mcp, pipe_path, cb);
    start_pipeline(mcp, my_pipeline, cb);
}

//String pipe_path = <absolute_path_to_pipeline_config_file>
function load_pipeline_json_file(mcp, pipe_path, cb) {
    const fs = require('fs');
    let pipeline_json = fs.readFileSync(pipe_path);
    let pipeline = JSON.parse(pipeline_json);
    return pipeline;
}

// args = { 'name': <pipeline_name>, 'services': [ ... service names ... ] }
function start_pipeline(mcp, args, cb) {
    return(set_pipeline(mcp, args, cb));
}