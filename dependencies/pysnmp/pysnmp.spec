Name: pysnmp
Version: 4.3.10
Release: 1%{dist}
BuildArch: noarch
Summary: SNMP library for Python

Source0: %{name}-%{version}.tar.gz
License: BSD
Group: Development/Libraries
Vendor: Ilya Etingof <etingof@gmail.com> <etingof@gmail.com>
Url: https://github.com/etingof/pysnmp

BuildRequires: python-setuptools
BuildRequires: python2-devel

Requires: pysmi
Requires: python2-pyasn1

%description
SNMP v1/v2c/v3 engine and apps written in pure-Python.
Supports Manager/Agent/Proxy roles,
scriptable MIBs, asynchronous operation and multiple transports.

%prep
%setup

# Remove bundled egg-info
rm -rf %{name}.egg-info

%build
%{__python} setup.py build

%install
%{__python} setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
%doc README.md
%license LICENSE.txt

%changelog
* Fri Oct 06 2017 Timothy Asir Jeyasingh <tjeyasin@redhat.com> - 4.3.10-1
- Initial build.
