# Disable clutter added by /usr/lib/rpm/find-debuginfo.sh
%define __debug_install_post %{nil}

Name: tsdb-server
Version: 1.0
Release: %{release}
Summary: Time Series Database server
Group: Systems
License: GPL 
Packager: Jacek Masiulaniec <jacek.masiulaniec@betfair.com>
BuildArch: noarch
Source0: stumbleupon-opentsdb-v1.0.0-0-g66a6b42.tar.gz
Source1: stumbleupon-opentsdb-v1.0.0-0-g66a6b42-dependencies.tar.gz
Source2: gnuplot-4.4.4.tar.gz
BuildRoot: /var/tmp/%{name}-buildroot
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gd-devel
BuildRequires: pango-devel
BuildRequires: libXpm-devel


%prep
%setup -T -q -b 0 -n stumbleupon-opentsdb-66a6b42
%setup -T -q -a 1 -n stumbleupon-opentsdb-66a6b42 -D
%setup -T -q -b 2 -n gnuplot-4.4.4


%build
build_gnuplot() {
	cd gnuplot-4.4.4
	./configure \
		--prefix=/opt/tsdb \
		--with-readline=builtin \
		--without-cairo \
		--without-lua \
		--disable-wxwidgets
	make
	cd ..
}

build_server() {
	cd stumbleupon-opentsdb-66a6b42
	sed -i '/AC_PROG_MKDIR_P/d' configure.ac
	sed -i 's/make "$@"/make/' build.sh
	mkdir -p build/.git
	(
		PATH=$PWD/../gnuplot-4.4.4/src:$PATH
		./build.sh --prefix=/opt/tsdb
	)
	cd ..
}

cd ..
build_gnuplot
build_server


%install
rm -fr $RPM_BUILD_ROOT
cd ..

install_server() {
	cd stumbleupon-opentsdb-66a6b42/build
	make install DESTDIR=$RPM_BUILD_ROOT
	sed -i 's/%d{ISO8601} //' $RPM_BUILD_ROOT/opt/tsdb/share/opentsdb/logback.xml
	mkdir -p $RPM_BUILD_ROOT/var/cache/tsdb
	cd ..
	cp src/create_table.sh $RPM_BUILD_ROOT/opt/tsdb/bin
	cd ..
	cp gnuplot-4.4.4/src/gnuplot $RPM_BUILD_ROOT/opt/tsdb/bin
	mkdir -p $RPM_BUILD_ROOT/opt/tsdb/share/gnuplot/4.4
	cp gnuplot-4.4.4/docs/gnuplot.gih $RPM_BUILD_ROOT/opt/tsdb/share/gnuplot/4.4
}

install_server_service() {
	mkdir -p $RPM_BUILD_ROOT/etc/init.d
	mkdir -p $RPM_BUILD_ROOT/etc/sysconfig
	cp tsdb-server.init $RPM_BUILD_ROOT/etc/init.d/tsdb-server
	cat >>$RPM_BUILD_ROOT/etc/sysconfig/tsdb-server <<EOF
CACHE=/var/cache/tsdb
CACHE_SIZE=1024
PORT=4242
QUORUM=localhost
JVMARGS=
EOF
	mkdir -p $RPM_BUILD_ROOT/var/log/tsdb-server
}

install_server_purger() {
	mkdir -p $RPM_BUILD_ROOT/etc/cron.hourly
	cp tsdb-purge $RPM_BUILD_ROOT/etc/cron.hourly
}

install_server
install_server_service
install_server_purger


%clean
rm -rf $RPM_BUILD_ROOT


%description
TSDB server part.


%post
chkconfig --add tsdb-server


%preun
s="tsdb-server"
service $s stop >/dev/null
chkconfig --del $s


%files
%defattr(644,root,root,755)
%attr(0755,root,root) /etc/cron.hourly/tsdb-purge
%attr(0755,root,root) /etc/init.d/tsdb-server
%config(noreplace) /etc/sysconfig/tsdb-server
%attr(0755,root,root) /opt/tsdb/bin/*
%attr(0755,root,root) /opt/tsdb/share/opentsdb/*.sh
%dir /opt/tsdb/share/opentsdb
/opt/tsdb/share/opentsdb/*.jar
/opt/tsdb/share/opentsdb/*.xml
/opt/tsdb/share/opentsdb/static
%dir /opt/tsdb/share/gnuplot
%dir /opt/tsdb/share/gnuplot/4.4
/opt/tsdb/share/gnuplot/4.4/*.gih
%dir /var/cache/tsdb
%dir /var/log/tsdb-server
