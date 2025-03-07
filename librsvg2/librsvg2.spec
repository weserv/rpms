# Use bundled deps as we don't ship the exact right versions for all the
# required rust libraries
%global bundled_rust_deps 1

%global cairo_version 1.17.0

# Disable AVIF support by default to reduce the attack surface
%bcond_with     avif

# Skip tests, including the reftests related to text rendering,
# as exact visual matches cannot be guaranteed.
%bcond_with     tests

Name:           librsvg2
Summary:        An SVG library based on cairo
Version:        2.59.91
Release:        1%{?dist}

License:        LGPL-2.1-or-later
URL:            https://wiki.gnome.org/Projects/LibRsvg
Source0:        https://download.gnome.org/sources/librsvg/2.59/librsvg-%{version}.tar.xz

# Use vendored crate dependencies so we can build offline.
# Created using "cargo vendor"
Source1:        https://rpms.wsrv.nl/sources/%{name}-%{version}-vendor.tar.xz

# Patch to ensure compat with EL9:
# - Revert commit 73c1ee7, ec5d747, c88987b and 166f74f;
# - Downgrade the minimum required Meson version to 0.63.3.
Patch0:         el-9-compat.patch

BuildRequires:  gcc
BuildRequires:  meson >= 0.63.3
BuildRequires:  cargo-c >= 0.9.19
BuildRequires:  cargo-rpm-macros >= 24
BuildRequires:  gi-docgen
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(cairo) >= %{cairo_version}
BuildRequires:  pkgconfig(cairo-gobject) >= %{cairo_version}
BuildRequires:  pkgconfig(cairo-png) >= %{cairo_version}
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
%if %{with avif}
BuildRequires:  pkgconfig(dav1d)
%endif
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(pangoft2)
BuildRequires:  vala
BuildRequires:  /usr/bin/rst2man

Requires:       cairo%{?_isa} >= %{cairo_version}
Requires:       cairo-gobject%{?_isa} >= %{cairo_version}
Recommends:     rsvg-pixbuf-loader

%description
An SVG library based on cairo.

%package devel
Summary:        Libraries and include files for developing with librsvg
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package provides the necessary development libraries and include
files to allow you to develop with librsvg.

%package     -n rsvg-pixbuf-loader
Summary:        SVG image loader for gdk-pixbuf
Requires:       gdk-pixbuf2%{?_isa}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n rsvg-pixbuf-loader
This package provides a gdk-pixbuf plugin for loading SVG images in GTK apps.

%package tools
Summary:        Extra tools for librsvg
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description tools
This package provides extra utilities based on the librsvg library.

%prep
%autosetup -p1 -n librsvg-%{version} %{?bundled_rust_deps:-a1}

%cargo_prep %{?bundled_rust_deps:-v vendor}

# Ensure we build without --locked, as %%cargo_prep removes
# the lock file (Cargo.lock), allowing more wiggle room when
# providing Rust dependencies.
sed -i 's/, "--locked"//g' meson/cargo_wrapper.py

%if 0%{?rhel} <= 9
# https://bugzilla.redhat.com/show_bug.cgi?id=2109099
sed -i "s/'gdk-pixbuf-query-loaders')/& + '-%{__isa_bits}'/" gdk-pixbuf-loader/meson.build
%endif

%if ! 0%{?bundled_rust_deps}
%generate_buildrequires
# cargo-c requires all optional dependencies to be available
%cargo_generate_buildrequires -a
%endif

%build
%if 0%{?rhel} <= 9
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Rust/#_compiler_flags
export RUSTFLAGS="%build_rustflags"
%endif

%meson \
%if %{without avif}
    -Davif=disabled \
%endif
    %{nil}

%meson_build

%cargo_license_summary
%{cargo_license} > LICENSE.dependencies
%if 0%{?bundled_rust_deps}
%cargo_vendor_manifest
%endif

%install
%meson_install

# Not useful in this package.
rm -f %{buildroot}%{_pkgdocdir}/COMPILING.md

%if %{with tests}
%check
%meson_test
%endif

%files
%doc code-of-conduct.md NEWS README.md
%license COPYING.LIB
%license LICENSE.dependencies
%if 0%{?bundled_rust_deps}
%license cargo-vendor.txt
%endif
%{_libdir}/librsvg-2.so.*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/Rsvg-2.0.typelib

%files devel
%{_libdir}/librsvg-2.so
%{_includedir}/librsvg-2.0/
%{_libdir}/pkgconfig/librsvg-2.0.pc
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/Rsvg-2.0.gir
%dir %{_datadir}/vala
%dir %{_datadir}/vala/vapi
%{_datadir}/vala/vapi/librsvg-2.0.vapi
%{_datadir}/vala/vapi/librsvg-2.0.deps
%{_docdir}/Rsvg-2.0

%files -n rsvg-pixbuf-loader
%{_libdir}/gdk-pixbuf-2.0/*/loaders/libpixbufloader_svg.so
%dir %{_datadir}/thumbnailers
%{_datadir}/thumbnailers/librsvg.thumbnailer

%files tools
%{_bindir}/rsvg-convert
%{_mandir}/man1/rsvg-convert.1*

%changelog
* Fri Mar  7 2025 Kleis Auke Wolthuizen <info@kleisauke.nl> - 2.59.91-1
- Update to 2.59.91

* Tue Feb 11 2025 Kleis Auke Wolthuizen <info@kleisauke.nl> - 2.59.90-1
- Update to 2.59.90
- Update EL9 compat patch for RHEL 9.5 which provides Rust 1.79

* Wed Oct 30 2024 Kleis Auke Wolthuizen <info@kleisauke.nl> - 2.59.2-1
- Update to 2.59.2

* Thu Oct  3 2024 Kleis Auke Wolthuizen <info@kleisauke.nl> - 2.59.1-1
- Update to 2.59.1

* Thu Sep 26 2024 Kleis Auke Wolthuizen <info@kleisauke.nl> - 2.59.0-2
- Ensure compiler flags are passed to rustc

* Fri Sep 13 2024 Kleis Auke Wolthuizen <info@kleisauke.nl> - 2.59.0-1
- Update to 2.59.0

* Sun Sep  1 2024 Kleis Auke Wolthuizen <info@kleisauke.nl> - 2.58.94-1
- Update to 2.58.94

* Thu Aug 15 2024 Kleis Auke Wolthuizen <info@kleisauke.nl> - 2.58.93-1
- Update to 2.58.93
- Disable AVIF support by default

* Sat Mar 30 2024 Kleis Auke Wolthuizen <info@kleisauke.nl> - 2.57.3-1
- Update to 2.57.3

* Tue Jan  2 2024 Kleis Auke Wolthuizen <info@kleisauke.nl> - 2.57.1-1
- Update to 2.57.1

* Sat Dec  2 2023 Kleis Auke Wolthuizen <info@kleisauke.nl> - 2.57.0-1
- Update to 2.57.0

* Mon Jul 24 2023 Kleis Auke Wolthuizen <info@kleisauke.nl> - 2.56.3-1
- Update to 2.56.3
- Split gdk-pixbuf loader into a subpackage

* Mon Jun 26 2023 Kleis Auke Wolthuizen <info@kleisauke.nl> - 2.56.1-1
- Update to 2.56.1

* Wed May 17 2023 Kleis Auke Wolthuizen <info@kleisauke.nl> - 2.56.0-1
- Update to 2.56.0
- Enable gtk-doc support

* Tue Oct  4 2022 Kleis Auke Wolthuizen <info@kleisauke.nl> - 2.55.1-1
- Update to 2.55.1

* Thu Aug  4 2022 Kleis Auke Wolthuizen <info@kleisauke.nl> - 2.55.0-1
- Update to 2.55.0

* Wed Jul 27 2022 Kleis Auke Wolthuizen <info@kleisauke.nl> - 2.54.4-1
- Update to 2.54.4
- Disable gtk-doc support as gi-docgen is not available in EPEL 9
  (rhbz#2072649)

* Thu Aug 12 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 2.50.5-3
- Rebuild with Rust 1.52.1

* Tue Jul  6 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 2.50.5-2
- Rebuild with Rust 1.49.0

* Mon May 17 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 2.50.5-1
- Update to 2.50.5

* Sun Feb  7 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 2.50.3-1
- Update to 2.50.3

* Fri Jan  1 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 2.50.2-2
- Import from Fedora
- Build against cairo, harfbuzz from weserv repo

* Wed Nov 25 2020 Kalev Lember <klember@redhat.com> - 2.50.2-1
- Update to 2.50.2

* Mon Oct  5 2020 Kalev Lember <klember@redhat.com> - 2.50.1-1
- Update to 2.50.1

* Fri Sep 11 2020 Kalev Lember <klember@redhat.com> - 2.50.0-1
- Update to 2.50.0

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.48.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 20 2020 Kalev Lember <klember@redhat.com> - 2.48.8-1
- Update to 2.48.8

* Fri Jun 05 2020 Kalev Lember <klember@redhat.com> - 2.48.7-1
- Update to 2.48.7

* Tue Jun 02 2020 Kalev Lember <klember@redhat.com> - 2.48.6-1
- Update to 2.48.6

* Mon Jun 01 2020 Kalev Lember <klember@redhat.com> - 2.48.5-1
- Update to 2.48.5

* Fri Apr 24 2020 Kalev Lember <klember@redhat.com> - 2.48.4-1
- Update to 2.48.4

* Fri Apr 10 2020 Kalev Lember <klember@redhat.com> - 2.48.3-1
- Update to 2.48.3

* Tue Mar 31 2020 Kalev Lember <klember@redhat.com> - 2.48.2-1
- Update to 2.48.2

* Sat Mar 28 2020 Kalev Lember <klember@redhat.com> - 2.48.1-1
- Update to 2.48.1

* Sat Mar 07 2020 Kalev Lember <klember@redhat.com> - 2.48.0-1
- Update to 2.48.0

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.46.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Nov 27 2019 Kalev Lember <klember@redhat.com> - 2.46.4-1
- Update to 2.46.4

* Wed Oct 23 2019 Kalev Lember <klember@redhat.com> - 2.46.3-1
- Update to 2.46.3

* Mon Oct 14 2019 Kalev Lember <klember@redhat.com> - 2.46.2-1
- Update to 2.46.2

* Mon Oct 07 2019 Kalev Lember <klember@redhat.com> - 2.46.1-1
- Update to 2.46.1

* Fri Sep 20 2019 Kalev Lember <klember@redhat.com> - 2.46.0-2
- Backport a patch to fix svg rendering in gnome-initial-setup (#1753183)

* Mon Sep 09 2019 Kalev Lember <klember@redhat.com> - 2.46.0-1
- Update to 2.46.0

* Tue Sep 03 2019 Kalev Lember <klember@redhat.com> - 2.45.92-1
- Update to 2.45.92

* Mon Aug 19 2019 Kalev Lember <klember@redhat.com> - 2.45.91-1
- Update to 2.45.91

* Sun Aug 04 2019 Pete Walter <pwalter@fedoraproject.org> - 2.45.90-1
- Update to 2.45.90

* Fri Jul 26 2019 Pete Walter <pwalter@fedoraproject.org> - 2.45.8-1
- Update to 2.45.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.45.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 08 2019 Kalev Lember <klember@redhat.com> - 2.45.7-1
- Update to 2.45.7

* Tue May 14 2019 Kalev Lember <klember@redhat.com> - 2.45.6-1
- Update to 2.45.6

* Wed Mar 13 2019 Kalev Lember <klember@redhat.com> - 2.45.5-4
- Go back to using bundled rust deps

* Tue Feb 19 2019 Kalev Lember <klember@redhat.com> - 2.45.5-3
- Rebuilt against fixed atk (#1626575)

* Tue Feb 19 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.45.5-2
- Unbundle Rust deps

* Sat Feb 16 2019 Kalev Lember <klember@redhat.com> - 2.45.5-1
- Update to 2.45.5

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.45.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 09 2019 Kalev Lember <klember@redhat.com> - 2.45.4-1
- Update to 2.45.4

* Wed Jan 09 2019 Kalev Lember <klember@redhat.com> - 2.45.3-2
- Fix accidental soname bump

* Wed Jan 09 2019 Kalev Lember <klember@redhat.com> - 2.45.3-1
- Update to 2.45.3

* Sat Dec 29 2018 Kalev Lember <klember@redhat.com> - 2.44.11-1
- Update to 2.44.11

* Tue Dec 18 2018 Kalev Lember <klember@redhat.com> - 2.44.10-1
- Update to 2.44.10

* Wed Nov 14 2018 Kalev Lember <klember@redhat.com> - 2.44.9-1
- Update to 2.44.9

* Fri Oct 26 2018 Kalev Lember <klember@redhat.com> - 2.44.8-1
- Update to 2.44.8

* Tue Oct 09 2018 Kalev Lember <klember@redhat.com> - 2.44.7-1
- Update to 2.44.7

* Fri Sep 28 2018 Kalev Lember <klember@redhat.com> - 2.44.6-1
- Update to 2.44.6

* Wed Sep 26 2018 Kalev Lember <klember@redhat.com> - 2.44.4-1
- Update to 2.44.4

* Thu Sep 20 2018 Kalev Lember <klember@redhat.com> - 2.44.3-1
- Update to 2.44.3

* Fri Sep 07 2018 Kalev Lember <klember@redhat.com> - 2.44.2-2
- Rebuilt against fixed atk (#1626575)

* Wed Sep 05 2018 Kalev Lember <klember@redhat.com> - 2.44.2-1
- Update to 2.44.2

* Wed Aug 08 2018 Kalev Lember <klember@redhat.com> - 2.43.4-1
- Update to 2.43.4
- Use bundled rust deps

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.43.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.43.1-2
- Bump cssparser to 0.24

* Sun Jun 24 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.43.1-1
- Update to 2.43.1

* Tue May 08 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.42.4-1
- Update to 2.42.4

* Thu May 03 2018 Josh Stone <jistone@redhat.com> - 2.42.3-2
- Update rust dependencies.

* Mon Mar 05 2018 Kalev Lember <klember@redhat.com> - 2.42.3-1
- Update to 2.42.3

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.42.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb 02 2018 Kalev Lember <klember@redhat.com> - 2.42.2-1
- Update to 2.42.2

* Wed Jan 31 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.42.1-2
- Switch to %%ldconfig_scriptlets

* Wed Jan 24 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.42.1-1
- Update to 2.42.1

* Sat Dec 16 2017 Kalev Lember <klember@redhat.com> - 2.40.20-1
- Update to 2.40.20

* Mon Oct 09 2017 Kalev Lember <klember@redhat.com> - 2.40.19-1
- Update to 2.40.19

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 20 2017 Kalev Lember <klember@redhat.com> - 2.40.18-1
- Update to 2.40.18

* Tue Apr 11 2017 Kalev Lember <klember@redhat.com> - 2.40.17-1
- Update to 2.40.17
- Remove lib64 rpaths

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Sep 22 2016 Kalev Lember <klember@redhat.com> - 2.40.16-2
- BR vala instead of obsolete vala-tools subpackage

* Thu Jun 09 2016 Kalev Lember <klember@redhat.com> - 2.40.16-1
- Update to 2.40.16

* Sat Apr 02 2016 David King <amigadave@amigadave.com> - 2.40.15-1
- Update to 2.40.15

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 08 2016 David King <amigadave@amigadave.com> - 2.40.13-1
- Update to 2.40.13
- Fix bogus date in changelog

* Wed Dec 02 2015 David King <amigadave@amigadave.com> - 2.40.12-1
- Update to 2.40.12

* Thu Oct 08 2015 Kalev Lember <klember@redhat.com> - 2.40.11-1
- Update to 2.40.11
- Drop ancient librsvg3 obsoletes

* Sat Aug 08 2015 Kalev Lember <klember@redhat.com> - 2.40.10-1
- Update to 2.40.10

* Wed Aug  5 2015 Matthias Clasen <mclasen@redhat.com> - 2.40.9-3
- Rely on gdk-pixbuf2 file triggers

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.40.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Mar 26 2015 Kalev Lember <kalevlember@gmail.com> - 2.40.9-1
- Update to 2.40.9

* Fri Feb 27 2015 David King <amigadave@amigadave.com> - 2.40.8-1
- Update to 2.40.8

* Mon Feb 16 2015 David King <amigadave@amigadave.com> - 2.40.7-1
- Update to 2.40.7
- Use license macro for COPYING and COPYING.LIB
- Use pkgconfig for BuildRequires
- Add URL

* Wed Dec 03 2014 Richard Hughes <rhughes@redhat.com> - 2.40.6-1
- Update to 2.40.6

* Mon Oct 13 2014 Kalev Lember <kalevlember@gmail.com> - 2.40.5-1
- Update to 2.40.5

* Sun Sep 14 2014 Kalev Lember <kalevlember@gmail.com> - 2.40.4-1
- Update to 2.40.4
- Tighten subpackage deps with the _isa macro

* Mon Aug 18 2014 Kalev Lember <kalevlember@gmail.com> - 2.40.3-1
- Update to 2.40.3

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.40.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 2.40.2-3
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.40.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 18 2014 Richard Hughes <rhughes@redhat.com> - 2.40.2-1
- Update to 2.40.2

* Mon Nov 25 2013 Richard Hughes <rhughes@redhat.com> - 2.40.1-1
- Update to 2.40.1

* Tue Oct 29 2013 Richard Hughes <rhughes@redhat.com> - 2.40.0-1
- Update to 2.40.0

* Thu Aug 22 2013 Kalev Lember <kalevlember@gmail.com> - 2.39.0-1
- Update to 2.39.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.37.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat May 11 2013 Kalev Lember <kalevlember@gmail.com> - 2.37.0-3
- Split rsvg-view-3 and rsvg-convert to a -tools subpackage (#915403)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.37.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 15 2013 Matthias Clasen <mclasen@redhat.com> - 2.37.0-1
- Update to 2.37.0

* Tue Oct 16 2012 Kalev Lember <kalevlember@gmail.com> - 2.36.4-1
- Update to 2.36.4

* Sun Sep 23 2012 Kalev Lember <kalevlember@gmail.com> - 2.36.3-1
- Update to 2.36.3
- Package the librsvg Vala bindings

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.36.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 17 2012 Kalev Lember <kalevlember@gmail.com> - 2.36.1-1
- Update to 2.36.1
- Removed unrecognized configure options
- Include the man page in the rpm

* Tue Mar 27 2012 Kalev Lember <kalevlember@gmail.com> - 2.36.0-1
- Update to 2.36.0

* Mon Feb  6 2012 Matthias Clasen <mclasen@redhat.com> - 2.35.2-1
- Update to 2.35.2

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.35.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 20 2011 Matthias Clasen <mclasen@redhat.com> - 2.35.1-1
- Update to 2.35.1

* Sat Dec 10 2011 Hans de Goede <hdegoede@redhat.com> - 2.35.0-3
- Fix including rsvg.h always causing a deprecated warning, as this breaks
  apps compiling with -Werror

* Fri Nov 25 2011 Daniel Drake <dsd@laptop.org> - 2.35.0-2
- Build gobject-introspection bindings

* Tue Nov 22 2011 Matthias Clasen <mclasen@redhat.com> - 2.35.0-1
- Update to 2.35.0

* Mon Nov  7 2011 Matthias Clasen <mclasen@redhat.com> - 2.34.1-2
- Rebuild against new libpng

* Tue Sep  6 2011 Matthias Clasen <mclasen@redhat.com> - 2.34.1-1
- Update to 2.34.1

* Sun Apr  3 2011 Christopher Aillon <caillon@redhat.com> - 2.34.0-1
- Update to 2.34.0

* Fri Feb 18 2011 Matthias Clasen <mclasen@redhat.com> - 2.32.1-3
- Fix a crash (#603183)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.32.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec  3 2010 Matthias Clasen <mclasen@redhat.com> - 2.32.1-1
- Update to 2.32.1

* Mon Oct 18 2010 Parag Nemade <paragn AT fedoraproject.org> - 2.32.0-2
- Merge-review cleanup (#226040)

* Wed Sep 29 2010 Matthias Clasen <mclasen@redhat.com> 2.32.0-1
- Update to 2.32.0

* Mon Jul 19 2010 Bastien Nocera <bnocera@redhat.com> 2.31.0-2
- Fix rawhide upgrade path with librsvg3

* Fri Jul  2 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.0-1
- Update to 2.31.0

* Fri Jul 02 2010 Adam Tkac <atkac redhat com> - 2.31.0-0.3.20100628git
- fix crash in rsvg-gobject.c:instance_dispose function
  (https://bugzilla.gnome.org/show_bug.cgi?id=623383)

* Wed Jun 30 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.0-0.2.20100628git
- Fix the .pc file to require gdk-pixbuf-2.0

* Mon Jun 28 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.0-0.1.20100628git
- Update to a git snapshot that builds against standalone gdk-pixbuf
- Drop librsvg3 package
- Drop svg theme engine

* Fri Jun 11 2010 Bastien Nocera <bnocera@redhat.com> 2.26.3-3
- Add missing scriptlets for librsvg3
- Fix requires for librsvg3-devel package

* Fri Jun 11 2010 Bastien Nocera <bnocera@redhat.com> 2.26.3-2
- Add GTK3 port of the libraries

* Sat May  1 2010 Matthias Clasen <mclasen@redhat.com> - 2.26.3-1
- Update to 2.26.3

* Tue Mar 30 2010 Matthias Clasen <mclasen@redhat.com> - 2.26.2-1
- Update to 2.26.2

* Mon Mar 29 2010 Matthias Clasen <mclasen@redhat.com> - 2.26.1-1
- Update to 2.26.1

* Sun Feb 14 2010 Matthias Clasen <mclasen@redhat.com> - 2.26.0-4
- Add missing libs

* Mon Aug 10 2009 Ville Skyttä <ville.skytta@iki.fi> - 2.26.0-3
- Convert specfile to UTF-8.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 16 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.3-1
- Update to 2.22.3

* Thu Sep 18 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.2-2
- Plug a memory leak

* Tue Mar  4 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.2-1
- Update to 2.22.2

* Sun Feb 24 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.1-1
- Update to 2.22.1

* Thu Feb 21 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-1
- Update to 2.22.0

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.20.0-2
- Autorebuild for GCC 4.3

* Sun Jan 20 2008 Matthias Clasen <mclasen@redhat.com> - 2.20.0-1
- Update to 2.20.0

* Tue Sep 11 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.2-2
- Plug memory leaks

* Mon Sep  3 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.2-1
- Update to 2.18.2

* Mon Sep  3 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.1-1
- Update to 2.18.1

* Thu Aug 23 2007 Adam Jackson <ajax@redhat.com> - 2.18.0-4
- Rebuild for build ID

* Tue Aug  7 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.0-3
- Update license field

* Wed Aug  1 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.0-2
- Don't let scriptlets fail (#243185)

* Fri Jul 27 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.0-1
- Update to 2.18.0

* Sat Nov  4 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.1-1
- Update to 2.16.1

* Tue Sep  5 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0-2.fc6
- Fix multilib issues

* Thu Aug 31 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0-1.fc6
- Update to 2.16.0
- Require pkgconfig in the -devel package

* Thu Aug  3 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.90-1.fc6
- Update to 2.15.90

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.15.0-3.1
- rebuild

* Sun Jun 18 2006 Florian La Roche <laroche@redhat.com>
- change to separate Requires(post/postun) lines

* Mon Jun 12 2006 Bill Nottingham <notting@redhat.com> 2.15.0-2
- remove libtool, automake14 buildreqs

* Wed May 10 2006 Matthias Clasen <mclasen@redhat.com> 2.15.0-1
- Update to 2.15.0
- Don't ship static libs

* Fri May  5 2006 Matthias Clasen <mclasen@redhat.com> 2.14.3-3
- Rebuild against new GTK+
- Require GTK+ 2.9.0

* Tue Apr  4 2006 Matthias Clasen <mclasen@redhat.com> 2.14.3-2
- Update to 2.14.3

* Sun Mar 12 2006 Ray Strode <rstrode@redhat.com> 2.14.2-1
- Update to 2.14.2

* Sat Mar 11 2006 Bill Nottingham <notting@redhat.com> 2.14.1-2
- fix bad libart dep

* Tue Feb 28 2006 Matthias Clasen <mclasen@redhat.com> 2.14.1-1
- Update to 2.14.1

* Sat Feb 25 2006 Matthias Clasen <mclasen@redhat.com> 2.14.0-1
- Update to 2.14.0

* Mon Feb 13 2006 Matthias Clasen <mclasen@redhat.com> 2.13.93-1
- Update to 2.13.93

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.13.92-1.1
- bump again for double-long bug on ppc(64)

* Mon Feb  6 2006 Matthias Clasen <mclasen@redhat.com> 2.13.92-1
- Update to 2.13.92

* Fri Jan 13 2006 Matthias Clasen <mclasen@redhat.com> 2.13.5-1
- Update to 2.13.5

* Tue Jan  3 2006 Jesse Keating <jkeating@redhat.com> 2.13.3-4
- Rebuilt on new gcc

* Fri Dec  9 2005 Alexander Larsson <alexl@redhat.com> 2.13.3-3
- Update dependencies (now cairo only, not libart)

* Fri Dec  2 2005 Matthias Clasen <mclasen@redhat.com> - 2.13.3-2
- Compile with svgz support

* Wed Nov 30 2005 Matthias Clasen <mclasen@redhat.com> - 2.13.3-1
- Update to 2.13.3

* Wed Oct 12 2005 Matthias Clasen <mclasen@redhat.com> - 2.12.7-1
- Newer upstream version

* Thu Oct  6 2005 Matthias Clasen <mclasen@redhat.com> - 2.12.5-1
- New upstream version

* Thu Oct  6 2005 Matthias Clasen <mclasen@redhat.com> - 2.12.4-1
- New upstream version

* Thu Sep 29 2005 Matthias Clasen <mclasen@redhat.com> - 2.12.3-1
- New upstream version

* Wed Aug 31 2005 Matthias Clasen <mclasen@redhat.com> - 2.11.1-1
- New upstream version

* Wed Mar  2 2005 Matthias Clasen <mclasen@redhat.com> - 2.9.5-2
- Rebuild with gcc4

* Wed Jan 26 2005 Matthias Clasen <mclasen@redhat.com> - 2.9.5-1
- update to 2.9.5

* Thu Sep 23 2004 Matthias Clasen <mclasen@redhat.com> - 2.8.1-2
- Must use the same rpm macro for the host triplet as the
  gtk2 package, otherwise things can fall apart.  (#137676)

* Thu Sep 23 2004 Alexander Larsson <alexl@redhat.com> - 2.8.1-1
- update to 2.8.1

* Fri Jul 30 2004 Matthias Clasen <mclasen@redhat.com> - 2.7.2-1
- Update to 2.7.2
- Fix up changelog section

* Mon Jun 28 2004 Dan Williams <dcbw@redhat.com> - 2.6.4-7
- Fix usage of "%%{_bindir}/update-gdk-pixbuf-loaders %%{_host}" 
  to point to right place and architecture

* Thu Jun 24 2004 Matthias Clasen <mclasen@redhat.com> 2.6.4-6
- Properly handle updating of arch-dependent config 
  files.  (#124483)

* Wed Jun 23 2004 Matthias Clasen <mclasen@redhat.com> 2.6.4-5
- PreReq gtk2 instead of just requiring it  (#90697)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri May 21 2004 Matthias Clasen <mclasen@redhat.com> 2.6.4-3
- rebuild

* Mon Apr  5 2004 Warren Togami <wtogami@redhat.com> 2.6.4-2
- BuildRequires libtool, libgnomeui-devel, there may be more
- -devel req libcroco-devel

* Thu Apr  1 2004 Alex Larsson <alexl@redhat.com> 2.6.4-1
- update to 2.6.4

* Wed Mar 17 2004 Alex Larsson <alexl@redhat.com> 2.6.1-2
- rebuild to get new gtk bin age

* Mon Mar 15 2004 Alex Larsson <alexl@redhat.com> 2.6.1-1
- update to 2.6.1

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jan 27 2004 Jonathan Blandford <jrb@redhat.com> 2.4.0-3
- update version
- Buildrequire libcroco

* Fri Oct 24 2003 Alexander Larsson <alexl@redhat.com> 2.4.0-3
- Fix libcroco in link line. Fixes #107875.
- Properly require libgsf and libcroco

* Tue Oct 21 2003 Florian La Roche <Florian.LaRoche@redhat.de> 2.4.0-2
- BuildReq libcroco-devel, seems this _can_ get picked up

* Mon Sep  8 2003 Jonathan Blandford <jrb@redhat.com> 2.4.0-1
- bump to 2.4.0

* Thu Sep  4 2003 Alexander Larsson <alexl@redhat.com> 2.3.1-3
- Don't use the epoch, thats implicitly zero and not defined

* Thu Sep  4 2003 Alexander Larsson <alexl@redhat.com> 2.3.1-2
- full version in -devel requires (#102063)

* Wed Aug 13 2003 Jonathan Blandford <jrb@redhat.com> 2.3.1-1
- new version for GNOME 2.4

* Fri Aug  8 2003 Alexander Larsson <alexl@redhat.com> 2.2.3-5
- BuildRequire libgsf-devel

* Wed Aug  6 2003 Elliot Lee <sopwith@redhat.com> 2.2.3-4
- Fix libtool

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Apr  8 2003 Matt Wilson <msw@redhat.com> 2.2.3-2
- use system libtool (#88339)

* Wed Feb  5 2003 Alexander Larsson <alexl@redhat.com> 2.2.3-1
- 2.2.3
- Moved engine and loaders from devel package

* Mon Feb  3 2003 Alexander Larsson <alexl@redhat.com> 2.2.2.1-2
- Move docs to rpm docdir

* Mon Feb  3 2003 Alexander Larsson <alexl@redhat.com> 2.2.2.1-1
- Update to 2.2.2.1, crash fixes

* Fri Jan 31 2003 Alexander Larsson <alexl@redhat.com> 2.2.1-1
- Update to 2.2.1, fixes crash
- Removed temporary manpage hack

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan 21 2003 Alexander Larsson <alexl@redhat.com> 2.2.0-3
- Manpage were installed in the wrong place

* Tue Jan 21 2003 Alexander Larsson <alexl@redhat.com> 2.2.0-2
- Add manpage

* Tue Jan 21 2003 Alexander Larsson <alexl@redhat.com> 2.2.0-1
- Update to 2.2.0

* Fri Jan 17 2003 Alexander Larsson <alexl@redhat.com> 2.1.3-3
- Require gtk2 2.2.0 for the pixbuf loader (#80857)

* Thu Jan 16 2003 Alexander Larsson <alexl@redhat.com> 2.1.3-2
- own includedir/librsvg-2

* Thu Jan  9 2003 Alexander Larsson <alexl@redhat.com> 2.1.3-1
- update to 2.1.3

* Tue Dec 17 2002 Owen Taylor <otaylor@redhat.com>
- Don't package gdk-pixbuf.loaders, it gets generated 
  in the %%post

* Mon Dec  9 2002 Alexander Larsson <alexl@redhat.com> 2.1.2-1
- Update to 2.1.2

* Sat Jul 27 2002 Havoc Pennington <hp@redhat.com>
- 2.0.1

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue May 21 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Thu May 02 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Thu Apr 18 2002 Havoc Pennington <hp@redhat.com>
- 1.1.6

* Mon Feb 11 2002 Alex Larsson <alexl@redhat.com> 1.1.3-1
- Update to 1.1.3

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan  2 2002 Havoc Pennington <hp@redhat.com>
- new CVS snap 1.1.0.91
- remove automake/autoconf calls

* Mon Nov 26 2001 Havoc Pennington <hp@redhat.com>
- convert to librsvg2 RPM

* Tue Oct 23 2001 Havoc Pennington <hp@redhat.com>
- 1.0.2

* Fri Jul 27 2001 Alexander Larsson <alexl@redhat.com>
- Add a patch that moves the includes to librsvg-1/librsvg
- in preparation for a later librsvg 2 library.

* Tue Jul 24 2001 Havoc Pennington <hp@redhat.com>
- build requires gnome-libs-devel, #49509

* Thu Jul 19 2001 Havoc Pennington <hp@redhat.com>
- own /usr/include/librsvg

* Wed Jul 18 2001 Akira TAGOH <tagoh@redhat.com> 1.0.0-4
- fixed the linefeed problem in multibyte environment. (Bug#49310)

* Mon Jul 09 2001 Havoc Pennington <hp@redhat.com>
- put .la file back in package 

* Fri Jul  6 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Put changelog at the end
- Move .so files to devel subpackage
- Don't mess with ld.so.conf
- Don't use %%{prefix}, this isn't a relocatable package
- Don't define a bad docdir
- Add BuildRequires
- Use %%{_tmppath}
- Don't define name, version etc. on top of the file (why 
  do so many do that?)
- s/Copyright/License/

* Wed May  9 2001 Jonathan Blandford <jrb@redhat.com>
- Put into Red Hat Build system

* Tue Oct 10 2000 Robin Slomkowski <rslomkow@eazel.com>
- removed obsoletes from sub packages and added mozilla and 
  trilobite subpackages

* Wed Apr 26 2000 Ramiro Estrugo <ramiro@eazel.com>
- created this thing

