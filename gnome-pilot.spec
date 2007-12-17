%define major 2
%define pilot_link_version 0.12.0
%define libname %mklibname %{name} %{major}

Summary:	GNOME Pilot programs
Name:		gnome-pilot
Version: 2.0.15
Release:	%mkrel 4
License:	GPL/LGPL
Group:		Graphical desktop/GNOME
Source0: 	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
# (fc) 2.0.15-2mdv fix version field in pc file
Patch0:		gnome-pilot-2.0.15-fixversion.patch
URL:		http://www.gnome.org/projects/gnome-pilot/

BuildRequires: pilot-link-devel >= %{pilot_link_version}
BuildRequires: libgnomeui2-devel
BuildRequires: libpanel-applet-devel
BuildRequires: scrollkeeper
BuildRequires: perl-XML-Parser
BuildRequires: automake
BuildRequires: intltool
BuildRequires: desktop-file-utils
BuildRequires: hal-devel
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

%package -n %{libname}-devel

Summary:	GNOME pilot libraries, includes, etc
Group:		Development/GNOME and GTK+
Requires: 	%{name} = %{version}
Requires:	%{libname} = %{version}

Requires:	pilot-link-devel >= %{pilot_link_version}
Requires:	libgnomeui2-devel

Obsoletes:  %{name}-devel
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}

%description -n %{libname}-devel
gpilotd libraries and includes.



%prep
%setup -q
%patch0 -p1 -b .fixversion

%build

%configure2_5x --enable-usb --enable-vfs --enable-network

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

# remove unpackaged files 
rm -f $RPM_BUILD_ROOT%{_libdir}/gnome-pilot/conduits/*.{a,la}

%clean
rm -rf $RPM_BUILD_ROOT

%define gconf_schemas pilot

%post
%{update_menus}
%post_install_gconf_schemas %gconf_schemas
%update_scrollkeeper
%update_desktop_database

%post -n %{libname} -p /sbin/ldconfig

%preun
%preun_uninstall_gconf_schemas %gconf_schemas

%postun
%{clean_menus}
%clean_scrollkeeper
%clean_desktop_database

%postun -n %{libname} -p /sbin/ldconfig

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
%{_datadir}/gnome-pilot
%{_datadir}/idl/*
%{_datadir}/mime-info/*
%{_datadir}/pixmaps/*
%{_mandir}/man1/*
%_datadir/applications/*.desktop
%dir %{_datadir}/omf/*
%{_datadir}/omf/*/*-C.omf

%files -n %{libname}
%defattr(-, root, root)
%{_libdir}/*.so.*


%files -n %{libname}-devel
%defattr(-, root, root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*a
%{_libdir}/pkgconfig/*
