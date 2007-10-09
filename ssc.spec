%define name ssc
%define version 0.8
%define release %mkrel 4

%define _libdir  %_prefix/X11R6/%_lib

Summary: A free OpenGL arcade space shoot-em-up with interesting physics
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.bz2
Patch0: %{name}.libdir.patch
Source3:        %{name}-16.png
Source4:        %{name}-32.png
Source5:        %{name}-48.png
Patch1: ssc-0.8-gcc34.diff  
License: GPL
Group: Games/Arcade
Url: http://sscx.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildRequires: freetype2-devel
BuildRequires: libSDL-devel
BuildRequires: libSDL_mixer-devel
BuildRequires: libMesaGLU-devel
BuildRequires: libpng-devel


%description
SSC is a 2D space shoot-em-up featuring interesting
physics and alife. Destroy all enemies on screen to
proceed to the next level. Inherits a lot of ideas
from the game Koules.

%prep
%setup -q
%patch0 -p0
%patch1 -p0
# Arg hardcore path
perl -pi -e s!/usr/local/share!%_gamesdatadir! src/audio.cc
perl -pi -e s!/usr/local/share!%_gamesdatadir! src/menu.cc
perl -pi -e s!/usr/local/share!%_gamesdatadir! src/asteroid.cc

%build
%configure --bindir=%_gamesbindir --datadir=%_gamesdatadir
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

# Menu and icons
mkdir -p %buildroot{%_menudir,%_liconsdir,%_iconsdir,%_miconsdir}

cp %SOURCE3 %buildroot%_miconsdir/%name.png
cp %SOURCE4 %buildroot%_iconsdir/%name.png
cp %SOURCE5 %buildroot%_liconsdir/%name.png

cat > %buildroot%_menudir/%name << EOF
?package(%{name}):\
        command="%{_gamesbindir}/%{name}"\
        title="Ssc"\
        longtitle="Arcade space game"\
        needs="x11"\
        section="Amusement/Arcade"\
        icon="%{name}.png"
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{update_menus}

%postun
%{clean_menus}

%files
%defattr(-,root,root)
%doc README TODO FAQ AUTHORS ChangeLog INSTALL
%_gamesbindir/%name
%_gamesdatadir/%name
%_menudir/%name
%_miconsdir/%name.png
%_iconsdir/%name.png
%_liconsdir/%name.png

