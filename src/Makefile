DIRS= \
	--define "_sourcedir $(PWD)" \
	--define "_builddir $(PWD)" \
	--define "_srcrpmdir $(PWD)" \
	--define "_rpmdir $(PWD)"

snapshot:
	rpmbuild $(DIRS) --quiet -bb --define "release $$(date +%s)" tsdb-server.spec

srpm:
	rpmbuild $(DIRS) --quiet -bs --define "release $$(date +%s)" tsdb-server.spec
