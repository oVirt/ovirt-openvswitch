#!/bin/bash -xe

mkdir -p exported-artifacts

rpmbuild --define "%_topdir `pwd`" -ba SPEC/ovirt-openvswitch.spec

cp RPMS/noarch/ovirt-openvswitch-*.noarch.rpm exported-artifacts/
cp RPMS/noarch/ovirt-python-openvswitch-*.noarch.rpm exported-artifacts/
cp SRPMS/ovirt-openvswitch-*.src.rpm exported-artifacts/
