#
# Conditional build:
%bcond_without	tests	# unit tests

%define		module	regex
Summary:	Alternative regular expression module, to replace re
Summary(pl.UTF-8):	Moduł wyrażeń regularnych alternatywny dla oryginalnego re
Name:		python3-%{module}
Version:	2022.8.17
Release:	3
License:	PSF, Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/regex/
Source0:	https://files.pythonhosted.org/packages/source/r/regex/%{module}-%{version}.tar.gz
# Source0-md5:	6b3c706a4d275af24f01496c10d516fa
URL:		https://bitbucket.org/mrabarnett/mrab-regex
BuildRequires:	python3-devel >= 1:3.6
BuildRequires:	python3-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python3-modules >= 1:3.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Alternative regular expression module, to replace re.

%description -l pl.UTF-8
Moduł wyrażeń regularnych alternatywny dla oryginalnego re.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build

%if %{with tests}
# directory with test_regex.py must not contain regex*
install -d tests_3
ln regex_3/test_regex.py tests_3/test_regex.py
PYTHONPATH=$(echo $(pwd)/build-3/lib.*) \
%{__python3} tests_3/test_regex.py
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/regex/test_regex.py \
	$RPM_BUILD_ROOT%{py3_sitedir}/regex/__pycache__/test_regex.*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE.txt README.rst docs/Features.html
%dir %{py3_sitedir}/regex
%attr(755,root,root) %{py3_sitedir}/regex/_regex.cpython-*.so
%{py3_sitedir}/regex/*.py
%{py3_sitedir}/regex/__pycache__
%{py3_sitedir}/%{module}-%{version}-py*.egg-info
