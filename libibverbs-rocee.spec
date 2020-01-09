%global __obsolete_version 1.1.8

Name: libibverbs-rocee
Version: 1.1.7
Release: 1.1%{?dist}
Summary: A library for direct userspace use of RDMA (InfiniBand/iWARP) hardware
Group: System Environment/Libraries
License: GPLv2 or BSD
Url: http://openfabrics.org/
Source: http://openfabrics.org/downloads/verbs/libibverbs-%{version}.tar.gz
Patch0: libibverbs-1.1.7-arg-fixes.patch
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Provides: libibverbs = %{version}
Obsoletes: libibverbs < %{__obsolete_version}
BuildRequires: valgrind-devel
ExcludeArch: s390 s390x

%description
libibverbs is a library that allows userspace processes to use RDMA
"verbs" as described in the InfiniBand Architecture Specification and
the RDMA Protocol Verbs Specification.  This includes direct hardware
access from userspace to InfiniBand/iWARP adapters (kernel bypass) for
fast path operations.

For this library to be useful, a device-specific plug-in module should
also be installed.

%package devel
Summary: Development files for the libibverbs library
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
%ifarch i686
Provides: libibverbs-devel(x86-32) = %{version}
%endif
%ifarch ppc
Provides: libibverbs-devel(ppc-32) = %{version}
%endif
%ifarch x86_64
Provides: libibverbs-devel(x86-64) = %{version}
%endif
%ifarch ppc64
Provides: libibverbs-devel(ppc-64) = %{version}
%endif
Provides: libibverbs-devel = %{version}
Obsoletes: libibverbs-devel < %{__obsolete_version}

%description devel
Header files for the libibverbs library.

%package devel-static
Summary: Static development files for the libibverbs library
Group: System Environment/Libraries
Requires: %{name}-devel = %{version}-%{release}
%ifarch x86_64
Provides: libibverbs-devel-static(x86-64) = %{version}
%endif
Provides: libibverbs-devel-static = %{version}
Obsoletes: libibverbs-devel-static < %{__obsolete_version}

%description devel-static
Static libraries for the libibverbs library.

%package utils
Summary: Examples for the libibverbs library
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Provides: libibverbs-utils = %{version}
Obsoletes: libibverbs-utils < %{__obsolete_version}
Requires: libibverbs-driver.%{_arch}

%description utils
Useful libibverbs example programs such as ibv_devinfo, which
displays information about RDMA devices.

%prep
%setup -q -n libibverbs-%{version}
%patch0 -p1 -b .fixes

%build
%configure --with-valgrind
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make CFLAGS="$CFLAGS -fno-strict-aliasing" %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
mkdir -p -m755 %{buildroot}%{_sysconfdir}/libibverbs.d
# remove unpackaged files from the buildroot
rm -f %{buildroot}%{_libdir}/*.la

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%dir %{_sysconfdir}/libibverbs.d
%{_libdir}/libibverbs*.so.*
%doc AUTHORS COPYING ChangeLog README

%files devel
%defattr(-,root,root,-)
%{_libdir}/lib*.so
%{_includedir}/*
%{_mandir}/man3/*

%files devel-static
%defattr(-,root,root,-)
%{_libdir}/*.a

%files utils
%defattr(-,root,root,-)
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Mon Dec 02 2013 Doug Ledford <dledford@redhat.com> - 1.1.7-1.1
- Fix obsoletes tags so yum updates work again
- Resolves: bz1037759

* Mon Oct 28 2013 Doug Ledford <dledford@redhat.com> - 1.1.7-1
- Update to 1.1.7 to match base product
- Related: bz879191

* Tue Oct 23 2012 Doug Ledford <dledford@redhat.com> - 1.1.6-3
- Don't print link state on iWARP links as it's always invalid
- Don't try to do ud transfers in excess of port MTU
- Resolves: bz822781

* Thu Mar 08 2012 Doug Ledford <dledford@redhat.com> - 1.1.6-2
- Make ibv_devinfo return an error when it can't find the requested port
- Resolves: bz755459

* Mon Jan 23 2012 Doug Ledford <dledford@redhat.com> - 1.1.6-1
- Update to latest upstream version (now includes native rocee support
  and FDR support)
- Related: bz758498, bz750609

* Tue Aug 02 2011 Doug Ledford <dledford@redhat.com> - 1.1.5-3
- Rebuild to fix issue with memcpy on ppc arch in the compat-1.0 layer
- Related: bz727336

* Fri Jul 22 2011 Doug Ledford <dledford@redhat.com> - 1.1.5-1
- Update to latest upstream version (1.1.4 to 1.1.5)
- Drop libibverbs cow.patch as it is in 1.1.5 already
- Drop ifnarch ia64 from valgrind usage as we don't build on ia64 any more
- Make sure RPATH entries are removed from programs
- Related: bz725016

* Tue Aug 31 2010 Doug Ledford <dledford@redhat.com> - 1.1.4-4
- Provide proper -devel provides
- Related: bz603804

* Mon Aug 16 2010 Doug Ledford <dledford@redhat.com> - 1.1.4-3
- Bump version to something later than base libibverbs package
- Enable valgrind support on most arches
- Use versioned provides for our pseudo provides of libibverbs base
  packages
- Related: bz603804

* Mon Aug 16 2010 Doug Ledford <dledford@redhat.com> - 1.1.4-1
- New package for rocee support
- Related: bz603804

* Tue Aug 03 2010 Doug Ledford <dledford@redhat.com> - 1.1.4-2
- Fix COW protection for large pages (bz605276)
- Resolves: bz605276

* Wed Jun 16 2010 Doug Ledford <dledford@redhat.com> - 1.1.4-1
- Update to latest upstream version
- Internal test build

* Mon Jan 11 2010 Doug Ledford <dledford@redhat.com> - 1.1.3-4
- Don't try to build on s390(x) as the hardware doesn't exist there

* Sat Dec 05 2009 Doug Ledford <dledford@redhat.com> - 1.1.3-3
- Own the /etc/libibverbs.d directory

* Fri Nov 06 2009 Doug Ledford <dledford@redhat.com> - 1.1.3-2
- Add Requires of -devel package to -devel-static package
- Add Requires of libibverbs-driver (this pulls in the various driver packages
  automatically when the libibverbs package is installed)

* Thu Oct 29 2009 Roland Dreier <rdreier@cisco.com> - 1.1.3-1
- New upstream release

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Apr 16 2008 Roland Dreier <rdreier@cisco.com> - 1.1.2-1
- New upstream release
- Update description to mention RDMA and iWARP, not just InfiniBand
- Add "Requires" tag for libibverbs base package to -devel

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1.1-3
- Autorebuild for GCC 4.3

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1.1.1-2
- Rebuild for selinux ppc32 issue.

* Fri Jun 15 2007 Roland Dreier <rdreier@cisco.com> - 1.1.1-1
- New upstream release

* Wed Apr 11 2007 Roland Dreier <rdreier@cisco.com> - 1.1-1
- New upstream release

* Mon May 22 2006 Roland Dreier <rdreier@cisco.com> - 1.1-0.1.rc2
- New upstream release
- Remove dependency on libsysfs, since it is no longer used
- Put section 3 manpages in devel package.
- Spec file cleanups: remove unused ver macro, improve BuildRoot, add
  Requires for /sbin/ldconfig, split static libraries into
  devel-static package, and don't use makeinstall any more (all
  suggested by Doug Ledford <dledford@redhat.com>).

* Thu May  4 2006 Roland Dreier <rdreier@cisco.com> - 1.0.4-1
- New upstream release

* Tue Mar 14 2006 Roland Dreier <rdreier@cisco.com> - 1.0.3-1
- New upstream release

* Mon Mar 13 2006 Roland Dreier <rdreier@cisco.com> - 1.0.1-1
- New upstream release

* Thu Feb 16 2006 Roland Dreier <rdreier@cisco.com> - 1.0-1
- New upstream release

* Wed Feb 15 2006 Roland Dreier <rolandd@cisco.com> - 1.0-0.5.rc7
- New upstream release

* Sun Jan 22 2006 Roland Dreier <rolandd@cisco.com> - 1.0-0.4.rc6
- New upstream release

* Tue Oct 25 2005 Roland Dreier <rolandd@cisco.com> - 1.0-0.3.rc5
- New upstream release

* Wed Oct  5 2005 Roland Dreier <rolandd@cisco.com> - 1.0-0.2.rc4
- Update to upstream 1.0-rc4 release

* Mon Sep 26 2005 Roland Dreier <rolandd@cisco.com> - 1.0-0.1.rc3
- Initial attempt at Fedora Extras-compliant spec file
