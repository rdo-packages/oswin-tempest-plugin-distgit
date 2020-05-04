# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%global module oswin_tempest_plugin
%global plugin oswin-tempest-plugin
%global service oswin-tests-tempest
%global with_doc 1

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc \
This package contains Tempest tests to cover the os-win project. \
Additionally it provides a plugin to automatically load these \
tests into Tempest.

Name:       python-%{service}
Version:    0.2.0
Release:    1%{?dist}
Summary:    Tempest Integration of os-win Project

License:    ASL 2.0
URL:        https://git.openstack.org/cgit/openstack/%{plugin}/
Source0:    http://tarballs.openstack.org/%{plugin}/%{plugin}-%{upstream_version}.tar.gz

BuildArch:  noarch
BuildRequires:    git
BuildRequires:    openstack-macros

%description
%{common_desc}

%package -n python%{pyver}-%{service}
Summary:    Tempest Integration of os-win Project
%{?python_provide:%python_provide python%{pyver}-%{service}}
BuildRequires:    python%{pyver}-devel
BuildRequires:    python%{pyver}-pbr
BuildRequires:    python%{pyver}-setuptools

Requires:    python%{pyver}-pbr >= 3.1.1
Requires:    python%{pyver}-oslo-config >= 2:5.2.0
Requires:    python%{pyver}-oslo-log >= 3.36.0
Requires:    python%{pyver}-oslo-utils >= 3.33.0
Requires:    python%{pyver}-tempest >= 1:18.0.0
Requires:    python%{pyver}-winrm

%description -n python%{pyver}-%{service}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{service}-doc
Summary: Documentation of os-win tempest plugin Project

BuildRequires:    python%{pyver}-sphinx
BuildRequires:    python%{pyver}-oslo-sphinx

%description -n python-%{service}-doc
It contains the documentation for the os-win tempest plugin.
%endif

%prep
%autosetup -n %{plugin}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup
# Remove bundled egg-info
rm -rf %{module}.egg-info

%build
%{pyver_build}

# Generate Docs
%if 0%{?with_doc}
%{pyver_bin} setup.py build_sphinx -b html
# remove the sphinx build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{pyver_install}

%files -n python%{pyver}-%{service}
%license LICENSE
%doc README.rst
%{pyver_sitelib}/%{module}
%{pyver_sitelib}/*.egg-info

%if 0%{?with_doc}
%files -n python-%{service}-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
* Thu Apr 04 2019 RDO <dev@lists.rdoproject.org> 0.2.0-1
- Update to 0.2.0
