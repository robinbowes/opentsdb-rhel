DIRS= \
	--define "_sourcedir $(PWD)/src" \
	--define "_builddir $(PWD)/src" \
	--define "_srcrpmdir $(PWD)/SRPMS" \
	--define "_rpmdir $(PWD)/RPMS"

snapshot:
	rpmbuild $(DIRS) --quiet -bb --define "release $$(date +%s)" src/tsdb-server.spec

release:
	rpmbuild $(DIRS) --quiet -bb --define "release 1" src/tsdb-server.spec

srpm:
	rpmbuild $(DIRS) --quiet -bs --define "release 1" src/tsdb-server.spec
