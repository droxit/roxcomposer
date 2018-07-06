let proto = require('./service_com_pb.js');
let uuid = require('uuid/v4');

exports = module.exports = {};

exports.Service = Service;
exports.Message = Message;
exports.deserialize_from_json = deserialize_from_json;
exports.deserialize_from_protobuf = deserialize_from_protobuf;
exports.deserialize = deserialize;
exports.get_packet_len = get_packet_len;

function get_packet_len(msg) {
	if(msg.length >= 4)
		return Buffer.from(msg).readUInt32BE(0);
	throw('argument too short');
}

function frame_message(msg) {
	let len = msg.length;
	let buf = Buffer.allocUnsafe(4 + len);
	buf.writeUInt32BE(len, 0);
	Buffer.from(msg.buffer).copy(buf, 4);

	return buf;
}

function unframe_message(msg) {
	let l = get_packet_len(msg);
    	if (l + 4 != msg.length)
        	throw (`Message of length ${msg.length} does not match frame header ${l}`);

	return new Uint8Array(msg.slice(4));
}

// ##### SERVICE CLASS CODE ######
function Service(ip, port, parameters=[]) {
	this.ip = ip;
	this.port = port;
	this.parameters = parameters;

	this.encodeId = encodeId;
	this.decodeId = decodeId;
}

function encodeId() {
	return `${this.ip}:${this.port}`;
}

// STATIC
function decodeId(idstring) {
	let parts = idstring.split(':');
	if (parts.length < 2) 
		throw `invalid service id: ${idstring}`;

	let port = parts.pop();
	let ip = parts.join(':');

	return { ip: ip, port: port };
}

// #### MESSAGE CLASS CODE ####
function Message() {
	this.pipeline = [];
	this.id = null;
	this.created = null;
	this.payload = null;

	this.create_id = create_id;
	this.set_payload = set_payload;
	this.get_payload = get_payload;
	this.get_content_as_dict = get_content_as_dict;
	this.pop_service = pop_service;
	this.peek_service = peek_service;
	this.add_service = add_service;
	this.has_empty_pipeline = has_empty_pipeline;
	this.serialize_to_protobuf = serialize_to_protobuf;
	this.serialize_to_json = serialize_to_json;
	this.serialize = serialize;

	this.create_id();
	this.created = Date.now();
}

function create_id() {
	this.id = uuid();
}

function set_payload(data) {
	this.payload = data
}

function get_payload() {
	return this.payload
}

function get_content_as_dict() {
	return {
		id: this.id,
		payload: this.payload,
		pipeline: this.pipeline
	};
}

function pop_service() {
	return this.pipeline.shift();
}

// returns undef if pipeline is empty
function peek_service() {
	return this.pipeline[0];
}

// returns undef if pipeline is empty
function add_service(service) {
	this.pipeline.push(service);
}

function has_empty_pipeline() {
	return this.pipeline.length == 0;
}

function serialize_to_protobuf() {
	pmsg = new proto.ROXcomposerMessage();
	let services = []
	for (let i in this.pipeline) {
		p = this.pipeline[i];
		let s = new proto.Service();
		s.setId(p.encodeId());
		s.setParametersList(p.parameters);
		services.push(s);
	}

	pmsg.setId(this.id);
	let payload = new proto.Payload();
	payload.setBody(this.payload);
	pmsg.setPayload(payload);
	let pipeline = new proto.Pipeline();
	pipeline.setServicesList(services);
	pmsg.setPipeline(pipeline);
	pmsg.setCreated(this.created);

	return pmsg.serializeBinary();
}

// STATIC
function deserialize_from_protobuf(binmsg) {
	let msg = new Message();
	let pmsg = proto.ROXcomposerMessage.deserializeBinary(binmsg);
	msg.set_payload(pmsg.getPayload().getBody());
	msg.id = pmsg.getId()
	let p = pmsg.getPipeline();
	let pipe = [];

	if (p) {
		pipe = p.getServicesList();
	}

	for (let s in pipe) {
		let addr = decodeId(pipe[s].getId());
		msg.add_service(new Service(addr.ip, addr.port, pipe[s].getParametersList()));
	}

	return msg;
}

function serialize_to_json() {
        let msg = {
			id: this.id,
			created: this.created,
			pipeline: this.pipeline.map( (x) => { return { id: x.encodeId(), parameters: x.parameters }; } ),
			payload: this.payload
            };

        return JSON.stringify(msg);
}

// STATIC
function deserialize_from_json(jsonstring) {
	let msg = new Message();
	let d = JSON.parse(jsonstring);
	msg.set_payload(d.payload);
	msg.id = d.id;
	msg.created = d.created;
	for (let i in d.pipeline) {
		let addr = decodeId(d.pipeline[i].id);
		msg.add_service(new Service(addr.ip, addr.port, d.pipeline[i].parameters));
	}

	return msg;
}

function serialize() {
	return frame_message(this.serialize_to_protobuf());
}

// STATIC
function deserialize(msg) {
    return this.deserialize_from_protobuf(unframe_message(msg));
}
        
