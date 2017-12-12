let fs = require('fs');
let bunyan = require('bunyan');
let spawn = require('child_process').spawn;
let net = require('net');
let uuid = require('uuid/v4');
let mosaic_message = require('./service_com_pb.js');

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
};

function service_name2id(name) {
	if (name in services) {
		return `${services[name].params.ip}:${services[name].params.port}`;
	}

	return null;
}

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
			fs.accessSync(service_container_path);
		} catch (e) {
			let msg = `unable to access service container module at ${service_container_path} - ${e.message}`;
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

	if ('name' in mcp.services) {
		cb({'code': 400, 'message': 'start_service: a service with that name already exists'});
		return;
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
			console.log(`service ${name} exited`);

			delete mcp.processes[name];
			delete mcp.services[name];
		})
		.on('error', (e) => {
			delete mcp.services[name];
			mcp.logger.error({error: e, args: args}, "unable to spawn service");
		});

	cb(null, {'message': `service [${name}] created`});
}

function create_mosaic_message(mcp, pline, data) {
	let msg = new mosaic_message.MosaicMessage();
	let arr = [];
	for (let s in pline) {
		let sname = pline[s];
		let service = new mosaic_message.Service();
		service.setId(mcp.services[sname]['params'].ip + ":" + mcp.services[sname]['params'].port);
		arr.push(service);
	}
	let pipeline = new mosaic_message.Pipeline();
	pipeline.setServicesList(arr);
	msg.setPipeline(pipeline);
	let payload = new mosaic_message.Payload();
	payload.setBody(data);
	msg.setPayload(payload);
	msg.setId(uuid());

	return msg;
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

	let msg = create_mosaic_message(mcp, pline.services, args.data);

	let socket = new net.Socket();
	let start = mcp.services[pline.services[0]];
	socket.connect({port: start.params.port, host: start.params.ip}, () => {
		let packet = msg.serializeBinary();
		socket.end(String.fromCharCode.apply(null, packet));
		cb(null, {'message': 'pipeline initiated', 'message_id': msg.getId()});
	});
	socket.on('error', (e) => {
		mcp.logger.error({error: e}, "unable to connect to service");
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
		cb(null, {'message': 'service stopped'});
	} else {
		cb({'code': 400, 'message': "shutdown: service unknown"});
	}
}

function post_to_report_service(mcp, funcname, args, cb) {
	let server = new net.createServer((c) => {
		// will only be closed when the last active connection has been closed
		// but this way we don't have to do it later
		server.close();
		let doc = ""
		c.on('data', (chunk) => {
			doc += chunk;
		});
		c.on('end', () => {
			try {
				let d = JSON.parse(doc);
				cb(null, d);
			} catch(e) {
				logger.error({msg: doc}, 'unable to parse report service answer');
				cb({'code': 500, 'message': 'internal server error'});
			}
		});
	});
	server.listen(() => {
		let socket = net.createConnection( mcp.services[reporting_service].params.port, mcp.services[reporting_service].params.ip, () => {
			let addr = socket.address();
			let pline = [ service_name2id(reporting_service), `${server.address().address}:${server.address().port}` ]
			let msg = create_mosaic_message(pline, JSON.stringify(args));
			let packet = msg.serializeBinary();
			socket.end(String.fromCharCode.apply(null, packet));
			cb(null, {'message': 'pipeline initiated'});
		}).on('error', (e) => {
			server.close();
			mcp.logger.error({error: e}, "unable to connect to reporting service");
			cb({'code': 500, 'message': 'internal server error'});
		});
	});
	server.on('error', (e) => {
		mcp.logger.error({error: e}, 'socket listening for report service answer encountered an error');
		server.close();
		cb({'code': 500, 'message': 'internal server error'});
	});
}

function get_msg_history(mcp, args, cb) {
	if (mcp.reporting_service)
		post_to_report_service(mcp, "get_msg_history", args, cb);
	else
		cb({'code': 400, 'message': 'no reporting service has been configured'});
}

function get_msg_status(mcp, args, cb) {
	if (mcp.reporting_service)
		post_to_report_service(mcp, "get_msg_status", args, cb);
	else
		cb({'code': 400, 'message': 'no reporting service has been configured'});
}
