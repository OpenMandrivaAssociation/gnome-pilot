%define major 5
%define pilot_link_version 0.12.0
%define libname %mklibname %{name} %{major}
%define cmmajor 4
%define libnamecm %mklibname pilotdcm %cmmajor
%define conduitmajor 3
%define libnameconduit %mklibname gpilotdconduit %conduitmajor
%define develname %mklibname -d %{name}

Summary:	GNOME Pilot programs
Name:		gnome-pilot
Version: 2.32.1
Release:	%mkrel 2
License:	GPLv2+ and LGPLv2+
Group:		Graphical desktop/GNOME
Source0: 	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
URL:		http://www.gnome.org/projects/gnome-pilot/

BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildRequires: pilot-link-devel >= %{pilot_link_version}
BuildRequires: evolution-data-server-devel
BuildRequires: libpanel-applet-devel
BuildRequires: libgudev-devel
BuildRequires: scrollkeeper
BuildRequires: automake
BuildRequires: intltool
BuildRequires: desktop-file-utils
BuildRequires: gnome-doc-utils
BuildRequires: gob2
Requires(post): scrollkeeper desktop-file-utils
Requires(postun): scrollkeeper desktop-file-utils

%description
GNOME pilot is a collection of programs and daemon for integrating
GNOME and the PalmPilot (tm).

%package -n %{libname}

Summary:	GNOME pilot libraries
Group:		System/Libraries

%description -n %{libname}
GNOME-Pilot libraries 

%package -n %{libnamecm}

Summary:	GNOME pilot libraries
Group:		System/Libraries

%description -n %{libnamecm}
GNOME-Pilot libraries 

%package -n %{libnameconduit}

Summary:	GNOME pilot libraries
Group:		System/Libraries

%description -n %{libnameconduit}
GNOME-Pilot libraries 

%package -n %{develname}
Summary:	GNOME pilot libraries, includes, etc
Group:		Development/GNOME and GTK+
Requires: 	%{name} = %{version}
Requires:	%{libname} = %{version}
Requires:	%{libnamecm} = %{version}
Requires:	%{libnameconduit} = %{version}
Requires:	pilot-link-devel >= %{pilot_link_version}
Obsoletes:	%{name}-devel < %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Obsoletes:	%{_lib}gnome-pilot2-devel < 2.0.17-7

%description -n %{develname}
gpilotd libraries and includes.

%prep
%setup -q

%build
%define _disable_ld_no_undefined 1
%configure2_5x --enable-usb --enable-network
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std 

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-gpilot-install-file.desktop << EOF
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
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/gpilotd-control-applet.desktop 

%{find_lang} %{name} --with-gnome
for omf in %buildroot%_datadir/omf/*/*-??*.omf;do
   echo "%lang($(basename $omf|sed -e s/.*-// -e s/.omf//)) $(echo $omf|sed -e s!%buildroot!!)" >> %name.lang
done 
# remove unpackaged files
find $RPM_BUILD_ROOT -name *.a | xargs rm

%clean
rm -rf $RPM_BUILD_ROOT

%define gconf_schemas pilot
%preun
%preun_uninstall_gconf_schemas %gconf_schemas

%files -f %{name}.lang
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_sysconfdir}/gconf/schemas/pilot.schemas
%{_bindir}/*
%{_libexecdir}/gpilotd
%{_libexecdir}/gpilot-applet
%{_libdir}/bonobo/servers/*
%dir %{_libdir}/gnome-pilot
%dir %{_libdir}/gnome-pilot/conduits
%{_libdir}/gnome-pilot/conduits/*.so*
%{_libdir}/gnome-pilot/conduits/*.la
%{_datadir}/gnome-pilot
%{_datadir}/mime-info/*
%{_datadir}/pixmaps/*
%{_mandir}/man1/*
%_datadir/applications/*.desktop
%dir %{_datadir}/omf/*
%{_datadir}/omf/*/*-C.omf
%_datadir/dbus-1/services/org.gnome.GnomePilot.service

%files -n %{libname}
%defattr(-, root, root)
%{_libdir}/libgpilotd.so.%{major}*

%files -n %{libnamecm}
%defattr(-, root, root)
%{_libdir}/libgpilotdcm.so.%{cmmajor}*

%files -n %{libnameconduit}
%defattr(-, root, root)
%{_libdir}/libgpilotdconduit.so.%{conduitmajor}*

%files -n %{develname}
%defattr(-, root, root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.la
%{_libdir}/pkgconfig/*
