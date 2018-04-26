//
// Test Classe test_message: standard test mosaic functionalities
// devs@droxit.de - droxIT GmbH
//
// Copyright (c) 2018 droxIT GmbH
//
let expect = require('expect.js');
let describe = require('mocha').describe;
let bunyan = require('bunyan');
let it = require('mocha').it;
let beforeEach = require('mocha').beforeEach;
let path = require('path');
let sleep = require('system-sleep');
let mosaic = require('../mosaic_message.js');

describe('mosaic_message', function () {
	let msg;
	let services;
	let payload;
	beforeEach(function() {
        	msg = new mosaic.Message();
		services = [ new mosaic.Service('127.0.0.1', 5000), new mosaic.Service('::1', 5001) ];
		payload = 'a;sdklfja0eifjq';
		msg.set_payload(payload);
		for (let s in services) {
			msg.add_service(services[s]);
		}
	});

	describe('test correct params in message object', function() {
		it('should have the right params after initialization', function() {
			expect(msg.get_payload()).to.be(payload);
			expect(msg.pipeline).to.eql(services);
			let d = {
				id: msg.id,
				pipeline: services,
				payload: payload
			};
			expect(msg.get_content_as_dict()).to.eql(d);
			expect(msg.pop_service()).to.eql(services[0]);
			expect(msg.pipeline).to.eql([services[1]]);
			expect(msg.peek_service()).to.eql(services[1]);
		});
	});

	describe('test various serialization functions', function() {
		it('should be able to serialize to json and deserialize to the same object', function() {
			let jsonmsg = msg.serialize_to_json();
			let msg2 = mosaic.deserialize_from_json(jsonmsg);
			let d1 = msg.get_content_as_dict();
			let d2 = msg2.get_content_as_dict();
			expect(d1).to.eql(d2);
		});
		it('should be able to serialize to protobuf and deserialize to the same object', function() {
			let jsonmsg = msg.serialize_to_protobuf();
			let msg2 = mosaic.deserialize_from_protobuf(jsonmsg);
			let d1 = msg.get_content_as_dict();
			let d2 = msg2.get_content_as_dict();
			expect(d1).to.eql(d2);
		});
		it('should be able to serialize framed binary and deserialize to the same object', function() {
			let binmsg = msg.serialize();
			let msg2 = mosaic.deserialize(binmsg);
			let d1 = msg.get_content_as_dict();
			let d2 = msg2.get_content_as_dict();
			expect(d1).to.eql(d2);
		});

	});
	sleep(200);
});
	
/*

    def test_serialization(self):
        protomsg = self.msg.serialize_to_protobuf()
        msg2 = mosaic_message.Message.deserialize_from_protobuf(protomsg)
        d1 = self.msg.get_content_as_dict()
        d2 = msg2.get_content_as_dict()
        self.assertEqual(d1, d2)

        jsonmsg = self.msg.serialize_to_json()
        msg2 = mosaic_message.Message.deserialize_from_json(jsonmsg)
        d2 = msg2.get_content_as_dict()
        self.assertEqual(d1, d2)

        binmsg = self.msg.serialize()
        msg2 = mosaic_message.Message.deserialize(binmsg)
        d2 = msg2.get_content_as_dict()
        self.assertEqual(d1, d2)
*/

