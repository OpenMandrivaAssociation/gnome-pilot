%define api 3.0
%define major 0
%define cmmajor 4
%define conduitmajor 3
%define libname %mklibname %{name} %{api} %{major}
%define libcm %mklibname pilotdcm %{api} %{cmmajor}
%define libconduit %mklibname gpilotdconduit %{api} %{conduitmajor}
%define develname %mklibname -d %{name}

Summary:	GNOME Pilot programs
Name:		gnome-pilot
Version:	2.91.93
Release:	1
License:	GPLv2+ and LGPLv2+
Group:		Graphical desktop/GNOME
URL:		http://www.gnome.org/projects/gnome-pilot/
Source0: 	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.xz

BuildRequires: intltool
BuildRequires: desktop-file-utils
BuildRequires: gnome-doc-utils
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
%define _disable_ld_no_undefined 1
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
for omf in %{buildroot}%{_datadir}/omf/*/*-??*.omf;do
   echo "%lang($(basename $omf|sed -e s/.*-// -e s/.omf//)) $(echo $omf|sed -e s!%{buildroot}!!)" >> %{name}.lang
done 

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
%dir %{_datadir}/omf/*
%{_datadir}/applications/*.desktop
%{_datadir}/gnome-panel/4.0/applets/org.gnome.applets.PilotApplet.panel-applet
%{_datadir}/gnome-pilot
%{_datadir}/mime-info/*
%{_datadir}/omf/*/*-C.omf
%{_datadir}/dbus-1/services/org.gnome.GnomePilot.service
%{_datadir}/dbus-1/services/org.gnome.panel.applet.PilotAppletFactory.service
%{_datadir}/pixmaps/*
%{_mandir}/man1/*

%files -n %{libname}
%{_libdir}/libgpilotd.so.%{major}*

%files -n %{libcm}
%{_libdir}/libgpilotdcm.so.%{cmmajor}*

%files -n %{libconduit}
%{_libdir}/libgpilotdconduit.so.%{conduitmajor}*

%files -n %{develname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
