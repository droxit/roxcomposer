set -e
for f in test/test_mocha*.js; do
	node_modules/mocha/bin/mocha $f;
done
for f in test/test_tape*.js; do
	node_modules/tape/bin/tape $f;
done
