%define _disable_ld_no_undefined 1

%define api 3.0
%define major 0
%define cmmajor 0
%define conduitmajor 0
%define libname %mklibname %{name} %{api} %{major}
%define libcm %mklibname pilotdcm %{api} %{cmmajor}
%define libconduit %mklibname gpilotdconduit %{api} %{conduitmajor}
%define develname %mklibname -d %{name}

Summary:	GNOME Pilot programs
Name:		gnome-pilot
Version:	2.91.93
Release:	3
License:	GPLv2+ and LGPLv2+
Group:		Graphical desktop/GNOME
URL:		http://www.gnome.org/projects/gnome-pilot/
Source0: 	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2

BuildRequires: intltool
BuildRequires: desktop-file-utils
BuildRequires: gnome-doc-utils-devel
BuildRequires: gob2
BuildRequires: pkgconfig(dbus-glib-1) >= 0.74
BuildRequires: pkgconfig(gconf-2.0)
BuildRequires: pkgconfig(gtk+-3.0) >= 2.99.2
BuildRequires: pkgconfig(gudev-1.0)
BuildRequires: pkgconfig(libebook-1.2)
BuildRequires: pkgconfig(libecal-1.2)
BuildRequires: pkgconfig(libedataserverui-3.0)
BuildRequires: pkgconfig(libpanelapplet-4.0)
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(pilot-link) >= 0.12.0
BuildRequires: scrollkeeper

%description
GNOME pilot is a collection of programs and daemon for integrating
GNOME and the PalmPilot (tm).

%package -n %{libname}
Summary:	GNOME pilot libraries
Group:		System/Libraries

%description -n %{libname}
GNOME-Pilot libraries 

%package -n %{libcm}
Summary:	GNOME pilot libraries
Group:		System/Libraries

%description -n %{libcm}
GNOME-Pilot libraries 

%package -n %{libconduit}
Summary:	GNOME pilot libraries
Group:		System/Libraries

%description -n %{libconduit}
GNOME-Pilot libraries 

%package -n %{develname}
Summary:	GNOME pilot libraries, includes, etc
Group:		Development/GNOME and GTK+
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libcm} = %{version}-%{release}
Requires:	%{libconduit} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
%rename	%{name}-devel < %{version}-%{release}

%description -n %{develname}
gpilotd libraries and includes.

%prep
%setup -q

%build
%configure2_5x \
	--disable-static \
	--enable-usb \
	--enable-network

%make

%install
rm -rf %{buildroot}
%makeinstall_std 
find %{buildroot} -name '*.la' -exec rm -f {} ';'

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-gpilot-install-file.desktop << EOF
[Desktop Entry]
Name=GNOME Pilot Install Databases
Comment=Install Databases on your Palm Pilot
Exec=gpilot-install-file %U
Icon=gnome-palm
Terminal=false
Type=Application
StartupNotify=true
MimeType=application/x-palm-database;
Categories=GNOME;GTK;TelephonyTools;Utility;
Hidden=true
EOF

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --dir %{buildroot}%{_datadir}/applications \
  %{buildroot}%{_datadir}/applications/gpilotd-control-applet.desktop 

%{find_lang} %{name} --with-gnome
#for omf in %{buildroot}%{_datadir}/omf/*/*-??*.omf;do
#   echo "%lang($(basename $omf|sed -e s/.*-// -e s/.omf//)) $(echo $omf|sed -e s!%{buildroot}!!)" >> %{name}.lang
#done 

%define gconf_schemas pilot
%preun
%preun_uninstall_gconf_schemas %gconf_schemas

%files -f %{name}.lang
%doc AUTHORS COPYING ChangeLog NEWS README
%{_sysconfdir}/gconf/schemas/pilot.schemas
%{_bindir}/*
%{_libexecdir}/gpilotd
%{_libexecdir}/gpilot-applet
%dir %{_libdir}/gnome-pilot
%dir %{_libdir}/gnome-pilot/conduits
%{_libdir}/gnome-pilot/conduits/*.so
#%dir %{_datadir}/omf/*
%{_datadir}/applications/*.desktop
%{_datadir}/gnome-panel/4.0/applets/org.gnome.applets.PilotApplet.panel-applet
%{_datadir}/gnome-pilot
%{_datadir}/mime-info/*
#%{_datadir}/omf/*/*-C.omf
%{_datadir}/dbus-1/services/org.gnome.GnomePilot.service
%{_datadir}/dbus-1/services/org.gnome.panel.applet.PilotAppletFactory.service
%{_datadir}/pixmaps/*
%{_mandir}/man1/*

%files -n %{libname}
%{_libdir}/libgpilotd-%{api}.so.%{major}*

%files -n %{libcm}
%{_libdir}/libgpilotdcm-%{api}.so.%{cmmajor}*

%files -n %{libconduit}
%{_libdir}/libgpilotdconduit-%{api}.so.%{conduitmajor}*

%files -n %{develname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*



%changelog
* Mon Sep 03 2012 Vladimir Testov <vladimir.testov@rosalab.ru> 2.91.93-2
- adopted for ROSA

* Thu Dec 08 2011 Matthew Dawkins <mattydaw@mandriva.org> 2.91.93-1
+ Revision: 739099
- fixed files list
- fixed majors
- new version 2.91.93
- cleaned up spec
- converted BRs to pkgconfig provides
- removed .la files
- disabled static build
- removed mkrel, BuildRoot, defattr, clean section
- added api to lib pkgs

* Mon May 23 2011 Funda Wang <fwang@mandriva.org> 2.32.1-3
+ Revision: 677714
- rebuild to add gconftool as req

* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 2.32.1-2
+ Revision: 664879
- mass rebuild

* Mon Mar 21 2011 GÃ¶tz Waschk <waschk@mandriva.org> 2.32.1-1
+ Revision: 647289
- update build deps
- disable hal
- new version
- update omf file list

* Sun Sep 26 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.32.0-1mdv2011.0
+ Revision: 581068
- new version
- drop all patches
- update file list
- update build deps
- fix build by disabling no-undefined

* Wed Feb 17 2010 Funda Wang <fwang@mandriva.org> 2.0.17-7mdv2010.1
+ Revision: 506941
- new devel package policy

* Mon Sep 14 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.0.17-6mdv2010.0
+ Revision: 439568
- update build deps
- rebuild for new libusb

* Tue Aug 11 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.0.17-5mdv2010.0
+ Revision: 414879
- improve linking, don't link libs with libglade

* Tue Aug 11 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.0.17-4mdv2010.0
+ Revision: 414792
- readd libtool archives, it is Mandriva policy to keep them

* Tue Aug 11 2009 Funda Wang <fwang@mandriva.org> 2.0.17-3mdv2010.0
+ Revision: 414685
- drop unused *.la files (which causes linking error with our default ldflags)

* Tue May 19 2009 Christophe Fergeau <cfergeau@mandriva.com> 2.0.17-2mdv2010.0
+ Revision: 377581
- Make sure newer libtool files are used after running autoreconf

* Tue Jan 20 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.0.17-2mdv2009.1
+ Revision: 331689
- fix linking with hal

* Thu Jan 08 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.0.17-1mdv2009.1
+ Revision: 327028
- new version
- drop patch 1
- fix format strings
- update license

* Sun Nov 09 2008 Oden Eriksson <oeriksson@mandriva.com> 2.0.16-3mdv2009.1
+ Revision: 301531
- rebuilt against new libxcb

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 2.0.16-2mdv2009.0
+ Revision: 222551
- buildrequires libglade2-devel

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Fri Mar 21 2008 Frederic Crozat <fcrozat@mandriva.com> 2.0.16-1mdv2008.1
+ Revision: 189419
- Patch1: fix detection of Palm with latest HAL

  + GÃ¶tz Waschk <waschk@mandriva.org>
    - new version
    - drop patch 1

* Mon Feb 04 2008 Frederic Crozat <fcrozat@mandriva.com> 2.0.15-5mdv2008.1
+ Revision: 162156
- Patch1 (SVN): fix unresolved symbols (SVN) (GNOME bug #431145)

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 09 2007 Funda Wang <fwang@mandriva.org> 2.0.15-4mdv2008.1
+ Revision: 116714
- drop old menu

  + Guillaume Rousse <guillomovitch@mandriva.org>
    - rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'

* Tue Aug 07 2007 Frederic Crozat <fcrozat@mandriva.com> 2.0.15-2mdv2008.0
+ Revision: 59886
- Reupload 2.0.15 in svn
- Patch0: fix version in .pc file, allow package to be built


* Tue Sep 26 2006 Frederic Crozat <fcrozat@mandriva.com> 2.0.14-2mdv2007.0
- Rebuild with latest ncurses

* Thu Sep 07 2006 Frederic Crozat <fcrozat@mandriva.com> 2.0.14-1mdv2007.0
- Release 2.0.14 final

* Wed Aug 30 2006 Frederic Crozat <fcrozat@mandriva.com> 2.0.14-0.pre6.1mdv2007.0
- Release 2.0.14pre6
- remove patch0, merged upstream

* Wed Aug 02 2006 Götz Waschk <waschk@mandriva.org> 2.0.13-7mdv2007.0
- xdg menu

* Mon Feb 27 2006 Frederic Crozat <fcrozat@mandriva.com> 2.0.13-6mdk
- Use mkrel
- Fix package uninstall

* Fri Dec 30 2005 Mandriva Linux Team <http://www.mandrivaexpert.com/> 2.0.13-5mdk
- Rebuild

* Fri Sep 02 2005 GÃ¶tz Waschk <waschk@mandriva.org> 2.0.13-4mdk
- rebuild to remove glitz dep

* Thu Aug 18 2005 Christiaan Welvaart <cjw@daneel.dyndns.org> 2.0.13-3mdk
- add BuildRequires: intltool

* Fri Aug 12 2005 Frederic Crozat <fcrozat@mandriva.com> 2.0.13-2mdk 
- Patch1: fix libdir for use on x86-64

* Thu Jun 16 2005 Götz Waschk <waschk@mandriva.org> 2.0.13-1mdk
- fix the menu
- replace prereq tag
- New release 2.0.13

* Mon Feb 28 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.0.12-3mdk
- rebuild to sync up with x86_64 tree and current cooker env, aka no
  more indent in orbit-idl

* Wed Jan 05 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 2.0.12-2mdk 
- Rebuild with latest howl

* Fri Dec 10 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.0.12-1mdk
- New release 2.0.12
- Remove patches 3, 4, 5 (merged upstream)
- Patch0: add support for Zire72 (Mdk bug #12502)

* Fri Sep 03 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.0.11-4mdk
- Patch5 (CVS): fix crash when using gpilot-install-file
- add default action for installing prc/pdb

* Wed Sep 01 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.0.11-3mdk
- Update patch3 to fully handle non ASCII username
- Patch4 : Fix sync on all new USB devices

* Sat Aug 28 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 2.0.11-2mdk
- add BuildRequires: perl-XML-Parser

* Fri Aug 27 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.0.11-1mdk
- Release 2.0.11
- Remove patches 2, 4, 7 (merged upstream), 5, 6 (obsolete)

* Thu Jul 08 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.0.10-8mdk
- Update patch4 with correct id for Treo 600 (found by Christophe Mertz)
- Patch7 : fix build with gcc 3.4

* Fri Feb 20 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.0.10-7mdk
- Patch6 : fix crash when /proc/bus/usb is not mounted

* Tue Feb 10 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.0.10-6mdk
- Update patch4 with Aceeca meazura device id

* Tue Feb 10 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.0.10-5mdk
- Patch4 : update device id to latest kernel list
- Fix menu

