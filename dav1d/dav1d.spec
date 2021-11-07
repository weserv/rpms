Name:           dav1d
Version:        0.9.1
Release:        1%{?dist}
Summary:        AV1 cross-platform Decoder

License:        BSD
URL:            https://code.videolan.org/videolan/dav1d
Source0:        %{url}/-/archive/%{version}/%{name}-%{version}.tar.bz2

BuildRequires:  gcc
BuildRequires:  nasm >= 2.14.0
BuildRequires:  doxygen
BuildRequires:  graphviz
BuildRequires:  meson >= 0.47.0

Requires:       libdav1d%{?_isa} = %{version}-%{release}

%description
dav1d is a new AV1 cross-platform Decoder, open-source, and focused on speed
and correctness.

%package -n libdav1d
Summary:        Library files for dav1d

%description -n libdav1d
Library files for dav1d, the AV1 cross-platform Decoder.

%package -n libdav1d-devel
Summary:        Development files for dav1d
Requires:       libdav1d%{?_isa} = %{version}-%{release}

%description -n libdav1d-devel
Development files for dav1d, the AV1 cross-platform Decoder.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
%meson -Dxxhash_muxer=disabled
%meson_build
%ninja_build -C %{_vpath_builddir} doc/html

%install
%meson_install

%check
%meson_test

%files
%doc CONTRIBUTING.md NEWS README.md
%{_bindir}/dav1d

%files -n libdav1d
%license COPYING doc/PATENTS
%{_libdir}/libdav1d.so.5*

%files -n libdav1d-devel
%doc %{_host_alias}/doc/html
%{_includedir}/dav1d/
%{_libdir}/libdav1d.so
%{_libdir}/pkgconfig/dav1d.pc

%changelog
* Sun Aug  1 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 0.9.1-1
- Update to 0.9.1

* Mon May 17 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 0.9.0-1
- Update to 0.9.0

* Sat Feb 27 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 0.8.2-1
- Disable optional xxh3 based muxer
- Update to 0.8.2

* Sun Jan  3 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 0.8.1-1
- Update to 0.8.1

* Fri Jan  1 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 0.8.0-2
- Import from Fedora
- Build with nasm from weserv repo

* Sat Dec 05 2020 Robert-André Mauchin <zebob.m@gmail.com> - 0.8.0-1
- Update to 0.8.0
- Close: rhbz#1849403

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 30 2020 Robert-André Mauchin <zebob.m@gmail.com> - 0.7.1-1
- Update to 0.7.1 (#1849403)

* Fri May 22 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.7.0-1
- Update to 0.7.0

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Dec 05 2019 Robert-André Mauchin <zebob.m@gmail.com> - 0.5.2-1
- Release 0.5.2 (#1779827)

* Tue Nov 19 2019 Robert-André Mauchin <zebob.m@gmail.com> - 0.5.1-1
- Release 0.5.1 (#1765775, #1771993)

* Fri Oct 11 2019 Robert-André Mauchin <zebob.m@gmail.com> - 0.5.0-1
- Release 0.5.0 (#1760765)

* Fri Aug 09 2019 Robert-André Mauchin <zebob.m@gmail.com> - 0.4.0-1
- Release 0.4.0 (#1708919)

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Apr 29 2019 Robert-André Mauchin <zebob.m@gmail.com> - 0.3.0-1
- Release 0.3.0 (#1701494)

* Sun Apr 21 2019 Robert-André Mauchin <zebob.m@gmail.com> - 0.2.2-1
- Release 0.2.2 (#1701494)

* Tue Apr 16 2019 Adam Williamson <awilliam@redhat.com> - 0.2.1-3
- Rebuild with Meson fix for #1699099

* Tue Mar 26 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.2.1-2
- Rebuild with -Db_ndebug=true

* Tue Mar 12 2019 Robert-André Mauchin - 0.2.1-1
- Release 0.2.1

* Tue Mar 05 2019 Robert-André Mauchin - 0.2.0-1
- Release 0.2.0

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Dec 11 2018 Robert-André Mauchin <zebob.m@gmail.com> - 0.1.0-1
- Initial build
