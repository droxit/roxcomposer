version != ./version.sh

python_package-files != find roxcomposer -name '*.py' | grep -v 'tests/' | grep -v '__init__.py' | grep -v 'pycache'
python_package = dist/roxcomposer-$(version).tar.gz

composer_base = roxcomposer-demo-$(version)

build_base = build
build_dir = $(build_base)/$(composer_base)
build_package_dir = $(build_dir)/packages
build_logs_dir = $(build_dir)/logs
build_dir_connector = $(build_dir)/api-server
build_dir_connector_plugins = $(build_dir_connector)/plugins
build_dirs = $(build_dir) $(build_package_dir) $(build_logs_dir) $(build_dir_connector_plugins)

connector_version != cat ROXCONNECTOR
connector_package_base = roxconnector-$(connector_version)
connector_package_files = $(build_package_dir)/$(connector_package_base)
connector_archive := $(connector_package_base).tgz
connector_package = $(build_package_dir)/$(connector_archive)
connector_link = https://artifacts.droxit.de/opt/artifacts/roxconnector/release/$(connector_archive)

composer_scripts = scripts/install.sh scripts/start_server.sh

demo_package = $(build_dir).tar.gz

cli_files != find cli |  grep '\.py\|\.json' | grep -v '__init__.py' | grep -v 'pycache'
elk_files != find elastic | grep '\.yml'

service_container = util/service_container.py

.PHONY: test

test:
	python3 setup.py test
	cd roxconnector_plugin; npm test; cd ..

python-package: $(python_package)

$(python_package): $(python_package_files)
	ROXCOMPOSER_VERSION=$(version) python3 setup.py sdist

$(build_dir):
	mkdir -p $(build_dir)

$(build_package_dir):
	mkdir -p $(build_dir)/packages

$(build_logs_dir):
	mkdir -p $(build_dir)/logs

$(build_dir_connector_plugins):
	mkdir -p $(build_dir_connector_plugins)

connector: $(connector_package)

$(connector_package): ROXCONNECTOR | $(build_package_dir) 
	if [ $$ARTIFACT_AUTH ]; then curl -s -u "$$ARTIFACT_AUTH" $(connector_link) > $(connector_package); else echo -n "username for artifacts.droxit.de: "; read art_user; curl -s -u "$$art_user" $(connector_link) > $(connector_package); fi

demo-package: $(demo_package)

$(demo_package): $(python_package) $(cli-files) $(elk-files) $(connector_package) $(composer_scripts) | $(build_dirs)
	cp $(python_package) $(build_package_dir)
	cp --parents $(elk_files) $(build_dir)
	pushd $(build_package_dir); tar x --one-top-level --strip-components=1 -f $(connector_archive); popd
	cp `find $(connector_package_files) -name '*.js'` $(connector_package_files)/package.json $(build_dir_connector)
	cp roxconnector_plugin/{*.js,package.json} $(build_dir_connector_plugins) 
	cp --parents $(cli_files) $(build_dir)
	cp $(composer_scripts) $(build_dir)
	cp $(service_container) $(build_dir_connector_plugins)
	cd demo-files; cp -r config assets ../$(build_dir_connector); cd ..
	cp requirements.txt $(build_dir)
	cd $(build_base); tar cz --exclude $(connector_package_base)* -f $(composer_base).tar.gz $(composer_base); cd ..

