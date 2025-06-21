%bcond_with devtools

Name:           libjxl
Epoch:          1
Version:        0.11.1
Release:        3%{?dist}
Summary:        JPEG XL image format reference implementation

License:        BSD-3-Clause
URL:            https://jpeg.org/jpegxl/
Source0:        https://github.com/libjxl/libjxl/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  giflib-devel
BuildRequires:  gtest-devel
BuildRequires:  pkgconfig(libhwy)
BuildRequires:  pkgconfig(libbrotlicommon)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(OpenEXR)
BuildRequires:  pkgconfig(zlib)

Requires:       shared-mime-info
Recommends:     jxl-pixbuf-loader = %{epoch}:%{version}-%{release}

%description
This package contains a reference implementation of JPEG XL (encoder and
decoder).

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package utils
Summary:        Utilities for manipulating JPEG XL images
Recommends:     jxl-pixbuf-loader = %{epoch}:%{version}-%{release}

%description utils
This package provides extra utilities for manipulating JPEG XL images.

%if %{with devtools}
%package devtools
Summary:        Development tools for %{name}
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description devtools
This package provides extra development tools for %{name}.
%endif

%package     -n jxl-pixbuf-loader
Summary:        JPEG XL image loader for GTK applications
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
Requires:       gdk-pixbuf2%{?_isa}
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description -n jxl-pixbuf-loader
This package provides a gdk-pixbuf plugin for loading JPEG XL images
in GTK apps.

%package doc
Summary:        Documentation for %{name}
BuildArch:      noarch
BuildRequires:  asciidoc
BuildRequires:  doxygen

%description doc
This package provides the documentation for %{name}.

%prep
%autosetup -p1

# Avoid SONAME bump
sed -i "/JPEGXL_SO_MINOR_VERSION/s/11/10/" lib/CMakeLists.txt

%build
%cmake -DBUILD_TESTING=OFF \
       -DJPEGXL_ENABLE_BENCHMARK=OFF \
       -DJPEGXL_ENABLE_PLUGIN_GIMP210=OFF \
       -DJPEGXL_ENABLE_SJPEG=OFF \
       -DJPEGXL_ENABLE_SKCMS=OFF \
       -DJPEGXL_ENABLE_PLUGINS=ON \
%if %{with devtools}
       -DJPEGXL_ENABLE_DEVTOOLS=ON \
%endif
       -DJPEGXL_FORCE_SYSTEM_BROTLI=ON \
       -DJPEGXL_FORCE_SYSTEM_GTEST=ON \
       -DJPEGXL_FORCE_SYSTEM_HWY=ON \
       -DJPEGXL_FORCE_SYSTEM_LCMS2=ON

%cmake_build -- all doc

%install
%cmake_install

%files
%license LICENSE
%{_libdir}/libjxl.so.0*
%{_libdir}/libjxl_threads.so.0*
%{_libdir}/libjxl_cms.so.0*
%dir %{_datadir}/thumbnailers
%{_datadir}/thumbnailers/jxl.thumbnailer
%{_datadir}/mime/packages/image-jxl.xml

%files devel
%doc CONTRIBUTING.md
%{_includedir}/jxl/
%{_libdir}/libjxl.so
%{_libdir}/libjxl_threads.so
%{_libdir}/libjxl_cms.so
%{_libdir}/libjxl_extras_codec.a
%{_libdir}/pkgconfig/libjxl.pc
%{_libdir}/pkgconfig/libjxl_threads.pc
%{_libdir}/pkgconfig/libjxl_cms.pc

%files utils
%doc CONTRIBUTING.md CONTRIBUTORS README.md
%{_bindir}/cjxl
%{_bindir}/djxl
%{_bindir}/jxlinfo
%{_mandir}/man1/cjxl.1*
%{_mandir}/man1/djxl.1*

%if %{with devtools}
%files devtools
%{_bindir}/djxl_fuzzer_corpus
%{_bindir}/butteraugli_main
%{_bindir}/decode_and_encode
%{_bindir}/display_to_hlg
%{_bindir}/exr_to_pq
%{_bindir}/icc_simplify
%{_bindir}/pq_to_hlg
%{_bindir}/render_hlg
%{_bindir}/tone_map
%{_bindir}/texture_to_cube
%{_bindir}/generate_lut_template
%{_bindir}/ssimulacra_main
%{_bindir}/ssimulacra2
%{_bindir}/xyb_range
%{_bindir}/jxl_from_tree
%{_bindir}/local_tone_map
%endif

%files -n jxl-pixbuf-loader
%license LICENSE
%{_libdir}/gdk-pixbuf-2.0/*/loaders/libpixbufloader-jxl.so

%files doc
%doc doc/*.md
%doc %{_vpath_builddir}/html
%license LICENSE


%changelog
* Sat Jun 21 2025 Kleis Auke Wolthuizen <info@kleisauke.nl> - 1:0.11.1-3
- Import from Fedora
- Keep SONAME at 0.10 for compat
- Rename package to libjxl
- Cleanup spec file
- Remove logic for disabled gimp plugin
- Disable build of devtools by default
- Drop redundant gflags and gperftools dependencies
- Remove bundled sjpeg dependency in favor of libjpeg-turbo
- Remove bundled skcms dependency in favor of lcms2

* Tue Feb 04 2025 Sérgio M. Basto <sergio@serjux.com> - 1:0.11.1-2
- un-bootstrap

* Sun Feb 02 2025 Sérgio M. Basto <sergio@serjux.com> - 1:0.11.1-0.1.0~sonamebump
- Update to 0.11.1 upstream release
- Resolves: rhbz#2312322

* Thu Jan 30 2025 Sérgio M. Basto <sergio@serjux.com> - 1:0.10.4-1
- Update jpegxl to 0.10.4

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.10.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Oct 29 2024 Sérgio M. Basto <sergio@serjux.com> - 1:0.10.3-5
- Fix upgrade path

* Thu Sep 19 2024 Sérgio M. Basto <sergio@serjux.com> - 1:0.10.3-4
- Disable gimp_plugin, jpegxl don't support Gimp 3 yet

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.10.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jul 07 2024 Sérgio M. Basto <sergio@serjux.com> - 1:0.10.3-2
- Fix generation of third_party sources

* Sun Jul 07 2024 Packit <hello@packit.dev> - 1:0.10.3-1
- Update to 0.10.3 upstream release
- Resolves: rhbz#2295526

* Sun Jul 07 2024 Sérgio M. Basto <sergio@serjux.com> - 1:0.10.2-6
- Configure Packit for release automation

* Tue Apr 23 2024 Orion Poplawski <orion@nwra.com> - 1:0.10.2-5
- Rebuild for openexr 3.2.4

* Wed Apr 17 2024 Sérgio M. Basto <sergio@serjux.com> - 1:0.10.2-4
- BR pkgconfig(lcms2) directly to fix build on eln

* Mon Mar 25 2024 Sérgio M. Basto <sergio@serjux.com> - 1:0.10.2-3
- un-bootstrap

* Wed Mar 13 2024 Sérgio M. Basto <sergio@serjux.com> - 1:0.10.2-0.2.0~sonamebump
- fix the build

* Wed Mar 13 2024 Sérgio M. Basto <sergio@serjux.com> - 1:0.10.2-0.1.0~sonamebump
- bootstrap 0.10.2 to start soname bump of jpegxl

* Wed Feb 14 2024 Sérgio M. Basto <sergio@serjux.com> - 1:0.9.2-2
- un-bootstrap jpegxl

* Wed Feb 14 2024 Sérgio M. Basto <sergio@serjux.com> - 1:0.9.2-0.1.0~sonamebump
- bootstrap 0.9.2 to build aom

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.8.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.8.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Aug 10 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1:0.8.2-3
- Drop unused build dependencies

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 22 2023 Sérgio M. Basto <sergio@serjux.com> - 1:0.8.2-1
- Update jpegxl to 0.8.2

* Tue Jun 20 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1:0.8.1-3
- Disable unused Qt5 build dependencies

* Sun Jun 18 2023 Sérgio M. Basto <sergio@serjux.com> - 1:0.8.1-2
- unbootrap soname

* Mon Apr 03 2023 Sérgio M. Basto <sergio@serjux.com> - 1:0.8.1-0.1.0~sonamebump
- Update to 0.8.1 with new soname
- Drop patches because they are already in the code
- Add update_third_party.sh helper script

* Mon Apr 03 2023 Sérgio M. Basto <sergio@serjux.com> - 1:0.7.0-7
- fix epel8 builds

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.7.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 27 2022 Miroslav Suchý <msuchy@fedoraproject.org> - 1:0.7.0-5
- add epoch back

* Sat Nov 19 2022 Robert-André Mauchin <zebob.m@gmail.com> - 0.7.0-4
- Convert to SPDX

* Sun Sep 25 2022 Robert-André Mauchin <zebob.m@gmail.com> - 1:0.7.0-3
- Fix typo

* Sun Sep 25 2022 Robert-André Mauchin <zebob.m@gmail.com> - 1:0.7.0-3
- Add Epoch to Provides. Close: rhbz#2129592

* Sun Sep 25 2022 Robert-André Mauchin <zebob.m@gmail.com> - 1:0.7.0-1
- Fix update path (bump Epoch). Close: rhbz#2129592

* Sat Sep 24 2022 Robert-André Mauchin <zebob.m@gmail.com> - 0.7.0-1
- Update to 0.7.0

* Sun Sep 18 2022 Robert-André Mauchin <zebob.m@gmail.com> - 0.7.0rc-1
- Update to 0.7.0rc

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0~pre1-0.3.0~sonamebump
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jul 09 2022 Robert-André Mauchin <zebob.m@gmail.com> - 0.7.0~pre1-0.2.0~sonamebump
- Unbootstrap

* Sun Jun 19 2022 Robert-André Mauchin <zebob.m@gmail.com> - 0.7.0~pre1-0.1.0~sonamebump
- Update to prerelease 0.7.0

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Dec 17 2021 Robert-André Mauchin <zebob.m@gmail.com> - 0.6.1-8
- Adapt for EPEL9

* Fri Dec 17 2021 Robert-André Mauchin <zebob.m@gmail.com> - 0.6.1-7
- Remove clang reference in favor of gcc-c++

* Sun Nov 21 2021 Björn Esser <besser82@fedoraproject.org> - 0.6.1-6
- Drop manual release override

* Sun Nov 21 2021 Björn Esser <besser82@fedoraproject.org> - 0.6.1-6
- Add manual release override

* Sun Nov 21 2021 Björn Esser <besser82@fedoraproject.org> - 0.6.1-4
- Rebuild without soname bootstrap

* Sun Nov 21 2021 Björn Esser <besser82@fedoraproject.org> - 0.6.1-3
- Fix BuildRequires when bumping soname

* Sun Nov 21 2021 Björn Esser <besser82@fedoraproject.org> - 0.6.1-2
- Set explicit soname

* Sun Nov 21 2021 Robert-André Mauchin <zebob.m@gmail.com> - 0.6.1-1
- Update to 0.6.1 Close: rhbz#2018648

* Sat Oct 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.5-3
- Rebuild for OpenEXR/Imath 3.1

* Tue Sep 07 2021 Robert-André Mauchin <zebob.m@gmail.com> - 0.5-2
- Rebuild. Close: rhbz#1997038

* Thu Aug 19 2021 Robert-André Mauchin <zebob.m@gmail.com> - 0.5-1
- Update to 0.5 Close: rhbz#1994433

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild
 
* Tue Jun 15 2021 Adam Williamson <awilliam@redhat.com> - 0.3.7-3
- libs: drop Recommends: gimp-jxl-plugin to avoid pulling GIMP into Workstation
 
* Mon May 31 2021 Robert-André Mauchin <zebob.m@gmail.com> - 0.3.7-2
- Use Clang instead of GCC due to vector conversion strictness of GCC
- Disable LTO on arm due to Clang 12.0.0 bug
- Close: rhbz#1922638
 
* Mon May 17 2021 Robert-André Mauchin <zebob.m@gmail.com> - 0.3.7-1
- Update to 0.3.7
 
* Sat Jan 30 2021 Robert-André Mauchin <zebob.m@gmail.com> - 0.3-1
- Update to 0.3
 
* Sat Dec 12 2020 Robert-André Mauchin <zebob.m@gmail.com> - 0.1.1-1
- Update to 0.1.1
 
* Wed Jul 15 2020 Robert-André Mauchin <zebob.m@gmail.com> - 0.0.1-0.1.20200715git0a46d01c
- Initial RPM
