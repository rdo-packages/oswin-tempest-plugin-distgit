%{!?upstream_version: %global upstream_version %{commit}}
%global commit ef0396e1868e1c851c8cc6c99904d6216e7aacc2
%global shortcommit %(c=%{commit}; echo ${c:0:7})
# DO NOT REMOVE ALPHATAG
%global alphatag .%{shortcommit}git

%global module oswin_tempest_plugin
%global plugin oswin-tempest-plugin
%global service oswin-tests-tempest
%global with_doc 1

%if 0%{?fedora}
%global with_python3 1
%endif

%global common_desc \
This package contains Tempest tests to cover the os-win project. \
Additionally it provides a plugin to automatically load these tests into Tempest.

Name:       python-%{service}
Version:    0.1.0
Release:    1%{?alphatag}%{?dist}
Summary:    Tempest Integration of os-win Project

License:    ASL 2.0
URL:        https://git.openstack.org/cgit/openstack/%{plugin}/
Source0:    http://github.com/openstack/%{plugin}/archive/%{commit}.tar.gz#/%{plugin}-%{shortcommit}.tar.gz

BuildArch:  noarch
BuildRequires:    git
BuildRequires:    openstack-macros

%description
%{common_desc}

package -n python2-%{service}
Summary: python-%{service}
%{?python_provide:%python_provide python2-%{service}}
BuildRequires:    python2-devel
BuildRequires:    python2-pbr
BuildRequires:    python2-setuptools

Requires:    python2-pbr >= 3.1.1
Requires:    python2-oslo-config >= 2:5.2.0
Requires:    python2-oslo-log >= 3.36.0
Requires:    python2-oslo-utils >= 3.33.0
Requires:    python2-tempest >= 1:18.0.0
Requires:    python2-winrm

%description -n python-%{service}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{service}-doc
Summary: python-%{service} documentation

BuildRequires:    python2-sphinx
BuildRequires:    python2-oslo-sphinx

%description -n python-%{service}-doc
It contains the documentation for the os-win tempest plugin.
%endif


%if 0%{?with_python3}
%package -n python3-%{service}
Summary: python3-%{service}
%{?python_provide:%python_provide python3-%{service}}
BuildRequires:    python3-devel
BuildRequires:    python3-pbr
BuildRequires:    python3-setuptools

Requires:    python2-pbr >= 3.1.1
Requires:    python2-oslo-config >= 2:5.2.0
Requires:    python2-oslo-log >= 3.36.0
Requires:    python2-oslo-utils >= 3.33.0
Requires:    python2-tempest >= 1:18.0.0
Requires:    python2-winrm

%description -n python3-%{service}
%{common_desc}
%endif

%prep
%autosetup -n %{plugin}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup
# Remove bundled egg-info
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

%files -n python-%{service}
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
* Thu Sep 06 2018 RDO <dev@lists.rdoproject.org> 0.1.0-1.ef0396egit
- Update to 0.1.0

* Tue Aug 28 2018 Chandan Kumar <chkumar@redhat.com> 0.0.1-0.2.ef0396e1git
- Update to pre-release 0.0.1 (ef0396e1868e1c851c8cc6c99904d6216e7aacc2)
