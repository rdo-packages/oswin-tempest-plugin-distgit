%global module oswin_tempest_plugin
%global name python-oswin-tempest-tests-plugin
%global plugin oswin-tempest-plugin
%global service oswin-tests-tempest
%global with_doc 1

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%if 0%{?fedora}
%global with_python3 1
%endif

%global common_desc \
This package contains Tempest tests to cover the os-win project. \
Additionally it provides a plugin to automatically load these tests into Tempest.

%global summary python-%{service} documentation.

Name:		python-%{service}
Version:	XXX
Release:	XXX
Summary:	Tempest Integration of os-win Project

License:    ASL 2.0
URL:		https://git.openstack.org/cgit/openstack/%{plugin}/
Source0:    http://tarballs.openstack.org/%{plugin}/%{plugin}-%{upstream_version}.tar.gz

BuildArch:  noarch

BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  git
BuildRequires:  openstack-macros

Requires:   pbr>=2.0
Requires:   oslo.config>=4.0.0, oslo.config!=4.3.0, oslo.config!=4.4.0
Requires:   oslo.log>=3.22.0
Requires:   oslo.utils>=3.20.0
Requires:   tempest>=16.1.0
Requires:   pywinrm>=0.2.2

%description
%{common_desc}

package -n python2-%{service}
Summary: %{summary}
%{?python_provide:%python_provide python2-%{service}}

%description -n python2-%{service}
%{common_desc}


%if 0%{?with_doc}
%package -n %{service}-doc
Summary: %{summary}

BuildRequires:  python-sphinx
BuildRequires:  python-openstackdocstheme

%description -n python-%{service}-doc
It contains the documentation for the os-win tempest plugin.
%endif


%if 0%{?with_python3}
%package -n python3-%{service}
Summary: %{summary}
%{?python_provide:%python_provide python3-%{service}}
BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools

Requires:   python3-pbr
Requires:   python3-six  >= 1.9.0
Requires:   python3-tempest >= 1:12.2.0
Requires:   python3-oslo-utils
Requires:   python3-oslo-log

%description -n python3-%{service}
%{common_desc}
%endif


%prep
%autosetup -n %{plugin}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup
# Remove bundled egg-ingo
rm -rf %{module}.egg-info

%build
%if 0%{?with_python3}
%py3_build
%endif
%py2_build

# Generate Docs
%if 0%{?with_doc}
%{__python2} setup.py build_sphinx -b html
# remove the sphinx build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%if 0%{?with_python3}
%py3_install
%endif
%py2_install

%files -n python2-%{service}
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{module}
%{python2_sitelib}/*.egg-info

%if 0%{?with_python3}
%files -n python3-%{service}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{module}
%{python3_sitelib}/*.egg-info
%endif

%if 0%{?with_doc}
%files -n python-%{service}-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog

