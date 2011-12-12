#define gitrev		6a68361
%define version		1.0
#define	prerel		rc2
%define longversion	0100
%define mdvrel		1

Name:		arduino
Version:	%version
Release:	%mkrel %{mdvrel}%{?prerel:.%prerel}
Summary:	An IDE for Arduino-compatible electronics prototyping platforms
Group:		Development/Other
License:	GPLv2+ and LGPLv2+ and CC-BY-SA
URL:		http://www.arduino.cc/

# There are lots of binaries in the "source" tarball.  Remove them with:
# curl https://nodeload.github.com/arduino/Arduino/tarball/%{version}-%{prerel} | tar -xzvf - && rm -rf arduino-Arduino-%{gitrev}/build/linux/dist/tools/* && find arduino-Arduino-%{gitrev} \( -type d \( -name macosx -o -name windows \) -o -type f \( -iname '*.jar' -or -iname '*.tgz' -or -iname '*.so' \) \) -print0 | xargs -0 rm -rf && tar -cjf arduino-Arduino-%{gitrev}.tar.bz2 arduino-Arduino-%{gitrev}
# See also http://code.google.com/p/arduino/issues/detail?id=193
%if 0%{?gitrev}
Source0:	arduino-Arduino-%{gitrev}.tar.bz2
%else
Source0:	%{name}-%{version}.tar.bz2
%endif
BuildArch:	noarch

# Use unbundled libs:
Patch0:		arduino-0022-mdv-script.patch

Patch2:		arduino-1.0-rc2-mdv-use-system-avrdude.patch
# Requested upstream in http://github.com/arduino/Arduino/pull/5:
Patch3:		arduino-0022-fedora-use-system-rxtx.patch

# Requested upstream in http://github.com/arduino/Arduino/pull/6:
Patch4:		arduino-0022-fedora-icons-etc.patch

Patch6:		arduino-0022-mdv-add-to-groups.patch
Patch7:		arduino-0022-mdv-release-check.patch
Patch8:		arduino-1.0-rc2-mdv-dont-build-avrdude.patch

BuildRequires:	java-devel >= 0:1.6.0 jpackage-utils ant ant-apache-regexp desktop-file-utils ecj jna rxtx git
Requires:	%{name}-core = %{version}-%{release}, %{name}-doc = %{version}-%{release}
Requires:	java >= 0:1.6.0 x11-font-type1 ecj jna rxtx
Requires:	zenity perl polkit


%description
Arduino is an open-source electronics prototyping platform based on
flexible, easy-to-use hardware and software. It's intended for artists,
designers, hobbyists, and anyone interested in creating interactive
objects or environments.

This package contains an IDE that can be used to develop and upload code
to the micro-controller.


%package core
Summary:	Files required for compiling code for Arduino-compatible micro-controllers
Group:		Development/Other
Requires:	cross-avr-gcc cross-avr-gcc-c++ avr-libc avrdude


%description core
Arduino is an open-source electronics prototyping platform based on
flexible, easy-to-use hardware and software. It's intended for artists,
designers, hobbyists, and anyone interested in creating interactive
objects or environments.

This package contains the core files required to compile and upload
Arduino code.


%package doc
Summary:	Documentation for the Arduino micro-controller platform
Group:		Development/Other


%description doc
Arduino is an open-source electronics prototyping platform based on
flexible, easy-to-use hardware and software. It's intended for artists,
designers, hobbyists, and anyone interested in creating interactive
objects or environments.

This package contains reference documentation.


%prep
%if 0%{?gitrev}
%setup -q -n arduino-Arduino-%{gitrev}
%else
%setup -q
%endif
find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;
%patch6 -p1
chmod a+rx build/linux/%{name}-add-groups
%patch0
%patch2 -p1
%patch3 -p1

# "git apply" fails silently if pwd is git-controlled.
pwd=`pwd`
cd /
git apply --directory=$pwd %{PATCH4}
cd $pwd

%patch7 -p1
%patch8 -p1
build-jar-repository -p -s app/lib/ ecj jna RXTXcomm


%build
cd core/methods
ant
cd ..
ant
cd ../build
ant dist < /dev/null
tar -xf linux/%{name}-%{longversion}-linux.tgz


%install
cd build/%{name}-%{longversion}

mkdir -p %{buildroot}/%{_bindir}
cp -a arduino %{buildroot}/%{_bindir}/

mkdir -p %{buildroot}/%{_datadir}/%{name}
cp -a hardware lib libraries examples %{buildroot}/%{_datadir}/%{name}/
rm %{buildroot}/%{_datadir}/%{name}/lib/*.jar
rm -r %{buildroot}/%{_datadir}/%{name}/hardware/tools

mkdir -p %{buildroot}/%{_defaultdocdir}/%{name}-%{version}
cp -a reference %{buildroot}/%{_defaultdocdir}/%{name}-%{version}/
ln -s %{_defaultdocdir}/%{name}-%{version}/reference %{buildroot}/%{_datadir}/%{name}/reference

# Requested upstream in http://github.com/arduino/Arduino/pull/4:
find %{buildroot} -type f -iname *.jpg -or -iname *.java -or -iname *.pde -or -iname *.h -or -iname *.cpp -or -iname *.c -or -iname *.txt -or -iname makefile -or -iname key*.txt -or -iname pref*.txt | xargs chmod -x;

cp -a lib/core.jar lib/pde.jar %{buildroot}/%{_datadir}/%{name}/

mkdir -p %{buildroot}/%{_sysconfdir}/%{name}
mv %{buildroot}/%{_datadir}/%{name}/hardware/%{name}/boards.txt \
   %{buildroot}/%{_datadir}/%{name}/hardware/%{name}/programmers.txt \
   %{buildroot}/%{_sysconfdir}/%{name}/
ln -s %{_sysconfdir}/%{name}/boards.txt \
   %{buildroot}/%{_datadir}/%{name}/hardware/%{name}/boards.txt
ln -s %{_sysconfdir}/%{name}/programmers.txt \
   %{buildroot}/%{_datadir}/%{name}/hardware/%{name}/programmers.txt

mkdir -p %{buildroot}/%{_mandir}/man1
cp -p ../linux/%{name}.1 %{buildroot}/%{_mandir}/man1/

desktop-file-install --dir=%{buildroot}%{_datadir}/applications ../linux/%{name}.desktop

for dir in ../linux/icons/*; do
    size=`basename $dir`
    mkdir -p %{buildroot}/%{_datadir}/icons/hicolor/$size/apps
    cp $dir/%{name}.png %{buildroot}/%{_datadir}/icons/hicolor/$size/apps/
done

mkdir -p %{buildroot}/usr/lib
cp -a ../linux/%{name}-add-groups %{buildroot}/usr/lib

mkdir -p %{buildroot}/%{_datadir}/polkit-1/actions
cp -a ../linux/cc.arduino.add-groups.policy %{buildroot}/%{_datadir}/polkit-1/actions

%clean
rm -rf %{buildroot}


%files
%doc license.txt readme.txt todo.txt
%{_bindir}/*
%{_datadir}/%{name}/*.jar
%{_datadir}/%{name}/lib/
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/polkit-1/actions/cc.arduino.add-groups.policy
/usr/lib/%{name}-add-groups
%{_mandir}/man1/%{name}.1.xz
%{_datadir}/%{name}/reference


%files -n %{name}-core
%doc license.txt readme.txt todo.txt
%config(noreplace) %{_sysconfdir}/%{name}/boards.txt
%config(noreplace) %{_sysconfdir}/%{name}/programmers.txt
%{_datadir}/%{name}/examples/
%{_datadir}/%{name}/hardware/
%{_datadir}/%{name}/libraries/


%files -n %{name}-doc
%{_defaultdocdir}/%{name}-%{version}/
