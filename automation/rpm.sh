#!/bin/bash -xe

EXPORT_DIR="${EXPORT_DIR:=exported-artifacts}"

mkdir -p $EXPORT_DIR

rpmbuild --define "%_topdir `pwd`" -ba SPEC/ovirt-openvswitch.spec

cp RPMS/noarch/ovirt-openvswitch-*.noarch.rpm $EXPORT_DIR/
cp RPMS/noarch/ovirt-python-openvswitch-*.noarch.rpm $EXPORT_DIR/
cp SRPMS/ovirt-openvswitch-*.src.rpm $EXPORT_DIR/

