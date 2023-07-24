# remirepo spec file for vips, from:
#
# Fedora spec file for vips
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
%global vips_version_base 8.14
%global vips_version %{vips_version_base}.3
%global vips_soname_major 42
#global vips_prever rc1
%global vips_tagver %{vips_version}%{?vips_prever:-%{vips_prever}}

%if 0%{?fedora} || 0%{?rhel} >= 8
%bcond_without             doc
%else
%bcond_with                doc
%endif

%if 0%{?fedora} || 0%{?rhel} >= 8
%bcond_without             libimagequant
%bcond_without             libcgif
%bcond_without             libspng
%else
%bcond_with                libimagequant
%bcond_with                libcgif
%bcond_with                libspng
%endif

%if 0%{?fedora} >= 34 || 0%{?rhel} >= 9
%bcond_without             openjpeg2
%else
# disabled by default
# as vips pulls poppler (libopenjpeg) and IM (libopenjp2)
# so vips segfaults in various place
# also see https://github.com/libvips/libvips/pull/2305
%bcond_with                openjpeg2
%endif

# 2 builds needed to get the full stack
# --without im6 --with im7
# --without im6 --with gm

%bcond_without             im6
%bcond_with                im7
%bcond_with                gm
%bcond_without             heif

%bcond_without             tests

%if 0%{?fedora} >= 34 || 0%{?rhel} >= 9
%bcond_without             jxl
%else
%bcond_with                jxl
%endif

Name:           vips
Epoch:          1
Version:        %{vips_version}%{?vips_prever:~%{vips_prever}}
Release:        1%{?dist}
Summary:        C/C++ library for processing large images

License:        LGPLv2+
URL:            https://github.com/libvips/libvips
Source0:        %{url}/releases/download/v%{vips_tagver}/vips-%{vips_version}.tar.xz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  meson >= 0.55
BuildRequires:  gettext
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(expat)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(orc-0.4)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(pangoft2)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(libtiff-4)
# Ensure we use libwebp7 on EL-7
# upstream requires 0.6
BuildRequires:  pkgconfig(libwebp) > 1
BuildRequires:  pkgconfig(libexif)
BuildRequires:  pkgconfig(libgsf-1)
BuildRequires:  pkgconfig(librsvg-2.0) >= 2.50.0
BuildRequires:  pkgconfig(libjpeg) > 1.5.3
%if %{with libspng}
BuildRequires:  pkgconfig(spng) >= 0.7
%else
BuildRequires:  pkgconfig(libpng) >= 1.2.9
%endif
%if %{with openjpeg2}
BuildRequires:  pkgconfig(libopenjp2) >= 2.4
%endif
%if %{with libimagequant}
BuildRequires:  pkgconfig(imagequant) >= 2.11.10
%endif
%if %{with libcgif}
BuildRequires:  pkgconfig(cgif)
%endif
%if %{with tests}
# bc command used in test suite
BuildRequires:  bc
%endif

# Not available as system library
Provides:       bundled(libnsgif)

%if 0%{?fedora} >= 27 || 0%{?rhel} >= 8
Suggests:   %{name}-openslide
Suggests:   %{name}-magick-im6
Recommends: %{name}-heif
Recommends: %{name}-poppler
%else
Requires:   %{name}-poppler
%endif


%description
VIPS is an image processing library. It is good for very large images
(even larger than the amount of RAM in your machine), and for working
with color.

This package should be installed if you want to use a program compiled
against VIPS.

Additional image formats are supported in additional optional packages:
%if %{with jxl}
* %{name}-jxl
%endif
* %{name}-heif
* %{name}-openslide
* %{name}-poppler
* %{name}-magick-im6 using ImageMagick version 6
* %{name}-magick-im7 using ImageMagick version 7
* %{name}-magick-gm  using GraphicsMagick



%package devel
Summary:    Development files for %{name}
Requires:   %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description devel
The %{name}-devel package contains the header files and
libraries necessary for developing programs using VIPS. It also
contains a C++ API and development documentation.


%package tools
Summary:    Command-line tools for %{name}
Requires:   %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description tools
The %{name}-tools package contains command-line tools for working with VIPS.


%if %{with doc}
%package doc
Summary:       Documentation for %{name}
BuildRequires: gtk-doc
BuildRequires: doxygen
Conflicts:     %{name} < %{epoch}:%{version}-%{release}, %{name} > %{epoch}:%{version}-%{release}

%description doc
The %{name}-doc package contains extensive documentation about VIPS in both
HTML and PDF formats.
%endif

%if %{with jxl}
%package jxl
Summary:       JPEG-XL support for %{name}
BuildRequires: pkgconfig(libjxl) >= 0.6
Requires:      %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Supplements:   %{name}

%description jxl
The %{name}-jxl package contains the Jxl module for VIPS.
%endif

%if %{with heif}
%package heif
Summary:       Heif support for %{name}
BuildRequires: pkgconfig(libheif) >= 1.4.0
Requires:      %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description heif
The %{name}-heif package contains the Heif module for VIPS.
%endif

%package openslide
Summary:       OpenSlide support for %{name}
BuildRequires: pkgconfig(openslide) >= 3.3.0
Requires:      %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description openslide
The %{name}-openslide package contains the OpenSlide module for VIPS.

%package poppler
Summary:       Poppler support for %{name}
BuildRequires: pkgconfig(poppler-glib)
Requires:      %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description poppler
The %{name}-poppler package contains the Poppler module for VIPS.

%if %{with im6}
%package magick-im6
Summary:       Magick support for %{name} using ImageMagick6
BuildRequires: ImageMagick6-devel
Requires:      %{name}%{?_isa} = %{epoch}:%{version}-%{release}
%if 0%{?fedora} >= 34
Obsoletes:     %{name}-magick         < %{epoch}:%{version}-%{release}
%endif
Provides:      %{name}-magick         = %{epoch}:%{version}-%{release}
Provides:      %{name}-magick%{?_isa} = %{epoch}:%{version}-%{release}
Conflicts:     %{name}-magick-im7
Conflicts:     %{name}-magick-gm

%description magick-im6
The %{name}-magick-im6 package contains the Magick module for VIPS
using ImageMagick version 6.
%endif

%if %{with im7}
%package magick-im7
Summary:       Magick support for %{name} using ImageMagick7
BuildRequires: ImageMagick7-devel
Requires:      %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Provides:      %{name}-magick         = %{epoch}:%{version}-%{release}
Provides:      %{name}-magick%{?_isa} = %{epoch}:%{version}-%{release}
Conflicts:     %{name}-magick-im6
Conflicts:     %{name}-magick-gm

%description magick-im7
The %{name}-magick-im7 package contains the Magick module for VIPS
using ImageMagick version 7.
%endif

%if %{with gm}
%package magick-gm
Summary:       Magick support for %{name} using GraphicsMagick
BuildRequires: GraphicsMagick-devel
Requires:      %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Provides:      %{name}-magick         = %{epoch}:%{version}-%{release}
Provides:      %{name}-magick%{?_isa} = %{epoch}:%{version}-%{release}
Conflicts:     %{name}-magick-im6
Conflicts:     %{name}-magick-im7

%description magick-gm
The %{name}-magick-gm contains the Magick module for VIPS
using GraphicsMagick.
%endif


%prep
%if %{with gm}
%if %{with im7}
: Cannot enable GraphicsMagick and ImageMagick7
exit 1
%endif
%if %{with im6}
: Cannot enable GraphicsMagick and ImageMagick6
exit 1
%endif
%endif

%setup -q -n vips-%{vips_version}

%build
# Upstream recommends enabling auto-vectorization of inner loops:
# https://github.com/libvips/libvips/pull/212#issuecomment-68177930
export CFLAGS="%{optflags} -ftree-vectorize"
export CXXFLAGS="%{optflags} -ftree-vectorize"
%meson \
%if %{without jxl}
    -Djpeg-xl=disabled \
%endif
%if %{without heif}
    -Dheif=disabled \
%endif
%if %{without libimagequant}
    -Dimagequant=disabled \
%endif
%if %{without libcgif}
    -Dcgif=disabled \
%endif
%if %{without openjpeg2}
    -Dopenjpeg=disabled \
%endif
%if %{without libspng}
    -Dspng=disabled \
%endif
%if %{with doc}
    -Ddoxygen=true \
    -Dgtk_doc=true \
%endif
%if %{with gm}
    -Dmagick-package=GraphicsMagick \
%endif
    -Dmagick-features=load \
    -Dcfitsio=disabled \
    -Dfftw=disabled \
    -Dmatio=disabled \
    -Dnifti=disabled \
    -Dopenexr=disabled \
    -Dpdfium=disabled \
    -Dquantizr=disabled \
    %{nil}

%meson_build

%install
%meson_install

# locale stuff
%find_lang vips%{vips_version_base}

%if %{with tests}
%check
%meson_test
%endif

%files -f vips%{vips_version_base}.lang
%doc ChangeLog README.md
%license LICENSE
%{_libdir}/*.so.%{vips_soname_major}*
%{_libdir}/girepository-1.0
%dir %{_libdir}/vips-modules-%{vips_version_base}


%files devel
%{_includedir}/vips
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_datadir}/gir-1.0


%files tools
%{_bindir}/*
%{_mandir}/man1/*


%if %{with doc}
%files doc
%{_datadir}/gtk-doc
%{_docdir}/vips-doc/html
%license LICENSE
%endif


%files openslide
%{_libdir}/vips-modules-%{vips_version_base}/vips-openslide.so

%files poppler
%{_libdir}/vips-modules-%{vips_version_base}/vips-poppler.so

%if %{with jxl}
%files jxl
%{_libdir}/vips-modules-%{vips_version_base}/vips-jxl.so
%endif

%if %{with heif}
%files heif
%{_libdir}/vips-modules-%{vips_version_base}/vips-heif.so
%endif

%if %{with im6}
%files magick-im6
%{_libdir}/vips-modules-%{vips_version_base}/vips-magick.so
%endif

%if %{with im7}
%files magick-im7
%{_libdir}/vips-modules-%{vips_version_base}/vips-magick.so
%endif

%if %{with gm}
%files magick-gm
%{_libdir}/vips-modules-%{vips_version_base}/vips-magick.so
%endif


%changelog
* Mon Jul 24 2023 Kleis Auke Wolthuizen <info@kleisauke.nl> - 8.14.3-1
- Update to 8.14.3

* Tue Apr 11 2023 Kleis Auke Wolthuizen <info@kleisauke.nl> - 8.14.2-1
- Bump epoch

* Tue Mar 21 2023 Kleis Auke Wolthuizen <info@kleisauke.nl> - 8.14.2-1
- Update to 8.14.2

* Mon Jan  9 2023 Kleis Auke Wolthuizen <info@kleisauke.nl> - 8.14.1-1
- Update to 8.14.1

* Wed Dec 28 2022 Kleis Auke Wolthuizen <info@kleisauke.nl> - 8.14.0~rc1-1
- Update to 8.14.0-rc1

* Sun Nov 20 2022 Kleis Auke Wolthuizen <info@kleisauke.nl> - 8.13.3-1
- Update to 8.13.3
- Enable libjxl usage

* Tue Oct  4 2022 Kleis Auke Wolthuizen <info@kleisauke.nl> - 8.13.2-1
- Update to 8.13.2

* Tue Jul 26 2022 Kleis Auke Wolthuizen <info@kleisauke.nl> - 8.13.0-1
- Update to 8.13.0

* Sat Jul 16 2022 Kleis Auke Wolthuizen <info@kleisauke.nl> - 8.13.0~rc2-1
- Update to 8.13.0-rc2

* Sun Jun 19 2022 Kleis Auke Wolthuizen <info@kleisauke.nl> - 8.13.0~rc1-1
- Update to 8.13.0-rc1
- Migrate build to Meson
- Enable openjpeg2 usage on RHEL >= 9
- Increase minimum required version of libspng to 0.7 for PNG write support
- Remove libpng in favor of libspng (if possible)
- Remove gtk-doc docs from vips-devel

* Wed Jan 26 2022 Kleis Auke Wolthuizen <info@kleisauke.nl> - 8.12.2-1
- Update to 8.12.2

* Sun Dec 12 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 8.12.1-1
- Update to 8.12.1

* Sun Nov 21 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 8.12.0-1
- Update to 8.12.0
- Enable libcgif usage
- Build against libjpeg-turbo-official
- Sync with remirepo
- Suggests vips-openslide/vips-magick-im6 package instead of recommends
- Recommend vips-heif package
- Remove vips-full obsoletes
- Remove redundant devel requires
- Remove redundant ldconfig post and postun

* Sun Nov 14 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 8.12.0~rc1-1
- Update to 8.12.0-rc1

* Mon Nov  8 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 8.12.0-1.20211107git296fd99
- Test libvips 8.12 with cgif

* Mon Jul  5 2021 Remi Collet <remi@remirepo.net> - 8.11.2-2
- rebuild with latest changes from Fedora

* Mon Jul 05 2021 Benjamin Gilbert <bgilbert@backtick.net> - 8.11.2-2
- Add doxygen C++ docs to vips-devel
- Use arch-specific Requires in plugin subpackages
- Provide bundled(libnsgif)
- Drop some redundant version restrictions

* Sun Jul  4 2021 Remi Collet <remi@remirepo.net> - 8.11.2-1
- update to 8.11.2
- drop patch merged (and improved) upstream

* Tue Jun 15 2021 Remi Collet <remi@remirepo.net> - 8.11.1-1
- update to 8.11.1

* Tue Jun 15 2021 Remi Collet <remi@remirepo.net> - 8.11.0-1.2
- test build for fix for bad prefix guess from
  https://github.com/libvips/libvips/pull/2308
- only use openjpeg2 >= 2.4 (Fedora >= 34)

* Thu Jun 10 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 8.11.0-1
- Update to 8.11.0

* Sat Jun  5 2021 Remi Collet <remi@remirepo.net> - 8.11.0~rc1-1
- update to 8.11.0rc1
- split modules in sub-packages

* Sat Mar 27 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 8.10.6-1
- Update to 8.10.6

* Sat Feb 27 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 8.10.5-4
- Build against ImageMagick6 and new soname from remirepo

* Sun Jan  3 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 8.10.5-3
- Ensure package does not provide disabled dependencies
- Remove duplicated dependency on libspng
- Requires pkgconfig(imagequant) instead of libimagequant-devel
- Remove dependency on deprecated gthread-2.0

* Fri Jan  1 2021 Kleis Auke Wolthuizen <info@kleisauke.nl> - 8.10.5-2
- Import from remirepo
- Disable fftw3, OpenEXR, matio, cfitsio, openslide
- Build against libspng, libheif, librsvg from weserv repo
- Enable libheif and libspng usage by default

* Sun Dec 20 2020 Remi Collet <remi@remirepo.net> - 8.10.5-1
- update to 8.10.5

* Mon Dec 14 2020 Remi Collet <remi@remirepo.net> - 8.10.4-3
- enable libspng usage on Fedora

* Mon Dec 14 2020 Remi Collet <remi@remirepo.net> - 8.10.4-1
- update to 8.10.4

* Sun Dec 13 2020 Remi Collet <remi@remirepo.net> - 8.10.3-1
- update to 8.10.3

* Tue Oct 13 2020 Remi Collet <remi@remirepo.net> - 8.10.2-1
- update to 8.10.2

* Fri Sep  4 2020 Remi Collet <remi@remirepo.net> - 8.10.1-1
- update to 8.10.1

* Wed Aug 19 2020 Remi Collet <remi@remirepo.net> - 8.10.0-2
- rebuild for matio 1.5.17 in EPEL-7

* Mon Aug 10 2020 Remi Collet <remi@remirepo.net> - 8.10.0-1
- update to 8.10.0

* Thu Jul 16 2020 Remi Collet <remi@remirepo.net> - 8.10.0~rc1-1
- update to 8.10.0-rc1

* Tue Apr 21 2020 Remi Collet <remi@remirepo.net> - 8.9.2-1
- update to 8.9.2

* Tue Apr 21 2020 Remi Collet <remi@remirepo.net> - 8.9.1-3
- build against ImageMagick on EL-7

* Tue Jan 28 2020 Remi Collet <remi@remirepo.net> - 8.9.1-1
- update to 8.9.1
- ensure vips-devel pull right ImageMagick-devel version
  https://github.com/remicollet/remirepo/issues/134

* Wed Jan  8 2020 Remi Collet <remi@remirepo.net> - 8.9.0-1
- update to 8.9.0

* Fri Jan  3 2020 Remi Collet <remi@remirepo.net> - 8.9.0~rc4-1
- update to 8.9.0-rc4
- open https://github.com/libvips/libvips/issues/1513
  ABI compatibility with 8.8.0

* Fri Dec  6 2019 Remi Collet <remi@remirepo.net> - 8.8.4-1
- update to 8.8.4

* Tue Oct  1 2019 Remi Collet <remi@remirepo.net> - 8.8.3-3
- rebuild with matio / hdf5 fom EPEL

* Tue Sep 17 2019 Remi Collet <remi@remirepo.net> - 8.8.3-1
- update to 8.8.3

* Fri Aug 30 2019 Remi Collet <remi@remirepo.net> - 8.8.2-1
- update to 8.8.2

* Mon Jul  8 2019 Remi Collet <remi@remirepo.net> - 8.8.1-1
- update to 8.8.1

* Wed May 22 2019 Remi Collet <remi@remirepo.net> - 8.8.0-1
- update to 8.8.0

* Thu May 16 2019 Remi Collet <remi@remirepo.net> - 8.8.0~rc3-1
- update to 8.8.0-rc3

* Thu May  9 2019 Remi Collet <remi@remirepo.net> - 8.8.0~rc2-1
- update to 8.8.0-rc2

* Mon May  6 2019 Remi Collet <remi@remirepo.net> - 8.8.0~rc1-1
- update to 8.8.0-rc1
- drop libvipsCC
- drop python support

* Mon Mar 18 2019 Remi Collet <remi@remirepo.net> - 8.7.4-2
- rebuild using libwebp7

* Fri Jan 18 2019 Remi Collet <remi@remirepo.net> - 8.7.4-1
- update to 8.7.4

* Fri Jan  4 2019 Remi Collet <remi@remirepo.net> - 8.7.3-1
- update to 8.7.3

* Wed Dec 19 2018 Remi Collet <remi@remirepo.net> - 8.7.2-1
- update to 8.7.2
- rename vips-python to python2-vips
- rename vips-python3 to python3-vips
- drop python2 on F30 and EL8

* Tue Dec 18 2018 Remi Collet <remi@remirepo.net> - 8.7.0-3
- fix URL and sources (from jcupitt to libvips)
- requires pkgconfig(libjpeg) instead of libjpeg-turbo-devel

* Tue Dec  4 2018 Remi Collet <remi@remirepo.net> - 8.7.0-2
- EL-8 build

* Thu Sep 20 2018 Remi Collet <remi@remirepo.net> - 8.7.0-1
- update to 8.7.0

* Thu Aug 30 2018 Remi Collet <remi@remirepo.net> - 8.7.0~rc3-1
- update to 8.7.0~rc3

* Mon Aug 27 2018 Remi Collet <remi@remirepo.net> - 8.7.0~rc2-1
- update to 8.7.0~rc2

* Thu Jul 26 2018 Remi Collet <remi@remirepo.net> - 8.6.5-1
- update to 8.6.5

* Thu Jun 14 2018 Remi Collet <remi@remirepo.net> - 8.6.4-1
- Update to 8.6.4

* Wed Jun 13 2018 Remi Collet <remi@remirepo.net> - 8.6.3-3
- rebuild against ImageMagick6 (6.9.10-0)

* Tue May 29 2018 Remi Collet <remi@remirepo.net> - 8.6.3-2
- rebuild against ImageMagick6 new soname (6.9.9-47)

* Fri Mar  9 2018 Remi Collet <remi@remirepo.net> - 8.6.3-1
- Update to 8.6.3

* Thu Feb  1 2018 Remi Collet <remi@remirepo.net> - 8.6.2-1
- Update to 8.6.2

* Fri Jan 12 2018 Remi Collet <remi@remirepo.net> - 8.6.1-1
- Update to 8.6.1
- open https://github.com/jcupitt/libvips/issues/854

* Fri Dec  8 2017 Remi Collet <remi@remirepo.net> - 8.6.0-1
- Update to 8.6.0

* Wed Oct 11 2017 Remi Collet <remi@remirepo.net> - 8.5.9-1
- Update to 8.5.9

* Mon Oct  2 2017 Remi Collet <remi@remirepo.net> - 8.6.0~alpha5-1
- update to 8.6.0-alpha5

* Mon Sep 11 2017 Remi Collet <remi@remirepo.net> - 8.6.0~alpha4-1
- update to 8.6.0-alpha4

* Fri Sep  8 2017 Remi Collet <remi@remirepo.net> - 8.6.0~alpha3-1
- update to 8.6.0-alpha3

* Thu Sep  7 2017 Remi Collet <remi@remirepo.net> - 8.6.0~alpha2-1
- update to 8.6.0-alpha2

* Wed Sep  6 2017 Remi Collet <remi@remirepo.net> - 8.5.8-4
- rebuild using ImageMagick on F27+

* Fri Aug 25 2017 Remi Collet <remi@remirepo.net> - 8.5.8-3
- rebuild using ImageMagick on F25+

* Tue Aug 22 2017 Remi Collet <remi@remirepo.net> - 8.5.8-2
- F27 rebuild

* Tue Aug 22 2017 Remi Collet <remi@remirepo.net> - 8.5.8-1
- Update to 8.5.8

* Sat Aug  5 2017 Remi Collet <remi@remirepo.net> - 8.5.7-2
- rebuild against ImageMagick6 new soname (6.9.9-5)

* Wed Aug  2 2017 Remi Collet <remi@remirepo.net> - 8.5.7-1
- Update to 8.5.7

* Thu Jun  8 2017 Remi Collet <remi@remirepo.net> - 8.5.6-1
- Update to 8.5.6

* Mon May 15 2017 Remi Collet <remi@remirepo.net> - 8.5.5-1
- Update to 8.5.5

* Sun Apr 23 2017 Remi Collet <remi@remirepo.net> - 8.5.4-1
- Update to 8.5.4

* Fri Apr 21 2017 Remi Collet <remi@remirepo.net> - 8.5.3-1
- update to 8.5.3

* Mon Apr 10 2017 Remi Collet <remi@remirepo.net> - 8.5.2-1
- update to 8.5.2
- new site http://jcupitt.github.io/libvips/
- drop dependency on libxml2
- add dependency on expat

* Sun Jan 29 2017 Remi Collet <remi@remirepo.net> - 8.4.4-4
- rebuild against ImageMagick6 new soname (6.9.7-6)

* Mon Dec 12 2016 Remi Collet <remi@remirepo.net> - 8.4.4-3
- rebuild against ImageMagick6

* Tue Dec  6 2016 Remi Collet <remi@remirepo.net> - 8.4.4-2
- ensure ImageMagick v6 is used

* Thu Nov 24 2016 Remi Collet <remi@remirepo.net> - 8.4.4-1
- backport for repo repository
- disable python3 and doc sub-package

* Sun Nov 13 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.4.4-1
- New release

* Thu Oct 13 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.4.2-1
- New release

* Sun Sep 25 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.4.1-1
- New release

* Sat Aug 06 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.3.3-1
- New release

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.3.1-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Jul 05 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.3.1-2
- Rebuilt for matio 1.5.7

* Tue May 10 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.3.1-1
- New release
- Verify that wrapper script name matches base version

* Thu Apr 14 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.3.0-1
- New release
- Add giflib, librsvg2, poppler-glib dependencies

* Mon Mar 28 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.2.3-1
- New release

* Sun Feb 21 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.2.2-3
- BuildRequire gcc-c++ per new policy

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 8.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 26 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.2.2-1
- New release

* Thu Jan 21 2016 Orion Poplawski <orion@cora.nwra.com> - 8.2.1-2
- Rebuild for hdf5 1.8.16

* Mon Jan 11 2016 Benjamin Gilbert <bgilbert@backtick.net> - 8.2.1-1
- New release

* Mon Dec 28 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 8.1.1-3
- Rebuilt for libwebp soname bump

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Sun Oct 18 2015 Benjamin Gilbert <bgilbert@backtick.net> - 8.1.1-1
- New release
- Update to new Python guidelines

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May 17 2015 Orion Poplawski <orion@cora.nwra.com> - 8.0.2-2
- Rebuild for hdf5 1.8.15

* Wed May 06 2015 Benjamin Gilbert <bgilbert@backtick.net> - 8.0.2-1
- New release

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 7.42.3-2
- Rebuilt for GCC 5 C++11 ABI change

* Sat Feb 14 2015 Benjamin Gilbert <bgilbert@backtick.net> - 7.42.3-1
- New release

* Thu Feb 05 2015 Benjamin Gilbert <bgilbert@backtick.net> - 7.42.2-1
- New release
- Move license files to %%license

* Wed Jan 07 2015 Orion Poplawski <orion@cora.nwra.com> - 7.42.1-2
- Rebuild for hdf5 1.8.14

* Sun Dec 28 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.42.1-1
- New release
- Package new Python bindings
- Build with auto-vectorization

* Tue Nov 25 2014 Rex Dieter <rdieter@fedoraproject.org> 7.40.11-2
- rebuild (openexr)

* Wed Nov 05 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.40.11-1
- New release

* Thu Sep 25 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.40.9-1
- New release

* Fri Aug 22 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.40.6-1
- New release

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.40.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 12 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.40.5-1
- New release

* Sat Jul 26 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.40.4-1
- New release

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 7.40.3-2
- Rebuilt for gobject-introspection 1.41.4

* Tue Jul 08 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.40.3-1
- New release

* Sun Jun 29 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.40.2-1
- New release
- Add libgsf dependency
- Fix version string consistency across architectures
- Use macros for package and soname versions

* Sun Jun 22 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.38.6-1
- New release

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.38.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 31 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.38.5-2
- Rebuild for ImageMagick

* Wed Mar 26 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.38.5-1
- New release

* Tue Jan 21 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.38.1-1
- New release

* Thu Jan 09 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.36.5-3
- Rebuild for cfitsio

* Thu Jan 02 2014 Benjamin Gilbert <bgilbert@backtick.net> - 7.36.5-2
- Rebuild for libwebp

* Mon Dec 23 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.36.5-1
- New release

* Thu Nov 28 2013 Rex Dieter <rdieter@fedoraproject.org> 7.36.3-2
- rebuild (openexr)

* Wed Nov 13 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.36.3-1
- New release
- BuildRequire libwebp

* Sat Oct 05 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.36.0-1
- New release

* Tue Sep 10 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.34.2-2
- Rebuild for ilmbase 2.0

* Tue Aug 06 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.34.2-1
- New release
- Update -devel description: there are no man pages anymore

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.34.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 11 2013 Orion Poplawski <orion@cora.nwra.com> - 7.34.0-2
- Rebuild for cfitsio 3.350

* Sat Jun 29 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.34.0-1
- New release

* Fri Jun 28 2013 Kalev Lember <kalevlember@gmail.com> - 7.32.4-2
- Rebuilt with libpng 1.6

* Thu Jun 13 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.32.4-1
- New release

* Thu May 16 2013 Orion Poplawski <orion@cora.nwra.com> - 7.32.3-2
- Rebuild for hdf5 1.8.11

* Fri Apr 26 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.32.3-1
- New release

* Thu Mar 21 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.32.1-1
- New release

* Thu Mar 21 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.32.0-4
- Rebuild for cfitsio

* Sun Mar 17 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.32.0-3
- Rebuild for ImageMagick

* Sun Mar 10 2013 Rex Dieter <rdieter@fedoraproject.org> 7.32.0-2
- rebuild (OpenEXR)

* Thu Mar 07 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.32.0-1
- New release
- Stop setting rpath on 64-bit builds

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.30.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 7.30.7-2
- rebuild due to "jpeg8-ABI" feature drop

* Thu Jan 17 2013 Benjamin Gilbert <bgilbert@backtick.net> - 7.30.7-1
- New release
- Modify %%files glob to catch accidental soname bumps
- Update BuildRequires

* Wed Nov 14 2012 Benjamin Gilbert <bgilbert@backtick.net> - 7.30.5-1
- New release

* Mon Oct 15 2012 Benjamin Gilbert <bgilbert@backtick.net> - 7.30.3-1
- New release
- Enable gobject introspection
- Add versioned dependency on base package
- Minor specfile cleanups

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.28.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 07 2012 Adam Jackson <ajax@redhat.com> 7.28.2-2
- Rebuild for new libmatio

* Fri Apr 13 2012 Adam Goode <adam@spicenitz.org> - 7.28.2-1
- New upstream release
   * libvips rewrite
   * OpenSlide support
   * better jpeg, png, tiff support
   * sequential mode read
   * operation cache

* Mon Jan 16 2012 Adam Goode <adam@spicenitz.org> - 7.26.7-1
- New upstream release
   * Minor fixes, mostly with reading and writing

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.26.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 7.26.3-2
- Rebuild for new libpng

* Sat Sep  3 2011 Adam Goode <adam@spicenitz.org> - 7.26.3-1
- New upstream release
   * More permissive operators
   * Better TIFF, JPEG, PNG, FITS support
   * VIPS rewrite!

* Fri Aug 12 2011 Adam Goode <adam@spicenitz.org> - 7.24.7-2
- Clean up Requires and BuildRequires

* Wed Aug 10 2011 Adam Goode <adam@spicenitz.org> - 7.24.7-1
- New upstream release

* Mon Feb 14 2011 Adam Goode <adam@spicenitz.org> - 7.24.2-1
- New upstream release
   * Run-time code generation, for 4x speedup in some operations
   * Open via disc mode, saving memory
   * FITS supported
   * Improved TIFF and JPEG load

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.22.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Oct 05 2010 jkeating - 7.22.2-1.2
- Rebuilt for gcc bug 634757

* Wed Sep 29 2010 jkeating - 7.22.2-3
- Rebuilt for gcc bug 634757

* Mon Sep 20 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 7.22.2-2
- rebuild against ImageMagick

* Fri Sep 17 2010 Rex Dieter <rdieter@fedoraproject.org> - 7.22.2-1.1
- rebuild (ImageMagick)

* Fri Aug  6 2010 Adam Goode <adam@spicenitz.org> - 7.22.2-1
- New upstream release (a few minor fixes)

* Tue Jul 27 2010 Adam Goode <adam@spicenitz.org> - 7.22.1-2
- Add COPYING to doc subpackage

* Tue Jul 27 2010 Adam Goode <adam@spicenitz.org> - 7.22.1-1
- New upstream release
   + More revision of VIPS library
   + New threading system
   + New command-line program, vipsthumbnail
   + Improved interpolators
   + German translation
   + PFM (portable float map) image format read and write
   + Much lower VM use with many small images open
   + Rewritten flood-fill

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 7.20.7-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jun 15 2010 Adam Goode <adam@spicenitz.org> - 7.20.7-3
- Don't require gtk-doc anymore (resolves #604421)

* Sun Mar  7 2010 Adam Goode <adam@spicenitz.org> - 7.20.7-2
- Rebuild for imagemagick soname change
- Remove some old RPM stuff

* Tue Feb  2 2010 Adam Goode <adam@spicenitz.org> - 7.20.7-1
- New upstream release
   + C++ and Python bindings now have support for deprecated functions
   + Bugfixes for YCbCr JPEG TIFF files

* Wed Jan  6 2010 Adam Goode <adam@spicenitz.org> - 7.20.6-1
- New upstream release
   + About half of the VIPS library has been revised
   + Now using gtk-doc
   + Better image file support
   + MATLAB file read supported
   + New interpolation system
   + Support for Radiance files

* Fri Sep  4 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 7.18.2-1
- Update to 7.18.2 to sync with fixed nip2 FTBFS.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.16.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 10 2009 Adam Goode <adam@spicenitz.org> - 7.16.4-3
- Rebuild for ImageMagick soname change

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.16.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Dec 28 2008 Adam Goode <adam@spicenitz.org> - 7.16.4-1
- New release

* Sun Dec 21 2008 Adam Goode <adam@spicenitz.org> - 7.16.3-1
- New release
- Update description

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 7.14.5-2
- Rebuild for Python 2.6

* Sat Aug 30 2008 Adam Goode <adam@spicenitz.org> - 7.14.5-1
- New release

* Fri Jun 20 2008 Adam Goode <adam@spicenitz.org> - 7.14.4-1
- New release

* Sat Mar 15 2008 Adam Goode <adam@spicenitz.org> - 7.14.1-1
- New release

* Mon Mar 10 2008 Adam Goode <adam@spicenitz.org> - 7.14.0-1
- New release
- Remove GCC 4.3 patch (upstream)

* Sat Feb  9 2008 Adam Goode <adam@spicenitz.org> - 7.12.5-5
- Fix GCC 4.3 build

* Sat Feb  9 2008 Adam Goode <adam@spicenitz.org> - 7.12.5-4
- GCC 4.3 mass rebuild

* Tue Oct 23 2007 Adam Goode <adam@spicenitz.org> - 7.12.5-3
- Eliminate build differences in version.h to work on multiarch

* Mon Oct 15 2007 Adam Goode <adam@spicenitz.org> - 7.12.5-2
- Rebuild for OpenEXR update

* Fri Sep 21 2007 Adam Goode <adam@spicenitz.org> - 7.12.5-1
- New upstream release

* Thu Aug 16 2007 Adam Goode <adam@spicenitz.org> - 7.12.4-2
- Add Conflicts for doc
- Update doc package description

* Thu Aug 16 2007 Adam Goode <adam@spicenitz.org> - 7.12.4-1
- New upstream release
- Update License tag

* Tue Jul 24 2007 Adam Goode <adam@spicenitz.org> - 7.12.2-1
- New stable release 7.12

* Sat May  5 2007 Adam Goode <adam@spicenitz.org> - 7.12.0-1
- New upstream release

* Thu Aug 31 2006 Adam Goode <adam@spicenitz.org> - 7.10.21-1
- New upstream release

* Fri Jul 28 2006 Adam Goode <adam@spicenitz.org> - 7.10.20-3
- Include results of running automake in the patch for undefined symbols
- No longer run automake or autoconf (autoconf was never actually necessary)

* Mon Jul 24 2006 Adam Goode <adam@spicenitz.org> - 7.10.20-2
- Eliminate undefined non-weak symbols in libvipsCC.so

* Fri Jul 21 2006 Adam Goode <adam@spicenitz.org> - 7.10.20-1
- New upstream release
- Updated for FC5

* Tue Dec 14 2004 John Cupitt <john.cupitt@ng-london.org.uk> 7.10.8
- updated for 7.10.8
- now updated from configure
- implicit deps and files

* Wed Jul 16 2003 John Cupitt <john.cupitt@ng-london.org.uk> 7.8.10
- updated for 7.8.10
- updated %%files
- copies formatted docs to install area

* Wed Mar 12 2003 John Cupitt <john.cupitt@ng-london.org.uk> 7.8.8
- updated for 7.8.8, adding libdrfftw

* Mon Feb 3 2003 John Cupitt <john.cupitt@ng-london.org.uk> 7.8.7-2
- hack to change default install prefix to /usr/local

* Thu Jan 30 2003 John Cupitt <john.cupitt@ng-london.org.uk> 7.8.7-1
- first stab at an rpm package for vips
