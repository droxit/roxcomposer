var logger = require('bunyan');
var spawn = require('child_process').spawn;
var processes = {};
var pipelines = {};
var address;
var port;
var portrange;

var module.exports = function(container) {
    container['init'] = init;
    container['spawn'] = spawn;
    container['shutdown'] = shutdown;
    container['add_pipeline'] = add_pipeline;
    container['get_services'] = get_services;
    container['get_pipelines'] = get_pipelines;
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
}

/**
 * spawn a new service
 * args need to contain the name of the service and the path to the service module
 **/
function spawn(args, cb) {
    var path = args.path;
    var name = args.name;
    var params = {};
    if('params' in args)
        params = args.params;

    if(name in processes) {
        cb({'code': 400, 'message': 'a service with that name already exists'});
    }

    var opt = [ path, params ];
    processes[name] = spawn('python3', opt)
        .on('exit', (code, signal) => {
            logger.info({service: name, exit_code: code}, "service exited");
            delete processes[name];
        })
        .on('error', (e) => {
            logger.error({error: e, args: args}, "unable to spawn service");
        });

    cb(null, {'message': 'service created'});
}

function get_services() {
    return processes;
}
