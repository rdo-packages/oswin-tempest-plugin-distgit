%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%global module oswin_tempest_plugin
%global plugin oswin-tempest-plugin
%global service oswin-tests-tempest
# oslosphinx do not work with sphinx > 2
%global with_doc 0

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc \
This package contains Tempest tests to cover the os-win project. \
Additionally it provides a plugin to automatically load these \
tests into Tempest.

Name:       python-%{service}
Version:    XXX
Release:    XXX
Summary:    Tempest Integration of os-win Project

License:    ASL 2.0
URL:        https://git.openstack.org/cgit/openstack/%{plugin}/
Source0:    http://tarballs.openstack.org/%{plugin}/%{plugin}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        http://tarballs.openstack.org/%{plugin}/%{plugin}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:  noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif
BuildRequires:    git-core
BuildRequires:    openstack-macros

%description
%{common_desc}

%package -n python3-%{service}
Summary:    Tempest Integration of os-win Project
%{?python_provide:%python_provide python3-%{service}}
BuildRequires:    python3-devel
BuildRequires:    python3-pbr
BuildRequires:    python3-setuptools

Requires:    python3-pbr >= 3.1.1
Requires:    python3-oslo-config >= 2:5.2.0
Requires:    python3-oslo-log >= 3.36.0
Requires:    python3-oslo-utils >= 3.33.0
Requires:    python3-tempest >= 1:18.0.0
Requires:    python3-winrm

%description -n python3-%{service}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{service}-doc
Summary: Documentation of os-win tempest plugin Project

BuildRequires:    python3-sphinx
BuildRequires:    python3-oslo-sphinx

%description -n python-%{service}-doc
It contains the documentation for the os-win tempest plugin.
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{plugin}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup
# Remove bundled egg-info
rm -rf %{module}.egg-info

%build
%{py3_build}

# Generate Docs
%if 0%{?with_doc}
%{__python3} setup.py build_sphinx -b html
# remove the sphinx build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{py3_install}

%files -n python3-%{service}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{module}
%{python3_sitelib}/*.egg-info

%if 0%{?with_doc}
%files -n python-%{service}-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
