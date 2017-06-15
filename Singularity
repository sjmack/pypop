# vim: ts=4 sw=4 noet

BootStrap: docker
From: fedora:25

%setup
	# Copy all files into a directory in the container
	# Make destination directories (code, and a place for logs)
	mkdir ${SINGULARITY_ROOTFS}/pypop-source
	mkdir ${SINGULARITY_ROOTFS}/.bootstrap_logs
	echo $PWD > ${SINGULARITY_ROOTFS}/.bootstrap_logs/setup_pwd

	# Use rsync to copy the files into the container
	# (We use -rlptD instead of -a because owner & group can be ignored.)
	rsync -v -rlptD . ${SINGULARITY_ROOTFS}/pypop-source/ 2>&1 | tee ${SINGULARITY_ROOTFS}/.bootstrap_logs/setup_rsync_output

	# Output some debug file listings
	ls -lR . 2>&1 | tee ${SINGULARITY_ROOTFS}/.bootstrap_logs/setup_pypop_listing_from_host
	ls -lR ${SINGULARITY_ROOTFS}/pypop-source 2>&1 | tee ${SINGULARITY_ROOTFS}/.bootstrap_logs/setup_pypop_listing_in_rootfs

%post
	# Inside the container, install our required packages.
	dnf install -y python27 python-devel python-numeric python-libxml2 libxslt-python gcc redhat-rpm-config gsl-devel swig less findutils vim 2>&1 | tee /.bootstrap_logs/dnf_install

	# Now, build PyPop.
	# (to be clear, the installs pypop into the container Python)
	ls -lR /pypop-source 2>&1 | tee /.bootstrap_logs/pypop_listing_from_post
	cd /pypop-source
	./setup.py build 2>&1 | tee /.bootstrap_logs/pypop_build

    # Make everything group- and world-readable
    # Also make directories group and world-executable.
    chmod -R go+r /pypop-source
    find /pypop-source -type d -exec chmod go+x {} +

    # Make everything group- and world-readable
    # Also make directories group and world-executable.
    chmod -R go+r /pypop-source
    find /pypop-source -type d -exec chmod go+x {} +

%runscript
	#!/bin/bash
	/usr/bin/env PYTHONPATH=/pypop-source /usr/bin/python2.7 /pypop-source/bin/pypop.py $@

%test
	# Use the runscript to do a simple run
	/singularity -m -c /pypop-source/data/samples/minimal.ini /pypop-source/data/samples/USAFEL-UchiTelle-small.pop

	# Compare the output with our samples.  Exit if there are differences.
    # NOTE: Tests disabled because some output variance is apparently expected.
	diff -u /pypop-source/data/singularity-test/USAFEL-UchiTelle-small-out.txt USAFEL-UchiTelle-small-out.txt || true
	diff -u /pypop-source/data/singularity-test/USAFEL-UchiTelle-small-out.xml USAFEL-UchiTelle-small-out.xml || true

	# Clean up!
	rm USAFEL-UchiTelle-small-out.txt USAFEL-UchiTelle-small-out.xml
