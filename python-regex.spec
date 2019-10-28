
# Conditional build:
%bcond_with	doc	# don't build doc
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module	regex
Summary:	Alternative regular expression module, to replace re
Summary(pl.UTF-8):	Alternatywny modułu wyrażeń regularnych w stosunku do oryginalnego re
Name:		python-%{module}
Version:	2018.02.21
Release:	3
License:	PSF
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/r/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	81c128915267f59738b2ac5757b8a460
URL:		https://bitbucket.org/mrabarnett/mrab-regex
BuildRequires:	rpm-pythonprov
# for the py_build, py_install macros
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-devel
#BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-devel
#BuildRequires:	python3-setuptools
%endif
# when using /usr/bin/env or other in-place substitutions
#BuildRequires:	sed >= 4.0
# replace with other requires if defined in setup.py
Requires:	python-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description

%description -l pl.UTF-8

%package -n python3-%{module}
Summary:	Alternative regular expression module, to replace re
Summary(pl.UTF-8):	Alternatywny modułu wyrażeń regularnych w stosunku do oryginalnego re
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{module}

%description -n python3-%{module} -l pl.UTF-8


%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
%py_install
%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc docs README
%{py_sitedir}/_%{module}_core.py[co]
%{py_sitedir}/%{module}.py[co]
%{py_sitedir}/test_%{module}.py[co]
%attr(755,root,root) %{py_sitedir}/_%{module}.so
%{py_sitedir}/%{module}-*-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc docs README
%{py3_sitedir}/%{module}.py
%{py3_sitedir}/test_%{module}.py
%{py3_sitedir}/_%{module}_core.py
%%attr(755,root,root) %{py3_sitedir}/_%{module}.*.so
%{py3_sitedir}/__pycache__/*
%{py3_sitedir}/%{module}-*-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
