%define name xnc
%define version 5.0.4
%define release %mkrel 6
%define iconname %{name}.png
 

Name: %name
Summary: X Northern Captain - X filemanager with many functions 
Version: %version
Release: %release
Source0: %{name}-%{version}.src.tar.bz2
Url: http://www.xnc.dubna.su  
Group:  File tools
Buildrequires: X11-devel ImageMagick
BuildRequires: libpng-devel libjpeg-devel libtiff-devel
BuildRoot: %_tmppath/%{name}-buildroot
License: GPL

%description
This program allows the user to navigate through many filesystems,
manipulate files, archives, execute commands in builtin shell, view
and edit images, text and binary files...

%prep
rm -rf $RPM_BUILD_ROOT

%setup -q

%build
# (misc) the configure is not generated by aclocal, and doesn't support --bindir and others
CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" LDFLAGS=-s ./configure \
	  --with-x \
	  --libdir=%{_libdir} 

%make

%install

%makeinstall_std

mkdir -p $RPM_BUILD_ROOT/%{_mandir}
mv  -f  $RPM_BUILD_ROOT/%{_prefix}/man/man1 $RPM_BUILD_ROOT/%{_mandir}

mkdir -p $RPM_BUILD_ROOT/usr/share/%{name}-%{version}/help
cp $RPM_BUILD_DIR/%{name}-%{version}/doc/*.html  $RPM_BUILD_ROOT/usr/share/%{name}-%{version}/help 
 
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

mkdir -p $RPM_BUILD_ROOT/%{_menudir}
cat << EOF > $RPM_BUILD_ROOT/%{_menudir}/%{name}
?package(%{name}):\
needs="x11"\
section="System/File Tools"\
title="Xnc"\
longtitle="X Northern Captain - X filemanager with many functions "\ 
command="xnc"\
icon="%{name}.png"
EOF

 


%find_lang %{name}

%post 
%{update_menus}

%postun
%{clean_menus}  

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
%{_menudir}/%{name}
%{_miconsdir}/%{iconname}
%{_iconsdir}/%{iconname}
%{_liconsdir}/%{iconname}
%_datadir/%name-%version

