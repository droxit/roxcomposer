var expect = require('expect.js');
var describe = require('mocha').describe;
var bunyan = require('bunyan');
var it = require('mocha').it;
var mc = {};
require('../mosaic_control.js')(mc);

describe('mosaic_control', function() {
    describe('init()', function() {
        it('should work without passing any arguments', function() {
            mc.init();
        });
    });
    describe('init()', function() {
        it('should work with a bunyan logger', function() {
            var logger = bunyan.createLogger({name: 'mosaic-control-testing', streams: [{level: 'fatal', path: '/dev/null'}]});
            mc.init({logger: logger});
        });
    });
    describe('start_service()', function() {
        it('should raise an exception if invoked without proper arguments', function() {
            expect(mc.start_service).to.throwError();
        });
        it('should raise an exception if invoked without a callback function', function() {
            expect(mc.start_service).withArgs({}).to.throwError();
        });
        it('should raise an exception if cb is not a function', function() {
            expect(mc.start_service).withArgs({}, {}).to.throwError();
        });
        it('should should return an error code >= 400 when invoked without a path or classpath in args', function(done) {
            mc.start_service({}, function(err) {
                if(err.code >= 400)
                    done();
                else
                    done(err);
            });
        });
        it('should should return an error code >= 400 when invoked without a non-existing path in args', function(done) {
            mc.start_service({path: '/bogus/path/from/hell', params: {}}, function(err) {
                if(err.code >= 400)
                    done();
                else
                    done(err);
            });
        });
    });
    describe('post_to_pipeline()', function() {
        it('should should return an error code >= 400 when invoked with an invalid pipeline name', function(done) {
            mc.post_to_pipeline({pipeline: 'blorp'}, function(err) {
                if(err.code >= 400)
                    done();
                else
                    done(err);
            });
        });
    });
    describe('set_pipeline()', function() {
        it('should should return an error code >= 400 when invoked without services parameter', function(done) {
            mc.set_pipeline({name: 'blorp'}, function(err) {
                if(err.code >= 400)
                    done();
                else
                    done(err);
            });
        });
        it('should should return an error code >= 400 when invoked with an empty service array', function(done) {
            mc.set_pipeline({name: 'blorp', services: []}, function(err) {
                if(err.code >= 400)
                    done();
                else
                    done(err);
            });
        });
        it('should should return an error code >= 400 when invoked with a a non-existant service in service array', function(done) {
            mc.set_pipeline({name: 'blorp', services: ['no-there']}, function(err) {
                if(err.code >= 400)
                    done();
                else
                    done(err);
            });
        });
    });
});
