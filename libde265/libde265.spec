Name:           libde265
Version:        1.0.14
Release:        1%{?dist}
Summary:        Open H.265 video codec implementation

License:        LGPLv3+
URL:            https://www.libde265.org/
Source0:        https://github.com/strukturag/libde265/releases/download/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc-c++
BuildRequires:  libtool

%description
libde265 is an open source implementation of the H.265 video codec.
It is written from scratch for simplicity and efficiency. Its simple
API makes it easy to integrate it into other software.


%package devel
Summary:    Open H.265 video codec implementation - development files
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description devel
libde265 is an open source implementation of the H.265 video codec.
It is written from scratch for simplicity and efficiency. Its simple
API makes it easy to integrate it into other software.

The development headers for compiling programs that use libde265
are provided by this package.

%package examples
# The entire examples source code is GPLv3+ except extra/getopt* which is BSD.
License:    GPLv3+ and BSD
Summary:    Open H.265 video codec implementation - examples
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description examples
libde265 is an open source implementation of the H.265 video codec.
It is written from scratch for simplicity and efficiency. Its simple
API makes it easy to integrate it into other software.

Sample applications using libde265 are provided by this package.

%prep
%autosetup -p1

%build
%configure \
 --disable-silent-rules \
 --disable-static \
 --disable-dec265 \
 --disable-sherlock265 \
 --enable-shared

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%make_build

%install
%make_install
find %buildroot -name '*.la' -or -name '*.a' | xargs rm -f
# Don't package internal development tools.
rm -f %{buildroot}%{_bindir}/bjoentegaard
rm -f %{buildroot}%{_bindir}/block-rate-estim
rm -f %{buildroot}%{_bindir}/gen-enc-table
rm -f %{buildroot}%{_bindir}/hdrcopy
rm -f %{buildroot}%{_bindir}/rd-curves
rm -f %{buildroot}%{_bindir}/tests
rm -f %{buildroot}%{_bindir}/yuv-distortion

%ldconfig_scriptlets

%files
%doc AUTHORS
%license COPYING
%{_libdir}/*.so.*

%files devel
%doc README.md
%{_includedir}/libde265/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc


%files examples
%doc README.md
%{_bindir}/acceleration_speed

%changelog
* Sat Dec  2 2023 Kleis Auke Wolthuizen <info@kleisauke.nl> - 1.0.14-1
- Update to 1.0.14

* Mon Jun 26 2023 Kleis Auke Wolthuizen <info@kleisauke.nl> - 1.0.12-1
- Update to 1.0.12

* Thu Feb  2 2023 Kleis Auke Wolthuizen <info@kleisauke.nl> - 1.0.11-1
- Update to 1.0.11

* Sun Nov 20 2022 Kleis Auke Wolthuizen <info@kleisauke.nl> - 1.0.9-1
- Update to 1.0.9

* Fri Jan  1 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 1.0.8-2
- Import from rpmfusion
- Drop libswscale, Qt5, sdl dependencies

* Fri Nov  6 2020 Leigh Scott <leigh123linux@gmail.com> - 1.0.8-1
- Update to 1.0.8

* Fri Aug 28 2020 Leigh Scott <leigh123linux@gmail.com> - 1.0.6-1
- Update to 1.0.6

* Tue Aug 18 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Mar 12 2020 Leigh Scott <leigh123linux@gmail.com> - 1.0.5-4
- Rebuilt for i686

* Sat Feb 22 2020 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.0.5-3
- Rebuild for ffmpeg-4.3 git

* Fri Jan 24 2020 Nicolas Chauvet <kwizart@gmail.com> - 1.0.5-2
- rebuilt

* Sat Jan 18 2020 Leigh Scott <leigh123linux@googlemail.com> - 1.0.5-1
- Update to 1.0.5

* Sun Dec 22 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.0.4-1
- Update to 1.0.4

* Wed Aug 07 2019 Leigh Scott <leigh123linux@gmail.com> - 1.0.3-5
- Rebuild for new ffmpeg version

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Nov 27 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.0.3-3
- Remove Group tag
- Switch to QT5
- Update ldconfig scriptlet
- Add BuildRequires gcc-c++
- Remove BuildRequires pkgconfig

* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Apr 29 2018 Sérgio Basto <sergio@serjux.com> - 1.0.3-1
- Update to 1.0.3
- Add the new /usr/bin file to examples package

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 17 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.0.2-7
- Rebuilt for ffmpeg-3.5 git

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Apr 29 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.0.2-5
- Rebuild for ffmpeg update

* Sun Mar 19 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Jul 30 2016 Julian Sikorski <belegdol@fedoraproject.org> - 1.0.2-3
- Rebuilt for ffmpeg-3.1.1

* Tue Jul 19 2016 Joachim Bauch <bauch@struktur.de> 1.0.2-2
- Fixed compatibility when compiling against FFmpeg 2.9 and newer.

* Thu Jun 09 2016 Joachim Bauch <bauch@struktur.de> 1.0.2-1
- Initial version.
