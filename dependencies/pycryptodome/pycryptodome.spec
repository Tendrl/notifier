Name: pycryptodome
Version: 3.4.7
Release: 1%{dist}
Source0: %{name}-%{version}.tar.gz
Summary: Cryptographic library for Python
License: BSD
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
Vendor: Helder Eijs <helderijs@gmail.com>
Url: http://www.pycryptodome.org

BuildRequires: python-setuptools
BuildRequires: python2-devel

%description

PyCryptodome is a self-contained Python package of low-level
cryptographic primitives.


%prep
%setup

%build
env CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%install
%{__python} setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
%doc README.rst
%license LICENSE.rst

%changelog
* Fri Oct 06 2017 Timothy Asir Jeyasingh <tjeyasin@redhat.com> - 0.2.1-1
- Initial build.
