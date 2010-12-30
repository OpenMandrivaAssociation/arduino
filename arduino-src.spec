
%define name	arduino
%define version	0021
%define distsuffix edm

Summary:	Arduino prototyping IDE
Summary(ru):	IDE для прототипирования на основе контроллеров Arduino
Name:		%{name}
Version:	%{version}
Release:	%mkrel 2
License:	GPLv2+
Group:		Applications/Development
URL:		http://arduino.cc
Source:		http://files.arduino.cc/downloads/%{name}-%{version}-src.tar.gz
Source1:        suexec_arduino-3.tar.bz2
Source2:        arduino_make
Source3:	reference.zip
BuildRoot:	%{_tmppath}/%{name}%{version}-root
Requires:	cross-avr-binutils >= 2.20
Requires:	cross-avr-compat-gcc == 4.3.2
Requires:	cross-avr-compat-gcc-c++ == 4.3.2
Requires:	avr-libc >= 1.6.8
Requires:	rxtx-nolock
Requires:	avrdude
Requires:	uucp
Requires:	java-1.6.0-sun
BuildRequires:  java-1.6.0-sun-devel
BuildRequires:  ant
BuildRequires:  ant-apache-regexp
BuildRequires:  xml-commons-jaxp-1.3-apis
BuildRequires:  crimson
#Conflicts:	java-1.5.0-gcj
#Conflicts:	java-1.6.0-openjdk


%description
Arduino is an open-source electronics prototyping platform based on flexible, 
easy-to-use hardware and software. It's intended for artists, designers, hobbyists, 
and anyone interested in creating interactive objects or environments. 
This packet contains the Arduino IDE and sample programs.

%description -l ru
Arduino - это open-source платформа для прототипирования электроники, созданная 
на основе гибкого и простого в использовании аппаратного и программного обеспечения.
Предназначена как для разработчиков, так и для любителей, интересующихся созданием
интерактивнных объектов и окружений.
Пакет содержит среду разработки Arduino IDE и примеры программ.

%prep
rm -rf ${RPM_BUILD_DIR}/%{name}-%{version}
mkdir -p ${RPM_BUILD_DIR}
cd ${RPM_BUILD_DIR}
tar xf ${RPM_SOURCE_DIR}/%{name}-%{version}-src.tar.gz
cd %{name}-%{version}
tar xf ${RPM_SOURCE_DIR}/suexec_arduino-3.tar.bz2
cd ${RPM_BUILD_DIR}/%{name}-%{version}/build
echo %{version} > linux/dist/lib/version.txt
#echo %{version} > linux/work/lib/version.txt
echo %{version} > ../app/lib/version.txt
cp -f ${RPM_SOURCE_DIR}/reference.zip ${RPM_BUILD_DIR}/%{name}-%{version}/build/shared/

%build
rm -rf %{buildroot}
cd ${RPM_BUILD_DIR}/%{name}-%{version}/build
ant
echo '%{version}' > linux/work/lib/version.txt
cd ${RPM_BUILD_DIR}/%{name}-%{version}/suexec_arduino/
%ifarch %ix86
export CFLAGS="-m32"
%endif
%ifarch x86_64
export CFLAGS="-m64"
%endif
make 


%install
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}

install -m 755 ${RPM_BUILD_DIR}/%{name}-%{version}/suexec_arduino/suexec_arduino ${RPM_BUILD_ROOT}/usr/bin
install -m 755 ${RPM_SOURCE_DIR}/arduino_make ${RPM_BUILD_ROOT}/usr/bin

ln -s suexec_arduino ${RPM_BUILD_ROOT}/usr/bin/arduino

#poner arduino en /usr/lib/arduino_version
mkdir -p ${RPM_BUILD_ROOT}/usr/lib/arduino
cp -a ${RPM_BUILD_DIR}/arduino-%{version}/build/linux/work/* ${RPM_BUILD_ROOT}/usr/lib/arduino

#pushd ${RPM_BUILD_ROOT}/usr/lib/arduino
#unzip -o %{SOURCE3}
#popd

#mover documentacion
mkdir -p ${RPM_BUILD_ROOT}/%{_docdir}/
mv ${RPM_BUILD_ROOT}/usr/lib/arduino/reference ${RPM_BUILD_ROOT}/%{_docdir}/%{name}-%{version}

#script ejecucion
cp  ${RPM_BUILD_DIR}/%{name}-%{version}/suexec_arduino/arduino_anv ${RPM_BUILD_ROOT}/usr/lib/arduino 

#usar bibliotecas del sistema y no propias para que use las de la arquitectura correcta
rm ${RPM_BUILD_ROOT}/usr/lib/arduino/lib/RXTXcomm.jar 

#crear link a librxtxSerial de la arquitectura correcta.
rm ${RPM_BUILD_ROOT}/usr/lib/arduino/lib/librxtxSerial.so 

#desktop
mkdir -p ${RPM_BUILD_ROOT}/usr/share/applications/
mkdir -p ${RPM_BUILD_ROOT}%{_iconsdir}/hicolor/

cp ${RPM_BUILD_DIR}/%{name}-%{version}/suexec_arduino/arduino.desktop ${RPM_BUILD_ROOT}/usr/share/applications/
cp -r ${RPM_BUILD_DIR}/%{name}-%{version}/suexec_arduino/icons/* ${RPM_BUILD_ROOT}%{_iconsdir}/hicolor/


%clean
rm -rf %{buildroot}

%files 
%attr(2755,root,dialout) %{_bindir}/suexec_arduino
%{_bindir}/arduino
%{_bindir}/arduino_make
/usr/lib/arduino/*
%{_datadir}/applications/*
%{_iconsdir}/hicolor/*
%{_docdir}/%{name}-%{version}

