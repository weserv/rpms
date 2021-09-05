# rpms.weserv.nl

Spec files and patches used for building libvips and dependencies that are not included (or outdated) in RHEL (and it's derivatives).

## Building the RPMs

Build the RPM as a non-root user from your home directory:

* Clone this repository.
    ```bash
    git clone https://github.com/weserv/rpms.git
    ```

* Install build requirements.
    ```bash
    sudo dnf install rpmdevtools mock epel-rpm-macros rust-toolset
    ```

* Set up your `rpmbuild` directory tree.
    ```bash
    rpmdev-setuptree
    ```

* Link the spec files and patches.
    ```bash
    ln -s $HOME/rpms/*/*.spec $HOME/rpmbuild/SPECS/
    ln -s $HOME/rpms/*/*.patch $HOME/rpmbuild/SOURCES/
    ```

* Download remote source files.
    ```bash
    spectool -g -R rpmbuild/SPECS/nasm.spec
    spectool -g -R rpmbuild/SPECS/dav1d.spec
    spectool -g -R rpmbuild/SPECS/cargo-c.spec
    spectool -g -R rpmbuild/SPECS/rav1e.spec
    spectool -g -R rpmbuild/SPECS/libde265.spec
    spectool -g -R rpmbuild/SPECS/libheif.spec
    spectool -g -R rpmbuild/SPECS/cairo.spec
    spectool -g -R rpmbuild/SPECS/harfbuzz.spec
    spectool -g -R rpmbuild/SPECS/librsvg2.spec
    spectool -g -R rpmbuild/SPECS/libspng.spec
    spectool -g -R rpmbuild/SPECS/cgif.spec
    spectool -g -R rpmbuild/SPECS/vips.spec
    ```

* Build the RPMs.
    ```bash
    rpmbuild -ba rpmbuild/SPECS/nasm.spec
    rpmbuild -ba rpmbuild/SPECS/dav1d.spec
    rpmbuild -ba rpmbuild/SPECS/cargo-c.spec
    rpmbuild -ba rpmbuild/SPECS/rav1e.spec
    rpmbuild -ba rpmbuild/SPECS/libde265.spec
    rpmbuild -ba rpmbuild/SPECS/libheif.spec
    rpmbuild -ba rpmbuild/SPECS/cairo.spec
    rpmbuild -ba rpmbuild/SPECS/harfbuzz.spec
    rpmbuild -ba rpmbuild/SPECS/librsvg2.spec
    rpmbuild -ba rpmbuild/SPECS/libspng.spec
    rpmbuild -ba rpmbuild/SPECS/cgif.spec
    rpmbuild -ba rpmbuild/SPECS/vips.spec
    ```
