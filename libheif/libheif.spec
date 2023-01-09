Name:           libheif
Version:        1.14.2
Release:        1%{?dist}
Summary:        HEIF file format decoder and encoder

License:        LGPLv3+ and MIT
URL:            https://github.com/strukturag/%{name}
Source0:        %{url}/releases/download/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(dav1d)
BuildRequires:  pkgconfig(libde265)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(rav1e)
BuildRequires:  pkgconfig(libpng)

Requires:  shared-mime-info

%description
HEIF is a image format using HEVC image coding for the best compression ratios.
libheif uses libde265 for the actual image decoding and x265 for encoding.
Alternative codecs for, e.g., AVC and JPEG can be provided as plugins.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1
rm -rf third-party/


%build
%cmake -DENABLE_PLUGIN_LOADING=0 \
       -DWITH_RAV1E_PLUGIN=0 \
       -DWITH_X265=0 \
       -DWITH_AOM=0 \
       -DWITH_SvtEnc=0

%cmake_build


%install
%cmake_install
find %buildroot -name '*.la' -or -name '*.a' | xargs rm -f


%ldconfig_scriptlets


%files
%license COPYING
%doc README.md
%{_bindir}/heif-convert
%{_bindir}/heif-enc
%{_bindir}/heif-info
%{_bindir}/heif-thumbnailer
%{_libdir}/*.so.1*
%{_libdir}/gdk-pixbuf-2.0/*/loaders/libpixbufloader-heif.*
%{_datadir}/mime/packages/*.xml
%{_datadir}/thumbnailers/
%{_mandir}/man1/heif-*

%files devel
%{_includedir}/%{name}/
%{_libdir}/cmake/%{name}/
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/*.so


%changelog
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
