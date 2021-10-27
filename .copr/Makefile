srpm:
	rpmbuild \
		-D "_topdir ." \
		-bs SPEC/ovirt-openvswitch.spec
	cp SRPMS/*.src.rpm $(outdir)
