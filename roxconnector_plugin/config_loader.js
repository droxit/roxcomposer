// encoding: utf-8
//
// This module provides config-loading support similar to the roxcomposer/config/config_loader.py in python.
// This is used as a workaround to load needed service information like ip and port until we have
// implemented a service callback feature with which the services will report their active configuration
// on their own.
//
// devs@droxit.de
//
// Copyright (c) 2017 droxIT GmbH
//

let fs = require('fs');

module.exports = ConfigModule;

function load_config(file) {
	let f;
	if (file)
		f = file;
	else if ('DROXIT_ROXCOMPOSER_CONFIG' in process.env)
		f = process.env.DROXIT_ROXCOMPOSER_CONFIG;
	else
		return null;

	let config = '';
	let s = '';

	try {
		s = fs.readFileSync(f, 'utf8')
	} catch(e) {
		throw(`unable to read file ${f} - e`);
	}
	try {
		config = JSON.parse(s);
	} catch(e) {
		throw(`config file needs to be correct JSON - ${f}`);
	}

	return config;
}

function ConfigModule(file) {
	this.config = load_config(file);

	if (this.config)
		return this;
	else
		return null;
}

ConfigModule.prototype.get_item = function(key) {
	if (typeof(key) != 'string' || key.length == 0)
		throw 'the key needs to be a string';

	let parts = key.split('\.');
	let c = this.config;
	while(parts.length) {
		k = parts.shift();
		if (k in c) {
			c = c[k];
		} else {
			throw `key not found: ${key}`;
		}
	}

	return c;
}
