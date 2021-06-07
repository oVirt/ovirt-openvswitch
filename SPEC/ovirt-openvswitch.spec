%define ovs_version 2.11
%define ovs_version_to_replace 2.11.1

%global py_openvswitch python3-openvswitch

Name:           ovirt-openvswitch
Version:        %{ovs_version}
Release:        0.2021060703%{?dist}
Summary:        Wrapper RPM for upgrading OVS to newer versions

Group:          System Environment/Daemons
License:        Public Domain
URL:            http://www.openvswitch.org
BuildArch:      noarch

Requires:       openvswitch%{ovs_version}
Requires(pretrans): bash
Requires(pretrans): systemd
Provides:       openvswitch = %{ovs_version}
Obsoletes:      openvswitch <= %{ovs_version_to_replace}
Obsoletes:      openvswitch-dpdk <= %{ovs_version_to_replace}
Obsoletes:      rhv-openvswitch

%description
Wrapper rpm for the openvswitch package

%package -n     ovirt-python-openvswitch
Summary:        Wrapper for python-openvswitch rpm
License:        Public Domain
Requires:       %{py_openvswitch}%{ovs_version}
Provides:       %{py_openvswitch} = %{ovs_version}
Obsoletes:      %{py_openvswitch} <= %{ovs_version_to_replace}
Obsoletes:      rhv-python-openvswitch

%description -n ovirt-python-openvswitch
Wrapper rpm for the base python-openvswitch package

%package        devel
Summary:        Wrapper for openvswitch-devel rpm
License:        Public Domain
Requires:       openvswitch%{ovs_version}-devel
Provides:       openvswitch-devel = %{ovs_version}
Obsoletes:      openvswitch-devel <= %{ovs_version_to_replace}
Obsoletes:      rhv-openvswitch-devel

%description devel
Wrapper rpm for the base openvswitch-devel package

%package        ovn
Summary:        Wrapper for ovn rpm
License:        Public Domain
Requires:       ovn%{ovs_version}
Provides:       openvswitch-ovn = %{ovs_version}
Provides:       ovn = %{ovs_version}
Obsoletes:      ovn <= %{ovs_version_to_replace}
Obsoletes:      rhv-openvswitch-ovn

%description ovn
Wrapper rpm for the base openvswitch-ovn-central package

%package        ovn-central
Summary:        Wrapper for openvswitch-ovn-central rpm
License:        Public Domain
Requires:       ovn%{ovs_version}-central
Requires:       ovirt-openvswitch-ovn
Provides:       openvswitch-ovn-central = %{ovs_version}
Obsoletes:      openvswitch-ovn-central <= %{ovs_version_to_replace}
Obsoletes:      ovn-central <= %{ovs_version_to_replace}
Obsoletes:      rhv-openvswitch-ovn-central

%description ovn-central
Wrapper rpm for the base openvswitch-ovn-central package

%package        ovn-host
Summary:        Wrapper for openvswitch-ovn-host rpm
License:        Public Domain
Requires:       ovn%{ovs_version}-host
Requires:       ovirt-openvswitch-ovn
Provides:       openvswitch-ovn-host = %{ovs_version}
Obsoletes:      openvswitch-ovn-host < %{ovs_version_to_replace}
Obsoletes:      ovn-host <= %{ovs_version_to_replace}
Obsoletes:      rhv-openvswitch-ovn-host

%description    ovn-host
Wrapper rpm for the base openvswitch-ovn-host package

%package        ovn-vtep
Summary:        Wrapper for openvswitch-ovn-vtep rpm
License:        Public Domain
Requires:       ovn%{ovs_version}-vtep
Requires:       ovirt-openvswitch-ovn
Provides:       openvswitch-ovn-vtep = %{ovs_version}
Obsoletes:      openvswitch-ovn-vtep < %{ovs_version_to_replace}
Obsoletes:      ovn-vtep <= %{ovs_version_to_replace}
Obsoletes:      rhv-openvswitch-ovn-vtep

%description    ovn-vtep
Wrapper rpm for the base openvswitch-ovn-vtep package

%package        ovn-common
Summary:        Wrapper for openvswitch-ovn-common rpm
License:        Public Domain
Requires:       ovn%{ovs_version}
Requires:       ovirt-openvswitch-ovn
Provides:       openvswitch-ovn-common = %{ovs_version}
Obsoletes:      openvswitch-ovn-common < %{ovs_version_to_replace}
Obsoletes:      ovn-common <= %{ovs_version_to_replace}
Obsoletes:      rhv-openvswitch-ovn-common

%description    ovn-common
Wrapper rpm for the base openvswitch-ovn-common package

%prep
# Nothing to prepare

%build
# Nothing to build

%install
# Nothing to install

%files
%files -n ovirt-python-openvswitch
%files devel
%files ovn
%files ovn-central
%files ovn-host
%files ovn-vtep
%files ovn-common

%pretrans
preenabled_dir=/var/run/ovirt-openvswitch/enabled
preactive_dir=/var/run/ovirt-openvswitch/active
mkdir -p "$preenabled_dir" "$preactive_dir"
for service in openvswitch ovn-northd ovirt-provider-ovn ovn-controller; do
    if [ "$(systemctl is-enabled "$service")" = "enabled" ]; then
        touch "$preenabled_dir/$service"
    fi
    if [ "$(systemctl is-active "$service")" = "active" ]; then
        touch "$preactive_dir/$service"
    fi
done

%posttrans
preenabled_dir=/var/run/ovirt-openvswitch/enabled
preactive_dir=/var/run/ovirt-openvswitch/active
if [ -d "$preenabled_dir" ]; then
    for service in openvswitch ovn-northd ovirt-provider-ovn ovn-controller; do
        if [ -e "$preenabled_dir/$service" ]; then
            systemctl enable "$service"
            rm "$preenabled_dir/$service"
        fi
        if [ -e "$preactive_dir/$service" ]; then
            systemctl start "$service"
            rm "$preactive_dir/$service"
        fi
    done
fi

%changelog
* Mon Jun 7 2021 Ales Musil <amusil@redhat.com> - 0.2021060703
- Fix obsolete of all rhv-openvswitch packages

* Tue May 25 2021 Ales Musil <amusil@redhat.com> - 0.2021052502
- Obsolete old rhv-openvswitch package

* Fri Jun 05 2020 Dominik Holler <dholler@redhat.com> - 2.11-7
- Initial version

