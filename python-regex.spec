#
# Conditional build:
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module	regex
Summary:	Alternative regular expression module, to replace re
Summary(pl.UTF-8):	Moduł wyrażeń regularnych alternatywny dla oryginalnego re
Name:		python-%{module}
Version:	2020.11.13
Release:	2
License:	PSF, Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/regex/
Source0:	https://files.pythonhosted.org/packages/source/r/regex/%{module}-%{version}.tar.gz
# Source0-md5:	4310bfc300d49224476fcd032a8ce5f7
URL:		https://bitbucket.org/mrabarnett/mrab-regex
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.6
BuildRequires:	python3-setuptools
%endif
Requires:	python-modules >= 1:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Alternative regular expression module, to replace re.

%description -l pl.UTF-8
Moduł wyrażeń regularnych alternatywny dla oryginalnego re.

%package -n python3-%{module}
Summary:	Alternative regular expression module, to replace re
Summary(pl.UTF-8):	Moduł wyrażeń regularnych alternatywny dla oryginalnego re
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.6

%description -n python3-%{module}
Alternative regular expression module, to replace re.

%description -n python3-%{module} -l pl.UTF-8
Moduł wyrażeń regularnych alternatywny dla oryginalnego re.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
# directory with test_regex.py must not contain regex*
install -d tests_2
ln regex_2/test_regex.py tests_2/test_regex.py
PYTHONPATH=$(echo $(pwd)/build-2/lib.*) \
%{__python} tests_2/test_regex.py
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
# directory with test_regex.py must not contain regex*
install -d tests_3
ln regex_3/test_regex.py tests_3/test_regex.py
PYTHONPATH=$(echo $(pwd)/build-3/lib.*) \
%{__python3} tests_3/test_regex.py
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/regex/test_regex.py*
%endif

%if %{with python3}
%py3_install

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/regex/test_regex.py \
	$RPM_BUILD_ROOT%{py3_sitedir}/regex/__pycache__/test_regex.*
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENSE.txt README.rst docs/Features.html
%dir %{py_sitedir}/regex
%attr(755,root,root) %{py_sitedir}/regex/_regex.so
%{py_sitedir}/regex/*.py[co]
%{py_sitedir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc LICENSE.txt README.rst docs/Features.html
%dir %{py3_sitedir}/regex
%attr(755,root,root) %{py3_sitedir}/regex/_regex.cpython-*.so
%{py3_sitedir}/regex/*.py
%{py3_sitedir}/regex/__pycache__
%{py3_sitedir}/%{module}-%{version}-py*.egg-info
%endif
