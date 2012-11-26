opentsdb-rhel
=============

OpenTSDB server rpm for Red Hat Linux, CentOS, etc.

The ready-to-use rpm is in RPMS/noarch.

Related Chef cookbook: http://community.opscode.com/cookbooks/tsdb-server
Nothing in the rpm assumes Chef; it should be easy to port the cookbook
to other systems. 

Tested on CentOS 5.

Ships local gnuplot executable as the CentOS version is too old.

The java command is assumed to be in $PATH.
