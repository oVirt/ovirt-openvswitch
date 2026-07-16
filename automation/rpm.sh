#!/bin/bash -xe

EXPORT_DIR="${EXPORT_DIR:=exported-artifacts}"

mkdir -p "$EXPORT_DIR"

RPMBUILD_ARGS=(
    --define "%_topdir $(pwd)"
    -ba SPEC/ovirt-openvswitch.spec
)

if [[ -n "${PACKAGE_RPM_RELEASE:-}" ]]; then
    RPMBUILD_ARGS+=(--define "package_rpm_release ${PACKAGE_RPM_RELEASE}")
fi
if [[ -n "${RELEASE_SUFFIX:-}" ]]; then
    RPMBUILD_ARGS+=(--define "release_suffix ${RELEASE_SUFFIX}")
fi

rpmbuild "${RPMBUILD_ARGS[@]}"

cp RPMS/noarch/ovirt-openvswitch-*.noarch.rpm "$EXPORT_DIR"/
cp RPMS/noarch/ovirt-python-openvswitch-*.noarch.rpm "$EXPORT_DIR"/
cp SRPMS/ovirt-openvswitch-*.src.rpm "$EXPORT_DIR"/

