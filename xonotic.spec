%global _hardened_build 1
%global dpver 20130605

Summary:    Multiplayer, deathmatch oriented first person shooter
Name:       xonotic
Version:    0.7.0
Release:    1%{?dist}
License:    GPLv2+ and LGPLv2+ and BSD
Group:      Amusements/Games
URL:        http://www.xonotic.org/
# Custom tarball:
# wget http://dl.xonotic.org/xonotic-%{version}.zip
# unzip xonotic-%{version}.zip
# cd Xonotic/source/
# cp ../misc/logos/icons_png/xonotic_256.png darkplaces/
# tar -czf darkplaces-%{version}.tar.gz darkplaces/
# tar -czf d0_blind_id-%{version}.tar.gz d0_blind_id/
Source0:    http://dl.xonotic.org/%{name}-%{version}.zip
#Source0: darkplaces-%{version}.tar.gz
Source1: %{name}.desktop
Source2: d0_blind_id-%{version}.tar.gz
Source10: darkplaces-quake.sh
Source11: darkplaces-quake.autodlrc
Source12: darkplaces-quake.desktop
Patch0: darkplaces-crypto.patch
Patch1: xonotic-nosse.patch

BuildRequires: alsa-lib-devel
BuildRequires: desktop-file-utils
BuildRequires: file
BuildRequires: libX11-devel
BuildRequires: mesa-libGL-devel
%if 0%{?rhel}
BuildRequires: libjpeg-devel
%else
BuildRequires: libjpeg-turbo-devel
%endif
BuildRequires: libXext-devel 
BuildRequires: libXpm-devel
BuildRequires: libXxf86dga-devel
BuildRequires: libXxf86vm-devel
BuildRequires: SDL-devel

Requires: xonotic-data = %{version}
Requires: darkplaces = %{dpver}-%{release}
Requires: opengl-games-utils

Obsoletes: nexuiz <= 2.5.2

Provides: nexuiz = %{name}-%{version}

%description
Xonotic is a fast-paced, chaotic, and intense multiplayer first person shooter,
focused on providing basic, old style deathmatches.

%package server
Group:      Amusements/Games
Summary:    Dedicated server for the Xonotic first person shooter
Requires:   xonotic-data = %{version}
Requires:   darkplaces-server = %{dpver}-%{release}
Obsoletes:  nexuiz-server <= 2.5.2
Provides:   nexuiz-server = %{name}-%{version}


%description server
Xonotic is a fast-paced, chaotic, and intense multiplayer first person shooter,
focused on providing basic, old style deathmatches.

This is the Xonotic dedicated server required to host network games.

%package -n darkplaces
Summary:    Modified Quake engine
Version:    %{dpver}
Group:      Amusements/Games
# This is necessary as these libraries are loaded during runtime
# and therefore it isn't picked up by RPM during build
Requires: zlib libvorbis libjpeg curl

%description -n darkplaces
DarkPlaces is a modified Quake engine.

%package -n darkplaces-server
Summary:    Quake engine server
Version:    %{dpver}
Group:      Amusements/Games
# This is necessary as these libraries are loaded during runtime
# and therefore it isn't picked up by RPM during build
Requires: zlib curl

%description -n darkplaces-server
DarkPlaces Quake engine server.

%package -n darkplaces-quake
Summary:    Multiplayer, deathmatch oriented first person shooter
Version:    %{dpver}
Group:      Amusements/Games
Requires:   autodownloader
Requires:   opengl-games-utils
Requires:   darkplaces = %{dpver}-%{release}

%description -n darkplaces-quake
Rage through levels of sheer terror and fully immersive sound and
lighting.  Arm yourself against the cannibalistic Ogre, fiendish Vore
and indestructible Schambler using letal nails, fierce Thunderbolts
and abominable Rocket and Grenade Launchers.

%package -n darkplaces-quake-server
Summary:    Dedicated DarkPlaces Quake server
Version:    %{dpver}
Group:      Amusements/Games
Requires:   darkplaces-server = %{dpver}-%{release}

%description -n darkplaces-quake-server
DarkPlaces server required for hosting multiplayer network Quake games.

%package -n data
Summary:    Game data for the Xonotic first person shooter
Version:    %{version}
Group:      Amusements/Games
BuildArch:  noarch
Obsoletes:  nexuiz-data <= 2.5.2
Provides:   nexuiz-data = %{name}-%{version}

%description -n data
Data (textures, maps, sounds and models) required to play xonotic.

%prep
%setup -q -n Xonotic
pushd source
    cp ../misc/logos/icons_png/xonotic_256.png darkplaces/
    pushd darkplaces
        sed -i 's/\r//' darkplaces.txt
        sed -i 's,/usr/X11R6/,/usr/,g' makefile makefile.inc
        sed -i 's/nexuiz/xonotic/g' makefile makefile.inc
        mv darkplaces.txt ../../
    popd
    tar -C darkplaces/ -xzf %{SOURCE2}
#     %patch0 -p0
#     %ifnarch %{ix86} x86_64
#     %patch1 -p0
#     %endif
popd

%build

#pushd d0_blind_id
#%%configure --disable-rijndael --without-openssl
#make
#popd
pushd source/darkplaces
    export DP_FS_BASEDIR=%{_datadir}/xonotic
    #export DP_CRYPTO_STATIC_LIBDIR="." 
    #export DP_CRYPTO_RIJNDAEL_STATIC_LIBDIR="."
    make release OPTIM_RELEASE="$RPM_OPT_FLAGS" STRIP=:
    make xonotic OPTIM_RELEASE="$RPM_OPT_FLAGS" STRIP=:
popd

%install
# Install the main programs
mkdir -p %{buildroot}%{_bindir}
pushd source/darkplaces
    for i in darkplaces xonotic; do
            install -pm 0755 $i-glx %{buildroot}%{_bindir}/$i-glx
            install -pm 0755 $i-sdl %{buildroot}%{_bindir}/$i-sdl
            install -pm 0755 $i-dedicated %{buildroot}%{_bindir}/$i-dedicated
    done
popd
# Install the desktop files
mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
    --dir %{buildroot}%{_datadir}/applications \
    %{SOURCE1}
desktop-file-install \
    --dir %{buildroot}%{_datadir}/applications \
    %{SOURCE12}

pushd source/darkplaces
    for s in 16 24 32 48 64 72 ; do
        install -Dpm 0644 darkplaces${s}x${s}.png \
        %{buildroot}%{_datadir}/icons/hicolor/${s}x${s}/apps/darkplaces.png
    done
    install -Dpm 0655 xonotic_256.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/xonotic.png

    ln -s opengl-game-wrapper.sh %{buildroot}%{_bindir}/xonotic-sdl-wrapper
    ln -s opengl-game-wrapper.sh %{buildroot}%{_bindir}/darkplaces-sdl-wrapper
    ln -s opengl-game-wrapper.sh %{buildroot}%{_bindir}/darkplaces-quake-sdl-wrapper

    for i in glx sdl dedicated ; do
        install -Dpm 755 %{SOURCE10} %{buildroot}%{_bindir}/darkplaces-quake-$i
    done
popd
install -Dpm 644 %{SOURCE11} %{buildroot}%{_datadir}/darkplaces/quake.autodlrc

#install -Dpm 755 d0_blind_id/blind_id %{buildroot}%{_bindir}/blind_id

mkdir -p %{buildroot}%{_datadir}/xonotic/data/
install -p data/xonotic-%{dpver}-data.pk3 %{buildroot}%{_datadir}/xonotic/data/
install -p data/xonotic-%{dpver}-maps.pk3 %{buildroot}%{_datadir}/xonotic/data/
install -p data/xonotic-%{dpver}-music.pk3 %{buildroot}%{_datadir}/xonotic/data/
install -p data/xonotic-%{dpver}-nexcompat.pk3 %{buildroot}%{_datadir}/xonotic/data/
install -p data/font-nimbussansl-%{dpver}.pk3 %{buildroot}%{_datadir}/xonotic/data/
install -p data/font-xolonium-%{dpver}.pk3 %{buildroot}%{_datadir}/xonotic/data/
install -p key_0.d0pk %{buildroot}%{_datadir}/xonotic/

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%post -n darkplaces
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun -n darkplaces
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans -n darkplaces
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%{_bindir}/xonotic-sdl-wrapper
%{_bindir}/xonotic-glx
%{_bindir}/xonotic-sdl
#%{_bindir}/blind_id
%{_datadir}/icons/hicolor/*/apps/xonotic.png
%{_datadir}/applications/*%{name}.desktop

%files server
%{_bindir}/xonotic-dedicated

%files -n darkplaces
%{_bindir}/darkplaces-sdl-wrapper
%{_bindir}/darkplaces-glx
%{_bindir}/darkplaces-sdl
%doc COPYING darkplaces.txt
%{_datadir}/icons/hicolor/*/apps/darkplaces.png

%files -n darkplaces-server
%doc COPYING darkplaces.txt
%{_bindir}/darkplaces-dedicated

%files -n darkplaces-quake
%{_bindir}/darkplaces-quake-glx
%{_bindir}/darkplaces-quake-sdl
%{_bindir}/darkplaces-quake-sdl-wrapper
%{_datadir}/darkplaces/
%{_datadir}/applications/*darkplaces-quake.desktop

%files -n darkplaces-quake-server
%doc COPYING darkplaces.txt
%{_bindir}/darkplaces-quake-dedicated

%files -n data
%doc GPL* COPYING
%{_datadir}/xonotic/


%changelog
* Thu Jun 13 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.7.0-1.1
- Update patch for arm

* Thu Jun 13 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.7.0-1
- Bump to 0.7

* Thu Feb 28 2013 Dan Horák <dan[at]danny.cz> - 0.6.0-8
- Fix build on non-x86 arches

* Fri Feb 22 2013 Jon Ciesla <limburgher@gmail.com> - 0.6.0-7
- Fix server O/P.

* Wed Feb 20 2013 Jon Ciesla <limburgher@gmail.com> - 0.6.0-6
- Drop sse flags to allow buildon ARM.

* Wed Feb 20 2013 Jon Ciesla <limburgher@gmail.com> - 0.6.0-5
- Removed more macros.
- Enabled parallel build, then re-disabled, unreliable.
- Fixed server file ownership.

* Fri Feb 08 2013 Jon Ciesla <limburgher@gmail.com> - 0.6.0-4
- Drop nexuiz name completely.
- Added jpeg BRs, neatened BRs.
- De-macroized many commands.
- Dropped dektop vendor tag.
- Preserved timestamps.

* Thu Dec 20 2012 Jon Ciesla <limburgher@gmail.com> - 0.6.0-2
- add d0_blind_id.

* Mon Mar 12 2012 Jon Ciesla <limburgher@gmail.com> - 0.6.0-1
- New upstream.

* Thu Jan 26 2012 Jon Ciesla <limburgher@gmail.com> - 0.5.0-1
- Initial version, based on Nexuiz 2.5.2 package.