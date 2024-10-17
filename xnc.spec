%define name xnc
%define version 5.0.4
%define release %mkrel 10
%define iconname %{name}.png
 

Name: %name
Summary: X Northern Captain - X filemanager with many functions 
Version: %version
Release: %release
Source0: %{name}-%{version}.src.tar.bz2
Patch0: xnc-gcc44.patch
Patch1: xnc-5.0.4-str-fmt.patch
Patch2: xnc-5.0.4-link.patch
Url: https://www.xnc.dubna.su  
Group:  File tools
BuildRequires: libx11-devel
BuildRequires: libxext-devel
Buildrequires: libxt-devel
BuildRequires: jpeg-devel
BuildRequires: tiff-devel
BuildRequires: png-devel
Buildrequires: imagemagick
BuildRoot: %_tmppath/%{name}-buildroot
License: GPL

%description
This program allows the user to navigate through many filesystems,
manipulate files, archives, execute commands in builtin shell, view
and edit images, text and binary files...

%prep
%setup -q
%patch0 -p0
%patch1 -p0
%patch2 -p0

%build
%configure2_5x --with-x
make

%install
rm -fr %buildroot
%makeinstall_std

mkdir -p $RPM_BUILD_ROOT%_sysconfdir/X11/wmconfig
cat > $RPM_BUILD_ROOT%_sysconfdir/X11/wmconfig/xnc <<EOF
xnc name "X Northern Captain"
xnc description "filemanager for X Window"
xnc icon "xnc.png"
xnc mini-icon "mini-xnc.png"
xnc group "Utilities/File Management"
xnc exec "xnc &"
EOF

mkdir -p %{buildroot}{%{_miconsdir},%{_iconsdir},%{_liconsdir},%{_menudir}}
convert %{buildroot}/usr/share/pixmaps/xnc.png -geometry 48x48 %{buildroot}%{_liconsdir}/%{iconname}
convert %{buildroot}/usr/share/pixmaps/xnc.png -geometry 32x32 %{buildroot}%{_iconsdir}/%{iconname}
convert %{buildroot}/usr/share/pixmaps/xnc.png -geometry 16x16 %{buildroot}%{_miconsdir}/%{iconname}

rm -fr %{buildroot}%{_datadir}/doc/

%find_lang %{name}

%if %mdkversion < 200900
%post 
%{update_menus}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}  
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root) 
%doc AUTHORS INSTALL INSTALL-bin.xnc LICENSE  release.news 
%doc README README.keys TODO WHATS_NEW   
%_bindir/*
%_libdir/xnc
%_mandir/man1/*
%config(noreplace) %_sysconfdir/X11/wmconfig/xnc
%{_datadir}/applications/xnc-gnome2.desktop
%{_datadir}/applnk/System/X_Northern_Captain.desktop
%{_datadir}/gnome/apps/Applications/xnc.desktop
%{_datadir}/pixmaps/*.* 
%{_miconsdir}/%{iconname}
%{_iconsdir}/%{iconname}
%{_liconsdir}/%{iconname}
