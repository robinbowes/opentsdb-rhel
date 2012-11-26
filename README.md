OpenTSDB server rpm for Red Hat Linux, CentOS, etc.

The ready-to-use rpm is in RPMS/noarch.

Related Chef cookbook: http://community.opscode.com/cookbooks/tsdb-server.
Nothing in the rpm assumes Chef; it should be easy to port the cookbook
to other systems. 

Tested on CentOS 5.

Ships local gnuplot executable as the CentOS version is too old.

The java command is assumed to be in $PATH.

Manual installation:

    rpm -i tsdb-server-1.0-1.noarch.rpm
    vi /etc/sysconfig/tsdb-server # Set Zookeeper address
    /etc/init.d/tsdb-server start
    chkconfig tsdb-server on

Verification test:

    # Write a data point.
    echo put test $(date +%s) 42 | nc localhost 4242

    # Read it back.
    curl -v 'http://localhost:4242/q?start=15m-ago&m=sum:test\{\}'
