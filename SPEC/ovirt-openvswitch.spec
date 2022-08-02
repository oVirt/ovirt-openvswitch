%define ovs_version 2.15
%define ovn_version 2021
%define version_to_replace 2.11

%global py_openvswitch python3-openvswitch

Name:           ovirt-openvswitch
Version:        %{ovs_version}
Release:        4%{?dist}
Summary:        Wrapper RPM for upgrading OVS to newer versions

Group:          System Environment/Daemons
License:        Public Domain
URL:            http://www.openvswitch.org
BuildArch:      noarch

Requires:       openvswitch%{ovs_version}
Requires(pre): bash
Requires(pre): systemd
Provides:       openvswitch = %{ovs_version}
Obsoletes:      openvswitch%{version_to_replace}
Obsoletes:      rhv-openvswitch

%description
Wrapper rpm for the openvswitch package

%package -n     ovirt-python-openvswitch
Summary:        Wrapper for python-openvswitch rpm
License:        Public Domain
Requires:       %{py_openvswitch}%{ovs_version}
Provides:       %{py_openvswitch} = %{ovs_version}
Obsoletes:      %{py_openvswitch}%{version_to_replace}
Obsoletes:      rhv-python-openvswitch

%description -n ovirt-python-openvswitch
Wrapper rpm for the base python-openvswitch package

%package        devel
Summary:        Wrapper for openvswitch-devel rpm
License:        Public Domain
Requires:       openvswitch%{ovs_version}-devel
Provides:       openvswitch-devel = %{ovs_version}
Obsoletes:      openvswitch%{version_to_replace}-devel
Obsoletes:      rhv-openvswitch-devel

%description devel
Wrapper rpm for the base openvswitch-devel package

%package        ipsec
Summary:        Wrapper for openvswitch-ipsec rpm
License:        Public Domain
Requires:       openvswitch%{ovs_version}-ipsec
Provides:       openvswitch-ipsec = %{ovs_version}
Obsoletes:      openvswitch%{version_to_replace}-ipsec

%description ipsec
Wrapper rpm for the base openvswitch-ipsec package

%package        ovn
Summary:        Wrapper for ovn rpm
License:        Public Domain
Requires:       ovn-%{ovn_version}
Provides:       openvswitch-ovn = %{ovn_version}
Provides:       ovn = %{ovn_version}
Obsoletes:      ovn%{version_to_replace}
Obsoletes:      rhv-openvswitch-ovn

%description ovn
Wrapper rpm for the base openvswitch-ovn-central package

%package        ovn-central
Summary:        Wrapper for openvswitch-ovn-central rpm
License:        Public Domain
Requires:       ovn-%{ovn_version}-central
Requires:       ovirt-openvswitch-ovn
Provides:       openvswitch-ovn-central = %{ovn_version}
Obsoletes:      ovn%{version_to_replace}-central
Obsoletes:      rhv-openvswitch-ovn-central

%description ovn-central
Wrapper rpm for the base openvswitch-ovn-central package

%package        ovn-host
Summary:        Wrapper for openvswitch-ovn-host rpm
License:        Public Domain
Requires:       ovn-%{ovn_version}-host
Requires:       ovirt-openvswitch-ovn
Provides:       openvswitch-ovn-host = %{ovn_version}
Obsoletes:      ovn%{version_to_replace}-host
Obsoletes:      rhv-openvswitch-ovn-host

%description    ovn-host
Wrapper rpm for the base openvswitch-ovn-host package

%package        ovn-vtep
Summary:        Wrapper for openvswitch-ovn-vtep rpm
License:        Public Domain
Requires:       ovn-%{ovn_version}-vtep
Requires:       ovirt-openvswitch-ovn
Provides:       openvswitch-ovn-vtep = %{ovn_version}
Obsoletes:      ovn%{version_to_replace}-vtep
Obsoletes:      rhv-openvswitch-ovn-vtep

%description    ovn-vtep
Wrapper rpm for the base openvswitch-ovn-vtep package

%package        ovn-common
Summary:        Wrapper for openvswitch-ovn-common rpm
License:        Public Domain
Requires:       ovn-%{ovn_version}
Requires:       ovirt-openvswitch-ovn
Provides:       openvswitch-ovn-common = %{ovn_version}
Obsoletes:      ovn%{version_to_replace}
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
%files ipsec
%files ovn
%files ovn-central
%files ovn-host
%files ovn-vtep
%files ovn-common

%pre
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
pre_upgrade_log_dir=/var/log/openvswitch
pre_upgrade_lib_dir=/var/lib/openvswitch
post_upgrade_log_dir=/var/log/ovn
post_upgrade_lib_dir=/var/lib/ovn
mkdir -p "$post_upgrade_log_dir" "$post_upgrade_lib_dir"
for db in ovnnb_db.db ovnsb_db.db; do
    if [ -e "$pre_upgrade_lib_dir/$db" ]; then
        mv "$pre_upgrade_lib_dir/$db" "$post_upgrade_lib_dir/$db"
    fi
done
for log in ovsdb-server-nb.log ovsdb-server-sb.log ovn-northd.log; do
    if [ -e "$pre_upgrade_log_dir/$log" ]; then
        mv "$pre_upgrade_log_dir/$log" "$post_upgrade_log_dir/$log"
    fi
done
chown -R openvswitch:openvswitch "$post_upgrade_log_dir"
chown -R openvswitch:openvswitch "$post_upgrade_lib_dir"
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
* Tue Aug 2 2022 Ales Musil <amusil@redhat.com> - 2.15-4
- Fix permission of the lib and log directory

* Fri Feb 4 2022 Ales Musil <amusil@redhat.com> - 2.15-3
- Use pre instead of pretrans during installation

* Fri Sep 10 2021 Ales Musil <amusil@redhat.com> - 2.15-2
- Add wrapper for openvswitch-ipsec package

* Wed Aug 25 2021 Ales Musil <amusil@redhat.com> - 2.15-1
- Update OvS version to 2.15
- Update OVN version to 2021

* Thu Jun 10 2021 Ales Musil <amusil@redhat.com> - 2.11-1
- Use simpler version numbers

* Mon Jun 7 2021 Ales Musil <amusil@redhat.com> - 0.2021060703
- Fix obsolete of all rhv-openvswitch packages

* Tue May 25 2021 Ales Musil <amusil@redhat.com> - 0.2021052502
- Obsolete old rhv-openvswitch package

* Fri Jun 05 2020 Dominik Holler <dholler@redhat.com> - 2.11-7
- Initial version

