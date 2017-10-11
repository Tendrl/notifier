Name: python2-pyasn1
Version: 0.3.7
Release: 1%{dist}
BuildArch: noarch
Summary: ASN.1 types and codecs

Source0: pyasn1-%{version}.tar.gz
License: BSD
Group: Development/Libraries
Vendor: Ilya Etingof <etingof@gmail.com> <etingof@gmail.com>
Url: https://github.com/etingof/pyasn1

BuildRequires: python-setuptools
BuildRequires: python2-devel
Provides: python-pyasn1

%description
Pure-Python implementation of ASN.1 types and DER/BER/CER codecs (X.208)
This is a free and open source implementation of ASN.1 types and codecs as
a Python package. ASN.1 solves the data serialization problem.
ASN.1 is designed to serialize data structures of unbounded complexity into
something compact and efficient when it comes to processing the data.

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
* Fri Oct 06 2017 Timothy Asir Jeyasingh <tjeyasin@redhat.com> - 0.3.7-1
- Initial build.
