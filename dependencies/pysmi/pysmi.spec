Name: pysmi
Version: 0.2.1
Release: 1%{dist}
BuildArch: noarch
Summary: SNMP SMI/MIB Parser

Source0: %{name}-%{version}.tar.gz
License: BSD
Group: Development/Libraries
Vendor: Ilya Etingof <etingof@gmail.com> <etingof@gmail.com>
Url: https://github.com/etingof/pysmi

BuildRequires: python-setuptools
BuildRequires: python2-devel

%description
A pure-Python implementation of SNMP/SMI MIB parsing and conversion library.

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
%license LICENSE.rst

%changelog
* Fri Oct 06 2017 Timothy Asir Jeyasingh <tjeyasin@redhat.com> - 0.2.1-1
- Initial build.
