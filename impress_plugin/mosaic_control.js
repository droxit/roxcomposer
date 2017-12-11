let fs = require('fs');
let bunyan = require('bunyan');
let spawn = require('child_process').spawn;
let net = require('net');
let mosaic_message = require('./service_com_pb.js');
let processes = {};
let services = {};
let pipelines = {};
let logger;
let service_container_path;

module.exports = function (container) {
	container['init'] = init;
	container['start_service'] = start_service;
	container['shutdown_service'] = shutdown_service;
	container['get_services'] = get_services;
	container['get_pipelines'] = get_pipelines;
	container['set_pipeline'] = set_pipeline;
	container['post_to_pipeline'] = post_to_pipeline;
};

/**
 * intialize this plugin
 * args needs to contain IP, port and the beginning of the portrange for the micro services
 **/
function init(args) {
	if (args && ('logger' in args))
		logger = args.logger;
	else
		logger = bunyan.createLogger({name: 'mosaic_control'});

	if (args && ('service_container' in args))
		service_container_path = args.service_container;

	if (service_container_path) {
		try {
			fs.accessSync(service_container_path);
		} catch (e) {
			let msg = `unable to access service container module at ${service_container_path} - ${e.message}`;
			throw new Error(msg);
		}
	}

}

/**
 * spawn a new service
 * args need to contain the name of the service and the path to the service module
 **/
function start_service(args, cb) {
	logger.debug({args: args}, 'start_service called');
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
			cb({'code': 400, 'message': 'start_service: path does not exist'});
			return;
		}
	} else if ('classpath' in args) {
        if (service_container_path) {
		    opt = [service_container_path, args.classpath];
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

	if ('name' in services) {
		cb({'code': 400, 'message': 'start_service: a service with that name already exists'});
		return;
	}

	let name = args.params.name;
	let params = args.params;
	opt.push(JSON.stringify(params));
	services[name] = {};
	services[name].path = args.path;
	services[name].params = args.params;

	logger.debug({opts: opt}, 'spawning process');

	processes[name] = spawn('python3', opt, {stdio: 'inherit'})
		.on('exit', (code, signal) => {
			// service exit callback
			logger.info({service: name, exit_code: code}, "service exited");

			// if a service receives the signal to shudtdown - set all pipelines to inactive if it conains the service
			// that shuts down
			if (signal === 'SIGTERM') {
				logger.info({service: name, exit_code: code}, "service terminated by user");
				for (let pl in pipelines) {
					for (let i=0; i < pipelines[pl]['services'].length; i++) {
						if (pipelines[pl]['services'][i] === name) {
							pipelines[pl]['active'] = false;
							break;
						}
					}
				}
			}

			delete processes[name];
			delete services[name];
		})
		.on('error', (e) => {
            delete services[name];
			logger.error({error: e, args: args}, "unable to spawn service");
		});

	cb(null, {'message': `service [${name}] created`});
}

// args = { 'name': pipeline_name, 'data': "..." }
function post_to_pipeline(args, cb) {
	if (!(args.name in pipelines)) {
		cb({'code': 400, 'message': 'no pipeline with that name'});
		return;
	}

	let pline = pipelines[args.name];

    if (pline.active === false) {
		cb({'code': 400, 'message': `pipeline ${args.name} is inactive`});
		return;
    }

	let msg = new mosaic_message.MosaicMessage();
	let arr = [];
	for (let s in pline.services) {
		let sname = pline.services[s];
		let service = new mosaic_message.Service();
		service.setId(services[sname]['params'].ip + ":" + services[sname]['params'].port);
		arr.push(service);
	}
	let pipeline = new mosaic_message.Pipeline();
	pipeline.setServicesList(arr);
	msg.setPipeline(pipeline);
	let payload = new mosaic_message.Payload();
	payload.setBody(args.data);
	msg.setPayload(payload);

	let socket = new net.Socket();
	let start = services[pline.services[0]];
	socket.connect({port: start.params.port, host: start.params.ip}, () => {
		let packet = msg.serializeBinary();
		socket.end(String.fromCharCode.apply(null, packet));
		cb(null, {'message': 'pipeline initiated'});
	});
	socket.on('error', (e) => {
		logger.error({error: e}, "unable to connect to service");
		cb({'code': 500, 'message': 'internal server error'});
	});
}

// no args required
function get_services(args, cb) {
	cb(null, services);
}

// no args required
function get_pipelines(args, cb) {
	cb(null, pipelines);
}

// args = { 'name': "...", 'pipeline': [ ... service names ... ] }
function set_pipeline(args, cb) {
	if (!('services' in args)) {
		let msg = 'set_pipeline: service array missing from arguments';
		logger.error({args: args}, msg);
		cb({'code': 400, 'message': msg});
		return;
	}
	if (!Array.isArray(args.services)) {
		let msg = 'set_pipeline: args.services must be an array';
		logger.error({args: args}, msg);
		cb({'code': 400, 'message': msg});
		return;
	}
	if (args.services.length === 0) {
		let msg = 'set_pipeline: args.services must not be empty';
		logger.error({args: args}, msg);
		cb({'code': 400, 'message': msg});
		return;
	}
	for (let s in args.services) {
		if (!(args.services[s] in services)) {
			let msg = `set_pipeline: no service with name [${args.services[s]}]`;
			logger.error(msg);
			cb({'code': 400, 'message': msg});
			return;
		}
	}

	let pipeline_services = args.services;
	pipelines[args.name] = {
		'services': pipeline_services,
		'active': true
	};
	cb(null, {'message': `pipeline [${args.name}] created`});
}

// args = { 'name': "..." }
function shutdown_service(args, cb) {
	if (args === undefined)
		throw TypeError("shutdown: 'args' must be a dictionary");
	if (typeof cb !== 'function')
		throw TypeError("shutdown: 'cb' must be a function");

	if (args.name in services) {
		let proc = processes[args.name];
		delete services[args.name];
		proc.kill('SIGTERM');
		cb(null, {'message': 'service stopped'});
	} else {
		cb({'code': 400, 'message': "shutdown: service unknown"});
	}
}
