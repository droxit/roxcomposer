var bunyan = require('bunyan');
var spawn = require('child_process').spawn;
var net = require('net');
var mosaic_message = require('./service_com_pb.js');
var processes = {};
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
    address = args.address;
    port = args.port;
    portrange = args.portrange_start;
    logger = args.logger;
}

/**
 * spawn a new service
 * args need to contain the name of the service and the path to the service module
 **/
function start_service(args, cb) {
    var path = args.path;
    var name = args.name;
    var params = args.params;

    if(name in processes) {
        cb({'code': 400, 'message': 'a service with that name already exists'});
    }

    var opt = [ path, JSON.stringify(params) ];
    processes[name] = {};
    processes[name].path = args.path;
    processes[name].params = args.params;
    spawn('python3', opt)
        .on('exit', (code, signal) => {
            logger.info({service: name, exit_code: code}, "service exited");
            delete processes[name];
        })
        .on('error', (e) => {
            logger.error({error: e, args: args}, "unable to spawn service");
        });

    cb(null, {'message': 'service created'});
}

// args = { 'name': pipeline_name, 'data': "..." }
function post_to_pipeline(args, cb) {
    if(!(args.name in pipelines)) {
        cb({'code': 400, 'message': 'no pipeline with that name'});
        return;
    }

    var pline = pipelines[args.name];
    var msg = new mosaic_message.MosaicMessage();
    for(var s in pline) {
        var p = pline[s];
        var service = new mosaic_message.Service();
        service.setId(processes[p].params.ip + ":" + processes[p].params.port);
        msg.getPipeline().addService(service);
    }
    msg.getPayload().setBody(args.data);

    var socket = new net.Socket();
    var start = processes[pline[0]];
    socket.connect({port: start.args.port, host: start.args.ip}, () => {
        socket.end(msg.serializeBinary());
        cb(null, {'message': 'pipeline initiated'});
    });
    socket.on('error', (e) => {
        logger.error({error: e}, "unable to connect to service");
        cb({'code': 500, 'message': 'internal server error'});
    });
}

// no args required
function get_services(args, cb) {
    cb(null, processes);
}

// no args required
function get_pipelines(args, cb) {
    cb(null, pipelines);
}

// args = { 'name': "...", 'pipeline': [ ... service names ... ] }
function set_pipeline(args, cb) {
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
        cb({'code': 400, 'message': "service unknown"});
    }
}
