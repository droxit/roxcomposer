var fs = require('fs');
var bunyan = require('bunyan');
var spawn = require('child_process').spawn;
var net = require('net');
var mosaic_message = require('./service_com_pb.js');
var processes = {};
var services = {};
var pipelines = {};
var address;
var port;
var portrange;
var logger;

module.exports = function(container) {
    container['init'] = init;
    container['start_service'] = start_service;
    container['shutdown'] = shutdown;
    container['get_services'] = get_services;
    container['get_pipelines'] = get_pipelines;
    container['set_pipeline'] = set_pipeline;
    container['post_to_pipeline'] = post_to_pipeline;
}

/**
 * intialize this plugin
 * args needs to contain IP, port and the beginning of the portrange for the micro services
 **/
function init(args) {
    if(args && 'logger' in args)
        logger = args.logger;
    else
        logger = bunyan.createLogger({name: 'mosaic_control'});
}

/**
 * spawn a new service
 * args need to contain the name of the service and the path to the service module
 **/
function start_service(args, cb) {
    logger.debug({args: args}, 'start_service called');
    var opt;

    if (args === undefined)
        throw TypeError("start_service: 'args' must to be a dictionary");
    if (typeof cb !== 'function')
        throw TypeError("start_service: 'cb' must be a function");

    if ('path' in args) {
        if(fs.exists(args.path)) 
            opt = [args.path];
        else {
            cb({'code': 400, 'message': 'start_service: path does not exist'});
            return;
        }
    } else if('classpath' in args) {
        opt = ['plugins/service_container.py', args.classpath];
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

    if(name in services) {
        cb({'code': 400, 'message': 'start_service: a service with that name already exists'});
        return;
    }

    var name = args.params.name;
    var params = args.params;

    opt.push(JSON.stringify(params));
    services[name] = {};
    services[name].path = args.path;
    services[name].params = args.params;

    logger.debug({opts: opt}, 'spawning process');

    processes[name] = spawn('python3', opt, {stdio: 'inherit'})
        .on('exit', (code, signal) => {
            logger.info({service: name, exit_code: code}, "service exited");
            delete processes[name];
            delete services[name];
        })
        .on('error', (e) => {
            logger.error({error: e, args: args}, "unable to spawn service");
        });

    cb(null, {'message': `service [${name}] created`});
}

// args = { 'name': pipeline_name, 'data': "..." }
function post_to_pipeline(args, cb) {
    if(!(args.name in pipelines)) {
        cb({'code': 400, 'message': 'no pipeline with that name'});
        return;
    }

    var pline = pipelines[args.name];
    var msg = new mosaic_message.MosaicMessage();
    var arr = [];
    for(var s in pline) {
        var p = pline[s];
        var service = new mosaic_message.Service();
        service.setId(services[p]['params'].ip + ":" + services[p]['params'].port);
        arr.push(service);
    }
    var pipeline = new mosaic_message.Pipeline();
    pipeline.setServicesList(arr);
    msg.setPipeline(pipeline);
    payload = new mosaic_message.Payload();
    payload.setBody(args.data);
    msg.setPayload(payload);

    var socket = new net.Socket();
    var start = services[pline[0]];
    socket.connect({port: start.params.port, host: start.params.ip}, () => {
        var packet = msg.serializeBinary();
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
    if(!('services' in args)) {
        var msg = 'set_pipeline: service array missing from arguments';
        logger.error({args: args}, msg);
        cb({'code': 400, 'message': msg});
        return;
    }
    if(!Array.isArray(args.services)) {
        var msg = 'set_pipeline: args.services must be an array';
        logger.error({args: args}, msg);
        cb({'code': 400, 'message': msg});
        return;
    }
    if(args.services.length === 0) {
        var msg = 'set_pipeline: args.services must not be empty';
        logger.error({args: args}, msg);
        cb({'code': 400, 'message': msg});
        return;
    }
    for(s in args.services) {
        if(!(s in services)) {
            var msg = 'set_pipeline: no service with that name';
            logger.error({service: s}, msg);
            cb({'code': 400, 'message': msg});
            return;
        }
    }

    pipelines[args.name] = args.services;
    cb(null, {'message': 'ok'});
}

// args = { 'name': "..." }
function shutdown(args, cb) {
    if(args.name in services) {
        var proc = services[args.name].proc;
        delete services[args.name];
        proc.kill('SIGTERM');
        cb(null, {'message': 'service stopped'});
    } else {
        cb({'code': 400, 'message': "shutdown: service unknown"});
    }
}
