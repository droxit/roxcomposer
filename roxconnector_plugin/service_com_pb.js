/**
 * @fileoverview
 * @enhanceable
 * @suppress {messageConventions} JS Compiler reports an error if a variable or
 *     field starts with 'MSG_' and isn't a translatable message.
 * @public
 *
 * |------------------- OPEN SOURCE LICENSE DISCLAIMER -------------------|
 * |                                                                      |
 * | Copyright (C) 2019  droxIT GmbH - devs@droxit.de                     |
 * |                                                                      |
 * | This file is part of ROXcomposer.                                    |
 * |                                                                      |
 * | ROXcomposer is free software: you can redistribute it and/or modify  |
 * | it under the terms of the GNU Lesser General Public License as       |
 * | published by the Free Software Foundation, either version 3 of the   |
 * | License, or (at your option) any later version.                      |
 * |                                                                      |
 * | This program is distributed in the hope that it will be useful,      |
 * | but WITHOUT ANY WARRANTY; without even the implied warranty of       |
 * | MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the         |
 * | GNU General Public License for more details.                         |
 * |                                                                      |
 * | You have received a copy of the GNU Lesser General Public License    |
 * | along with this program. See also <http://www.gnu.org/licenses/>.    |
 * |                                                                      |
 * |----------------------------------------------------------------------|
 *
 * GENERATED CODE -- DO NOT EDIT!
 * 
 */
var jspb = require('google-protobuf');
var goog = jspb;
var global = Function('return this')();

goog.exportSymbol('proto.service_communication.Parameter', null, global);
goog.exportSymbol('proto.service_communication.Payload', null, global);
goog.exportSymbol('proto.service_communication.Pipeline', null, global);
goog.exportSymbol('proto.service_communication.ROXcomposerMessage', null, global);
goog.exportSymbol('proto.service_communication.Service', null, global);

/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.service_communication.ROXcomposerMessage = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.service_communication.ROXcomposerMessage, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  proto.service_communication.ROXcomposerMessage.displayName = 'proto.service_communication.ROXcomposerMessage';
}


if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto suitable for use in Soy templates.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     com.google.apps.jspb.JsClassTemplate.JS_RESERVED_WORDS.
 * @param {boolean=} opt_includeInstance Whether to include the JSPB instance
 *     for transitional soy proto support: http://goto/soy-param-migration
 * @return {!Object}
 */
proto.service_communication.ROXcomposerMessage.prototype.toObject = function(opt_includeInstance) {
  return proto.service_communication.ROXcomposerMessage.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Whether to include the JSPB
 *     instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.service_communication.ROXcomposerMessage} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.service_communication.ROXcomposerMessage.toObject = function(includeInstance, msg) {
  var f, obj = {
    pipeline: (f = msg.getPipeline()) && proto.service_communication.Pipeline.toObject(includeInstance, f),
    payload: (f = msg.getPayload()) && proto.service_communication.Payload.toObject(includeInstance, f),
    id: jspb.Message.getFieldWithDefault(msg, 3, ""),
    created: jspb.Message.getFieldWithDefault(msg, 4, 0)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.service_communication.ROXcomposerMessage}
 */
proto.service_communication.ROXcomposerMessage.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.service_communication.ROXcomposerMessage;
  return proto.service_communication.ROXcomposerMessage.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.service_communication.ROXcomposerMessage} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.service_communication.ROXcomposerMessage}
 */
proto.service_communication.ROXcomposerMessage.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = new proto.service_communication.Pipeline;
      reader.readMessage(value,proto.service_communication.Pipeline.deserializeBinaryFromReader);
      msg.setPipeline(value);
      break;
    case 2:
      var value = new proto.service_communication.Payload;
      reader.readMessage(value,proto.service_communication.Payload.deserializeBinaryFromReader);
      msg.setPayload(value);
      break;
    case 3:
      var value = /** @type {string} */ (reader.readString());
      msg.setId(value);
      break;
    case 4:
      var value = /** @type {number} */ (reader.readInt64());
      msg.setCreated(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.service_communication.ROXcomposerMessage.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.service_communication.ROXcomposerMessage.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.service_communication.ROXcomposerMessage} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.service_communication.ROXcomposerMessage.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getPipeline();
  if (f != null) {
    writer.writeMessage(
      1,
      f,
      proto.service_communication.Pipeline.serializeBinaryToWriter
    );
  }
  f = message.getPayload();
  if (f != null) {
    writer.writeMessage(
      2,
      f,
      proto.service_communication.Payload.serializeBinaryToWriter
    );
  }
  f = message.getId();
  if (f.length > 0) {
    writer.writeString(
      3,
      f
    );
  }
  f = message.getCreated();
  if (f !== 0) {
    writer.writeInt64(
      4,
      f
    );
  }
};


/**
 * optional Pipeline pipeline = 1;
 * @return {?proto.service_communication.Pipeline}
 */
proto.service_communication.ROXcomposerMessage.prototype.getPipeline = function() {
  return /** @type{?proto.service_communication.Pipeline} */ (
    jspb.Message.getWrapperField(this, proto.service_communication.Pipeline, 1));
};


/** @param {?proto.service_communication.Pipeline|undefined} value */
proto.service_communication.ROXcomposerMessage.prototype.setPipeline = function(value) {
  jspb.Message.setWrapperField(this, 1, value);
};


proto.service_communication.ROXcomposerMessage.prototype.clearPipeline = function() {
  this.setPipeline(undefined);
};


/**
 * Returns whether this field is set.
 * @return {!boolean}
 */
proto.service_communication.ROXcomposerMessage.prototype.hasPipeline = function() {
  return jspb.Message.getField(this, 1) != null;
};


/**
 * optional Payload payload = 2;
 * @return {?proto.service_communication.Payload}
 */
proto.service_communication.ROXcomposerMessage.prototype.getPayload = function() {
  return /** @type{?proto.service_communication.Payload} */ (
    jspb.Message.getWrapperField(this, proto.service_communication.Payload, 2));
};


/** @param {?proto.service_communication.Payload|undefined} value */
proto.service_communication.ROXcomposerMessage.prototype.setPayload = function(value) {
  jspb.Message.setWrapperField(this, 2, value);
};


proto.service_communication.ROXcomposerMessage.prototype.clearPayload = function() {
  this.setPayload(undefined);
};


/**
 * Returns whether this field is set.
 * @return {!boolean}
 */
proto.service_communication.ROXcomposerMessage.prototype.hasPayload = function() {
  return jspb.Message.getField(this, 2) != null;
};


/**
 * optional string id = 3;
 * @return {string}
 */
proto.service_communication.ROXcomposerMessage.prototype.getId = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 3, ""));
};


/** @param {string} value */
proto.service_communication.ROXcomposerMessage.prototype.setId = function(value) {
  jspb.Message.setProto3StringField(this, 3, value);
};


/**
 * optional int64 created = 4;
 * @return {number}
 */
proto.service_communication.ROXcomposerMessage.prototype.getCreated = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 4, 0));
};


/** @param {number} value */
proto.service_communication.ROXcomposerMessage.prototype.setCreated = function(value) {
  jspb.Message.setProto3IntField(this, 4, value);
};



/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.service_communication.Pipeline = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, proto.service_communication.Pipeline.repeatedFields_, null);
};
goog.inherits(proto.service_communication.Pipeline, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  proto.service_communication.Pipeline.displayName = 'proto.service_communication.Pipeline';
}
/**
 * List of repeated fields within this message type.
 * @private {!Array<number>}
 * @const
 */
proto.service_communication.Pipeline.repeatedFields_ = [5];



if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto suitable for use in Soy templates.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     com.google.apps.jspb.JsClassTemplate.JS_RESERVED_WORDS.
 * @param {boolean=} opt_includeInstance Whether to include the JSPB instance
 *     for transitional soy proto support: http://goto/soy-param-migration
 * @return {!Object}
 */
proto.service_communication.Pipeline.prototype.toObject = function(opt_includeInstance) {
  return proto.service_communication.Pipeline.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Whether to include the JSPB
 *     instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.service_communication.Pipeline} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.service_communication.Pipeline.toObject = function(includeInstance, msg) {
  var f, obj = {
    servicesList: jspb.Message.toObjectList(msg.getServicesList(),
    proto.service_communication.Service.toObject, includeInstance)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.service_communication.Pipeline}
 */
proto.service_communication.Pipeline.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.service_communication.Pipeline;
  return proto.service_communication.Pipeline.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.service_communication.Pipeline} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.service_communication.Pipeline}
 */
proto.service_communication.Pipeline.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 5:
      var value = new proto.service_communication.Service;
      reader.readMessage(value,proto.service_communication.Service.deserializeBinaryFromReader);
      msg.addServices(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.service_communication.Pipeline.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.service_communication.Pipeline.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.service_communication.Pipeline} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.service_communication.Pipeline.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getServicesList();
  if (f.length > 0) {
    writer.writeRepeatedMessage(
      5,
      f,
      proto.service_communication.Service.serializeBinaryToWriter
    );
  }
};


/**
 * repeated Service services = 5;
 * @return {!Array.<!proto.service_communication.Service>}
 */
proto.service_communication.Pipeline.prototype.getServicesList = function() {
  return /** @type{!Array.<!proto.service_communication.Service>} */ (
    jspb.Message.getRepeatedWrapperField(this, proto.service_communication.Service, 5));
};


/** @param {!Array.<!proto.service_communication.Service>} value */
proto.service_communication.Pipeline.prototype.setServicesList = function(value) {
  jspb.Message.setRepeatedWrapperField(this, 5, value);
};


/**
 * @param {!proto.service_communication.Service=} opt_value
 * @param {number=} opt_index
 * @return {!proto.service_communication.Service}
 */
proto.service_communication.Pipeline.prototype.addServices = function(opt_value, opt_index) {
  return jspb.Message.addToRepeatedWrapperField(this, 5, opt_value, proto.service_communication.Service, opt_index);
};


proto.service_communication.Pipeline.prototype.clearServicesList = function() {
  this.setServicesList([]);
};



/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.service_communication.Service = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, proto.service_communication.Service.repeatedFields_, null);
};
goog.inherits(proto.service_communication.Service, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  proto.service_communication.Service.displayName = 'proto.service_communication.Service';
}
/**
 * List of repeated fields within this message type.
 * @private {!Array<number>}
 * @const
 */
proto.service_communication.Service.repeatedFields_ = [7];



if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto suitable for use in Soy templates.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     com.google.apps.jspb.JsClassTemplate.JS_RESERVED_WORDS.
 * @param {boolean=} opt_includeInstance Whether to include the JSPB instance
 *     for transitional soy proto support: http://goto/soy-param-migration
 * @return {!Object}
 */
proto.service_communication.Service.prototype.toObject = function(opt_includeInstance) {
  return proto.service_communication.Service.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Whether to include the JSPB
 *     instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.service_communication.Service} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.service_communication.Service.toObject = function(includeInstance, msg) {
  var f, obj = {
    id: jspb.Message.getFieldWithDefault(msg, 6, ""),
    parametersList: jspb.Message.toObjectList(msg.getParametersList(),
    proto.service_communication.Parameter.toObject, includeInstance)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.service_communication.Service}
 */
proto.service_communication.Service.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.service_communication.Service;
  return proto.service_communication.Service.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.service_communication.Service} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.service_communication.Service}
 */
proto.service_communication.Service.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 6:
      var value = /** @type {string} */ (reader.readString());
      msg.setId(value);
      break;
    case 7:
      var value = new proto.service_communication.Parameter;
      reader.readMessage(value,proto.service_communication.Parameter.deserializeBinaryFromReader);
      msg.addParameters(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.service_communication.Service.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.service_communication.Service.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.service_communication.Service} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.service_communication.Service.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getId();
  if (f.length > 0) {
    writer.writeString(
      6,
      f
    );
  }
  f = message.getParametersList();
  if (f.length > 0) {
    writer.writeRepeatedMessage(
      7,
      f,
      proto.service_communication.Parameter.serializeBinaryToWriter
    );
  }
};


/**
 * optional string id = 6;
 * @return {string}
 */
proto.service_communication.Service.prototype.getId = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 6, ""));
};


/** @param {string} value */
proto.service_communication.Service.prototype.setId = function(value) {
  jspb.Message.setProto3StringField(this, 6, value);
};


/**
 * repeated Parameter parameters = 7;
 * @return {!Array.<!proto.service_communication.Parameter>}
 */
proto.service_communication.Service.prototype.getParametersList = function() {
  return /** @type{!Array.<!proto.service_communication.Parameter>} */ (
    jspb.Message.getRepeatedWrapperField(this, proto.service_communication.Parameter, 7));
};


/** @param {!Array.<!proto.service_communication.Parameter>} value */
proto.service_communication.Service.prototype.setParametersList = function(value) {
  jspb.Message.setRepeatedWrapperField(this, 7, value);
};


/**
 * @param {!proto.service_communication.Parameter=} opt_value
 * @param {number=} opt_index
 * @return {!proto.service_communication.Parameter}
 */
proto.service_communication.Service.prototype.addParameters = function(opt_value, opt_index) {
  return jspb.Message.addToRepeatedWrapperField(this, 7, opt_value, proto.service_communication.Parameter, opt_index);
};


proto.service_communication.Service.prototype.clearParametersList = function() {
  this.setParametersList([]);
};



/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.service_communication.Parameter = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.service_communication.Parameter, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  proto.service_communication.Parameter.displayName = 'proto.service_communication.Parameter';
}


if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto suitable for use in Soy templates.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     com.google.apps.jspb.JsClassTemplate.JS_RESERVED_WORDS.
 * @param {boolean=} opt_includeInstance Whether to include the JSPB instance
 *     for transitional soy proto support: http://goto/soy-param-migration
 * @return {!Object}
 */
proto.service_communication.Parameter.prototype.toObject = function(opt_includeInstance) {
  return proto.service_communication.Parameter.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Whether to include the JSPB
 *     instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.service_communication.Parameter} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.service_communication.Parameter.toObject = function(includeInstance, msg) {
  var f, obj = {
    serviceparams: jspb.Message.getFieldWithDefault(msg, 8, "")
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.service_communication.Parameter}
 */
proto.service_communication.Parameter.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.service_communication.Parameter;
  return proto.service_communication.Parameter.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.service_communication.Parameter} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.service_communication.Parameter}
 */
proto.service_communication.Parameter.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 8:
      var value = /** @type {string} */ (reader.readString());
      msg.setServiceparams(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.service_communication.Parameter.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.service_communication.Parameter.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.service_communication.Parameter} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.service_communication.Parameter.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getServiceparams();
  if (f.length > 0) {
    writer.writeString(
      8,
      f
    );
  }
};


/**
 * optional string serviceParams = 8;
 * @return {string}
 */
proto.service_communication.Parameter.prototype.getServiceparams = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 8, ""));
};


/** @param {string} value */
proto.service_communication.Parameter.prototype.setServiceparams = function(value) {
  jspb.Message.setProto3StringField(this, 8, value);
};



/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.service_communication.Payload = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.service_communication.Payload, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  proto.service_communication.Payload.displayName = 'proto.service_communication.Payload';
}


if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto suitable for use in Soy templates.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     com.google.apps.jspb.JsClassTemplate.JS_RESERVED_WORDS.
 * @param {boolean=} opt_includeInstance Whether to include the JSPB instance
 *     for transitional soy proto support: http://goto/soy-param-migration
 * @return {!Object}
 */
proto.service_communication.Payload.prototype.toObject = function(opt_includeInstance) {
  return proto.service_communication.Payload.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Whether to include the JSPB
 *     instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.service_communication.Payload} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.service_communication.Payload.toObject = function(includeInstance, msg) {
  var f, obj = {
    body: jspb.Message.getFieldWithDefault(msg, 9, "")
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.service_communication.Payload}
 */
proto.service_communication.Payload.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.service_communication.Payload;
  return proto.service_communication.Payload.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.service_communication.Payload} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.service_communication.Payload}
 */
proto.service_communication.Payload.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 9:
      var value = /** @type {string} */ (reader.readString());
      msg.setBody(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.service_communication.Payload.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.service_communication.Payload.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.service_communication.Payload} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.service_communication.Payload.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getBody();
  if (f.length > 0) {
    writer.writeString(
      9,
      f
    );
  }
};


/**
 * optional string body = 9;
 * @return {string}
 */
proto.service_communication.Payload.prototype.getBody = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 9, ""));
};


/** @param {string} value */
proto.service_communication.Payload.prototype.setBody = function(value) {
  jspb.Message.setProto3StringField(this, 9, value);
};


goog.object.extend(exports, proto.service_communication);
