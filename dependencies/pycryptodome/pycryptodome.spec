Name: name pycryptodome
Version: 3.4.7
Release: 1%{release}
Source0: %{name}-%{version}.tar.gz
Summary: Cryptographic library for Python
License: BSD
Group: Development/Libraries
Vendor: Helder Eijs <helderijs@gmail.com>
Url: http://www.pycryptodome.org

%description

PyCryptodome is a self-contained Python package of low-level
cryptographic primitives.


%prep
%setup

%build
env CFLAGS="$RPM_OPT_FLAGS" python setup.py build

%install
python setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
