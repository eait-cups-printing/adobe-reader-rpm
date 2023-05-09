# Turn off missing build-id warnings
%global _build_id_links none

# Turn off generating debug package
%global debug_package %{nil}

# Turn off BRP scripts which strip binaries
%global __os_install_post %{nil}

# Set delete_efs_plugin to 1 to remove Internet Access Plug-in (EFS.api) from
# this RPM if :
#  - you are concerned about acroread accessing the Internet,
#  - EFS.api is causing high CPU usage if it can't access the Internet, or
#  - EFS.api is causing acroread to die after around 15 seconds.
%define delete_efs_plugin 0

Name:    AdobeReader
Version: 9.5.5
Release: 2
Summary: Adobe Reader, an application to easily view, print and collaborate on PDF files.
License: Commercial
URL:     http://www.adobe.com
Source0: ftp://ftp.adobe.com/pub/adobe/reader/unix/9.x/9.5.5/enu/AdbeRdr9.5.5-1_i486linux_enu.rpm
Source1: libidn.so.11.6.18
Source2: libpangox-1.0.so.0.0.0

# Use rpmbuild --target i686 to satisfy the exclusive architecture
ExclusiveArch: %ix86

BuildRequires: execstack

Requires: coreutils

# 'Unable to locate theme engine in module_path: "adwaita"' acroread runtime
# Gtk-Message warning is suppressed with adwaita-gtk2-theme.i686
Recommends: adwaita-gtk2-theme(x86-32)

# 'Failed to load module "canberra-gtk-module"' acroread runtime Gtk-Message
# warning is suppressed with libcanberra-gtk2.i686
Recommends: libcanberra-gtk2(x86-32)

# 'Failed to load module "pk-gtk-module"' acroread runtime Gtk-Message warning
# is suppressed with PackageKit-gtk3-module.i686
Recommends: PackageKit-gtk3-module(x86-32)

Provides: %{_bindir}/acroread

Provides: AdobeReader_enu = %{version}-%{release}
Obsoletes: AdobeReader_enu <= 9.5.5-1

# filter out auto-requires for libs bundled with this package
# filter out auto-provides for libs bundled with this package
%{?filter_setup:
%filter_from_requires /libACE\.so.*/d
%filter_from_requires /libAdobeXMP\.so.*/d
%filter_from_requires /libAGM\.so.*/d
%filter_from_requires /libAXE8SharedExpat\.so.*/d
%filter_from_requires /libAXSLE\.so.*/d
%filter_from_requires /libBIB\.so.*/d
%filter_from_requires /libBIBUtils\.so.*/d
%filter_from_requires /libCoolType\.so.*/d
%filter_from_requires /libJP2K\.so/d
%filter_from_requires /libResAccess\.so/d
%filter_from_requires /libWRServices\.so/d
%filter_from_requires /libadobelinguistic\.so/d
%filter_from_requires /libcrypto\.so\.0\.9\.8/d
%filter_from_requires /libcurl\.so\.3/d
%filter_from_requires /libeggtrayicon\.so/d
%filter_from_requires /libextendscript\.so/d
%filter_from_requires /libicucnv\.so\.36/d
%filter_from_requires /libicudata\.so\.36/d
%filter_from_requires /libicui18n\.so\.36/d
%filter_from_requires /libicuuc.so\.36/d
%filter_from_requires /libidn\.so\.11/d
%filter_from_requires /libpangox-1\.0\.so\.0/d
%filter_from_requires /libsccore\.so/d
%filter_from_requires /libssl\.so\.0\.9\.8/d
%filter_from_provides /lib.*\.so.*/d
%filter_setup
}

%description
Adobe Reader software is the global standard for electronic document sharing.
It is the only PDF file viewer that can open and interact with all PDF
documents. Use Adobe Reader to view, search, digitally sign, verify, print,
and collaborate on Adobe PDF files.

%prep
%setup -T -c
rpm2cpio '%{SOURCE0}' | cpio -idm

%build
# rename _filedir function to avoid name clash which can break bash-completion
sed -i 's/_filedir/_acroread_filedir/' opt/Adobe/Reader9/Resource/Shell/acroread_tab

# bash-completion does not require acroread_tab file to be executable
chmod a-x opt/Adobe/Reader9/Resource/Shell/acroread_tab

# Executable stack memory is a potential security problem, clear execstack
# flag from library files that have it set
execstack -c opt/Adobe/Reader9/Reader/intellinux/lib/libcrypto.so.0.9.8
execstack -c opt/Adobe/Reader9/Reader/intellinux/lib/libsccore.so

# Remove Netscape NPAPI based PDF plug-in as not supported by modern web-browsers
rm -rf opt/Adobe/Reader9/Browser

%if %{delete_efs_plugin}
# delete Internet Access Plug-in (EFS.api)
rm opt/Adobe/Reader9/Reader/intellinux/plug_ins/EFS.api
%endif

cp -p opt/Adobe/Reader9/Reader/Legal/en_US/License.txt .

%install
cp -a opt %{buildroot}

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/mime/packages
mkdir -p %{buildroot}%{_datadir}/bash-completion/completions

# create temporary placeholders with touch for absolute path symlinks
touch %{buildroot}%{_bindir}/acroread
touch %{buildroot}%{_mandir}/man1/acroread.1.gz
touch %{buildroot}%{_datadir}/applications/AdobeReader.desktop
touch %{buildroot}%{_datadir}/mime/packages/AdobeReader.xml
touch %{buildroot}%{_datadir}/bash-completion/completions/acroread

for i in 16 22 24 32 36 48 64 96 128 192; do
  mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps
  touch %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/AdobeReader9.png
  touch %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/adobe.pdf.png
  touch %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/vnd.fdf.png
  touch %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/vnd.adobe.pdx.png
  touch %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/vnd.adobe.xdp+xml.png
  touch %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/vnd.adobe.xfdf.png

  mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/mimetypes
  touch %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/mimetypes/application-pdf.png
  touch %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/mimetypes/application-fdf.png
  touch %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/mimetypes/application-pdx.png
  touch %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/mimetypes/application-xdp+xml.png
  touch %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/mimetypes/application-xfdf.png
done

# libidn.so.11.6.18
cp -p '%{SOURCE1}' %{buildroot}/opt/Adobe/Reader9/Reader/intellinux/lib
ln -s libidn.so.11.6.18 %{buildroot}/opt/Adobe/Reader9/Reader/intellinux/lib/libidn.so.11.6

# libpangox-1.0.so.0.0.0
cp -p '%{SOURCE2}' %{buildroot}/opt/Adobe/Reader9/Reader/intellinux/lib
ln -s libpangox-1.0.so.0.0.0 %{buildroot}/opt/Adobe/Reader9/Reader/intellinux/lib/libpangox-1.0.so.0

%post
ln -sf /opt/Adobe/Reader9/bin/acroread %{_bindir}/acroread
ln -sf /opt/Adobe/Reader9/Resource/Shell/acroread.1.gz %{_mandir}/man1/acroread.1.gz
ln -sf /opt/Adobe/Reader9/Resource/Shell/acroread_tab %{_datadir}/bash-completion/completions/acroread
ln -sf /opt/Adobe/Reader9/Resource/Support/AdobeReader.desktop %{_datadir}/applications/AdobeReader.desktop
ln -sf /opt/Adobe/Reader9/Resource/Support/AdobeReader.xml %{_datadir}/mime/packages/AdobeReader.xml

for i in 16 22 24 32 36 48 64 96 128 192; do
  ln -sf /opt/Adobe/Reader9/Resource/Icons/${i}x${i}/AdobeReader9.png %{_datadir}/icons/hicolor/${i}x${i}/apps/AdobeReader9.png
  ln -sf /opt/Adobe/Reader9/Resource/Icons/${i}x${i}/adobe.pdf.png %{_datadir}/icons/hicolor/${i}x${i}/apps/adobe.pdf.png
  ln -sf /opt/Adobe/Reader9/Resource/Icons/${i}x${i}/vnd.fdf.png %{_datadir}/icons/hicolor/${i}x${i}/apps/vnd.fdf.png
  ln -sf /opt/Adobe/Reader9/Resource/Icons/${i}x${i}/vnd.adobe.pdx.png %{_datadir}/icons/hicolor/${i}x${i}/apps/vnd.adobe.pdx.png
  ln -sf /opt/Adobe/Reader9/Resource/Icons/${i}x${i}/vnd.adobe.xdp+xml.png %{_datadir}/icons/hicolor/${i}x${i}/apps/vnd.adobe.xdp+xml.png
  ln -sf /opt/Adobe/Reader9/Resource/Icons/${i}x${i}/vnd.adobe.xfdf.png %{_datadir}/icons/hicolor/${i}x${i}/apps/vnd.adobe.xfdf.png

  ln -sf /opt/Adobe/Reader9/Resource/Icons/${i}x${i}/adobe.pdf.png  %{_datadir}/icons/hicolor/${i}x${i}/mimetypes/application-pdf.png
  ln -sf /opt/Adobe/Reader9/Resource/Icons/${i}x${i}/vnd.fdf.png %{_datadir}/icons/hicolor/${i}x${i}/mimetypes/application-fdf.png
  ln -sf /opt/Adobe/Reader9/Resource/Icons/${i}x${i}/vnd.adobe.pdx.png %{_datadir}/icons/hicolor/${i}x${i}/mimetypes/application-pdx.png
  ln -sf /opt/Adobe/Reader9/Resource/Icons/${i}x${i}/vnd.adobe.xdp+xml.png %{_datadir}/icons/hicolor/${i}x${i}/mimetypes/application-xdp+xml.png
  ln -sf /opt/Adobe/Reader9/Resource/Icons/${i}x${i}/vnd.adobe.xfdf.png %{_datadir}/icons/hicolor/${i}x${i}/mimetypes/application-xfdf.png
done

%files
%license License.txt
%ghost %{_bindir}/acroread
%ghost %{_mandir}/man1/acroread.1.gz
%ghost %{_datadir}/applications/AdobeReader.desktop
%ghost %{_datadir}/mime/packages/AdobeReader.xml
%ghost %{_datadir}/icons/hicolor/*/apps/*.png
%ghost %{_datadir}/icons/hicolor/*/mimetypes/*.png
%ghost %{_datadir}/bash-completion/completions/acroread
%dir %{_datadir}/bash-completion/completions
/opt/Adobe
