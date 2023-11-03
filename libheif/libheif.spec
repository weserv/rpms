Name:           libheif
Epoch:          1
Version:        1.17.3
Release:        1%{?dist}
Summary:        HEIF and AVIF file format decoder and encoder

License:        LGPL-3.0-or-later and MIT
URL:            https://github.com/strukturag/%{name}
Source0:        %{url}/releases/download/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
#BuildRequires: pkgconfig(libsharpyuv) TODO requires libwebp >= 1.3.0
BuildRequires:  pkgconfig(dav1d)
BuildRequires:  pkgconfig(libde265)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(rav1e)

%description
libheif is an ISO/IEC 23008-12:2017 HEIF and AVIF (AV1 Image File Format)
file format decoder and encoder.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        tools
Summary:        Tools for manipulating HEIF files
License:        MIT
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires:       shared-mime-info

%description    tools
This package provides tools for manipulating HEIF files.

%package -n     heif-pixbuf-loader
Summary:        HEIF image loader for GTK+ applications
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires:       gdk-pixbuf2%{?_isa}

%description -n heif-pixbuf-loader
This package provides a plugin to load HEIF files in GTK+ applications.

%prep
%autosetup -p1
rm -rf third-party/


%build
%cmake -DENABLE_PLUGIN_LOADING=0 \
       -DWITH_DAV1D=1 \
       -DWITH_DAV1D_PLUGIN=0 \
       -DWITH_RAV1E=1 \
       -DWITH_RAV1E_PLUGIN=0 \
       -DWITH_X265=0 \
       -DWITH_AOM_DECODER=0 \
       -DWITH_AOM_ENCODER=0

%cmake_build


%install
%cmake_install

%ldconfig_scriptlets


%files
%license COPYING
%doc README.md
%{_libdir}/*.so.1*

%files devel
%{_includedir}/%{name}/
%{_libdir}/cmake/%{name}/
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/*.so

%files tools
%{_bindir}/heif-*
%{_mandir}/man1/heif-*
%{_datadir}/thumbnailers/heif.thumbnailer

%files -n heif-pixbuf-loader
%{_libdir}/gdk-pixbuf-2.0/*/loaders/libpixbufloader-heif.so


%changelog
* Fri Nov  3 2023 Kleis Auke Wolthuizen <info@kleisauke.nl> - 1.17.3-1
- Update to 1.17.3

* Thu Oct 19 2023 Kleis Auke Wolthuizen <info@kleisauke.nl> - 1.17.1-1
- Update to 1.17.1

* Mon Jun 26 2023 Kleis Auke Wolthuizen <info@kleisauke.nl> - 1.16.2-1
- Update to 1.16.2

* Wed May 10 2023 Kleis Auke Wolthuizen <info@kleisauke.nl> - 1.16.1-1
- Update to 1.16.1

* Sun Apr  2 2023 Kleis Auke Wolthuizen <info@kleisauke.nl> - 1.15.2-1
- Bump epoch
- Update to 1.15.2
- Split tools and gdk-pixbuf loader to subpackages

* Sun Mar 19 2023 Kleis Auke Wolthuizen <info@kleisauke.nl> - 1.15.1-1
- Update to 1.15.1

* Mon Jan  9 2023 Kleis Auke Wolthuizen <info@kleisauke.nl> - 1.14.2-1
- Update to 1.14.2

* Sun Nov 20 2022 Kleis Auke Wolthuizen <info@kleisauke.nl> - 1.14.0-1
- Update to 1.14.0

* Mon May 17 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 1.12.0-1
- Update to 1.12.0

* Sun Feb  7 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 1.11.0-1
- Update to 1.11.0

* Fri Jan  1 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 1.10.0-2
- Import from rpmfusion
- Disable x265
- Build against dav1d, libde265, rav1e from weserv repo

* Sat Dec 19 2020 Leigh Scott <leigh123linux@gmail.com> - 1.10.0-1
- Update to 1.10.0

* Mon Dec 14 2020 Leigh Scott <leigh123linux@gmail.com> - 1.9.1-3
- Actually do the dav1d rebuild

* Mon Dec 14 2020 Robert-André Mauchin <zebob.m@gmail.com> - 1.9.1-2
- Rebuild for dav1d SONAME bump

* Tue Oct 27 2020 Leigh Scott <leigh123linux@gmail.com> - 1.9.1-1
- Update to 1.9.1

* Fri Aug 28 2020 Leigh Scott <leigh123linux@gmail.com> - 1.8.0-1
- Update to 1.8.0

* Tue Aug 18 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 08 2020 Leigh Scott <leigh123linux@gmail.com> - 1.7.0-2
- Rebuilt

* Thu Jun 04 2020 Leigh Scott <leigh123linux@gmail.com> - 1.7.0-1
- Update to 1.7.0

* Sun May 31 2020 Leigh Scott <leigh123linux@gmail.com> - 1.6.2-3
- Rebuild for new x265 version

* Sun Feb 23 2020 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.6.2-2
- Rebuild for x265

* Mon Feb 10 2020 Leigh Scott <leigh123linux@gmail.com> - 1.6.2-1
- Update to 1.6.2

* Tue Feb 04 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 28 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.6.0-1
- Update to 1.6.0
- Rebuilt for x265

* Sun Nov 03 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.5.1-1
- Update to 1.5.1

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 02 2019 Nicolas Chauvet <kwizart@gmail.com> - 1.4.0-3
- Rebuilt for x265

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Feb 28 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-1
- Update to 1.4.0

* Thu Jan 03 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.3.2-2
- Rebuild for new x265 for el7

* Thu Nov 29 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.3.2-1
- First build
