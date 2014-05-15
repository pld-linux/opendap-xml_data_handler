#
# Conditional build:
%bcond_with	tests	# make check (requires BES server)
#
Summary:	Basic request handling the OPeNDAP data server
Summary(pl.UTF-8):	Obsługa podstawowych zapytań dla serwera danych OPeNDAP
Name:		opendap-xml_data_handler
Version:	1.0.4
Release:	1
License:	LGPL v2.1+
Group:		Daemons
Source0:	http://www.opendap.org/pub/source/xml_data_handler-%{version}.tar.gz
# Source0-md5:	9762a8b761c6c21d3ebbacd23e37e9b1
Patch0:		%{name}-libdap.patch
URL:		http://opendap.org/
BuildRequires:	autoconf >= 2.62
BuildRequires:	automake >= 1:1.10
%{?with_tests:BuildRequires:	bes >= 3.13.0}
BuildRequires:	bes-devel >= 3.13.0
%{?with_tests:BuildRequires:	cppunit-devel >= 1.12.0}
BuildRequires:	libdap-devel >= 3.13.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	pkgconfig
Requires:	bes >= 3.13.0
Requires:	libdap >= 3.13.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains a general purpose handler for use with the Hyrax
data server. This handler takes input from a 'data handler' and
returns XML document that encodes both dataset metadata and values. It
is intended to be used for small data requests and web systems that
need data in XML documents.

%description -l pl.UTF-8
Ten pakiet zawiera moduł obsługi ogólnego przeznaczenia przeznaczony
dla serwera danych Hyrax. Moduł ten przyjmuje dane wejściowe z modułu
obsługi danych (data handler) i zwraca dokuemnt XML, zawierający
zakodowane zarówno metadane, jak i wartości zbioru danych. Jest
przeznaczony do użycia dla ządań małych danych oraz systemów WWW
wymagających danych w dokumentach XML.

%prep
%setup -q -n xml_data_handler-%{version}
%patch0 -p1

%build
# rebuild autotools for -as-needed to work
%{__libtoolize}
%{__aclocal} -I conf
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/bes/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog NEWS README
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bes/modules/xml_data_handler.conf
%attr(755,root,root) %{_libdir}/bes/libxml_data_module.so
