# rpms.weserv.nl

Spec files and patches used for building libvips and dependencies in RHEL 8 (and it's derivatives).

## Build instructions

Build the libvips RPM within a Docker container:

* Clone this repository.
    ```bash
    git clone https://github.com/weserv/rpms.git
    cd rpms/
    ```

* Build the container locally.
    ```bash
    docker build -t weserv/rpms .
    ```

* Create rpmbuild working directory and change the ownership to the builder user (uid 1000).
    ```bash
    mkdir ~/rpmbuild
    chown -R 1000:1000 ~/rpmbuild
    ```

* Build the source RPM.
    ```bash
    docker run --cap-add=SYS_ADMIN -v $(pwd):/rpms -v $HOME/rpmbuild:/rpmbuild weserv/rpms \
       mock --buildsrpm -r el8-wsrv-x86_64 --enable-network -D '_disable_source_fetch 0' --resultdir=/rpmbuild/SRPMS \
         --spec=/rpms/vips/vips.spec --sources=/rpms/vips
    ```

* Build the RPM.
    ```bash
    docker run --cap-add=SYS_ADMIN -v $HOME/rpmbuild:/rpmbuild weserv/rpms sh -c '\
      mock --rebuild -r el8-wsrv-x86_64 --resultdir=/rpmbuild/RPMS/"{{target_arch}}"/ \
        $(find /rpmbuild/SRPMS -type f -name "vips*.src.rpm")'
    ```
