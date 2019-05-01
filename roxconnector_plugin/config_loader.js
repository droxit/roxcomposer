// encoding: utf-8
//
// This module provides config-loading support similar to the roxcomposer/config/config_loader.py in python.
// This is used as a workaround to load needed service information like ip and port until we have
// implemented a service callback feature with which the services will report their active configuration
// on their own.
//
// |------------------- OPEN SOURCE LICENSE DISCLAIMER -------------------|
// |                                                                      |
// | Copyright (C) 2019  droxIT GmbH - devs@droxit.de                     |
// |                                                                      |
// | This file is part of ROXcomposer.                                    |
// |                                                                      |
// | ROXcomposer is free software: you can redistribute it and/or modify  |
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
