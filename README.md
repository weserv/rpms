# weserv/rpms

Spec files and patches used for building the nginx weserv module and dependencies in RHEL 9 (and its derivatives).

## Build instructions

Build the `nginx-mod-weserv` RPM within a Docker container:

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
    docker run --privileged -v $(pwd):/rpms -v $HOME/rpmbuild:/rpmbuild weserv/rpms \
       mock --buildsrpm -r el9-wsrv-x86_64 --enable-network -D '_disable_source_fetch 0' --resultdir=/rpmbuild/SRPMS \
         --spec=/rpms/nginx-mod-weserv/nginx-mod-weserv.spec --sources=/rpms/nginx-mod-weserv
    ```

* Build the RPM.
    ```bash
    docker run --privileged -v $HOME/rpmbuild:/rpmbuild weserv/rpms \
      mock --rebuild -r el9-wsrv-x86_64 --resultdir=/rpmbuild/RPMS/"{{target_arch}}"/ \
        /rpmbuild/SRPMS/nginx-mod-weserv-5.0.0-1.20240812git947dbc4.el9.wsrv.src.rpm
    ```
