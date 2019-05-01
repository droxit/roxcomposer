//
// Test Classe test_message: standard test roxcomposer functionalities
//
// |------------------- OPEN SOURCE LICENSE DISCLAIMER -------------------|
// |                                                                      |
// | Copyright (C) 2019  droxIT GmbH - devs@droxit.de                     |
// |                                                                      |
// | This program is free software: you can redistribute it and/or modify |
// | it under the terms of the GNU General Public License as published by |
// | the Free Software Foundation, either version 3 of the License, or    |
// | (at your option) any later version.                                  |
// |                                                                      |
// | This program is distributed in the hope that it will be useful,      |
// | but WITHOUT ANY WARRANTY; without even the implied warranty of       |
// | MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the         |
// | GNU General Public License for more details.                         |
// |                                                                      |
// | You have received a copy of the GNU General Public License           |
// | along with this program. See also <http://www.gnu.org/licenses/>.    |
// |                                                                      |
// |----------------------------------------------------------------------|
//
let expect = require('expect.js');
let describe = require('mocha').describe;
let bunyan = require('bunyan');
let it = require('mocha').it;
let beforeEach = require('mocha').beforeEach;
let path = require('path');
let sleep = require('system-sleep');
let roxcomposer = require('../roxcomposer_message.js');

describe('roxcomposer_message', function () {
	let msg;
	let services;
	let payload;
	beforeEach(function() {
        	msg = new roxcomposer.Message();
		services = [ new roxcomposer.Service('127.0.0.1', 5000), new roxcomposer.Service('::1', 5001) ];
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
			let msg2 = roxcomposer.deserialize_from_json(jsonmsg);
			let d1 = msg.get_content_as_dict();
			let d2 = msg2.get_content_as_dict();
			expect(d1).to.eql(d2);
		});
		it('should be able to serialize to protobuf and deserialize to the same object', function() {
			let jsonmsg = msg.serialize_to_protobuf();
			let msg2 = roxcomposer.deserialize_from_protobuf(jsonmsg);
			let d1 = msg.get_content_as_dict();
			let d2 = msg2.get_content_as_dict();
			expect(d1).to.eql(d2);
		});
		it('should be able to serialize framed binary and deserialize to the same object', function() {
			let binmsg = msg.serialize();
			let msg2 = roxcomposer.deserialize(binmsg);
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
        msg2 = roxcomposer_message.Message.deserialize_from_protobuf(protomsg)
        d1 = self.msg.get_content_as_dict()
        d2 = msg2.get_content_as_dict()
        self.assertEqual(d1, d2)

        jsonmsg = self.msg.serialize_to_json()
        msg2 = roxcomposer_message.Message.deserialize_from_json(jsonmsg)
        d2 = msg2.get_content_as_dict()
        self.assertEqual(d1, d2)

        binmsg = self.msg.serialize()
        msg2 = roxcomposer_message.Message.deserialize(binmsg)
        d2 = msg2.get_content_as_dict()
        self.assertEqual(d1, d2)
*/

