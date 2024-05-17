# Re-packaging the Adobe Reader RPM
**(for newer Fedora and RHEL >=8 releases)**

Adobe Reader for Linux is no longer supported by Adobe. Acrobat Reader 9.5.5
was the last version released back in April, 2013. 

Unfortunately trying to install `AdbeRdr9.5.5-1_i486linux_enu.rpm` on newer
Fedora or RHEL releases results in unsatisfied dependencies :

```
$ sudo dnf install ./AdbeRdr9.5.5-1_i486linux_enu.rpm
Error: 
 Problem: conflicting requests
  - nothing provides /bin/basename needed by AdobeReader_enu-9.5.5-1.i486
  - nothing provides libidn.so.11 needed by AdobeReader_enu-9.5.5-1.i486
  - nothing provides libpangox-1.0.so.0 needed by AdobeReader_enu-9.5.5-1.i486
```

## Bug fixes and enhancements
The new AdobeReader binary RPM that is generated from the instructions in
the following sections has a number of fixes and enhancements compared to
the original RPM:
- Missing `/bin/basename` requires dependency has been replaced with
**coreutils**.
- Missing `libidn.so.11` and `libpangox-1.0.so.0` are bundled in the new RPM
and located in `/opt/Adobe/Reader9/Reader/intellinux/lib/`.
  + The missing `libidn.so.11` is extracted from a CentOS 8 **libidn** i686
  RPM (`libidn-1.34-5.el8.i686.rpm`). Although `libidn.so.11` is not
  strictly required to have been included in the new AdobeReader RPM for
  RHEL 8, the new RPM will also be compatible with both RHEL 9 and Fedora.
  + The missing `libpangox-1.0.so.0` is extracted from a Fedora 31
  **pangox-compat** i686 RPM (`pangox-compat-0.0.2-15.fc31.i686.rpm`).
  **pangox-compat** RPM is used because the main **pango** RPM hasn't provided
  the obsolete libpangox library since Fedora 17.
- _Recommends_ dependencies added for packages that suppress Gtk-Message
runtime warnings. (Note: any _Recommends_ dependency which can no longer be
satisfied on a newer Fedora or RHEL release because the i686 package no
longer exists is automatically ignored, so unfortunately may have to live
with some runtime warnings)
- Filtered automatically generated requires and provides for bundled library
files so that only requires dependencies for external libraries are kept.
`/opt/Adobe/Reader9/Reader/intellinux/lib/` where the bundled library
files are installed is exclusive to the AdobeReader RPM, so should not be
used to satisfy the dependencies of any other RPM.
- Removed Netscape NPAPI based PDF plug-in as it is not supported by any
modern web-browser.
- Use `/usr/share/bash-completion/completions/` directory instead of legacy
`/etc/bash_completion.d/` for the symlink to the `acroread_tab` file.
- Renames `_filedir` function to `_acroread_filedir` in the `acroread_tab`
file to avoid potential name clash issues.
- Clear the execstack flag from the `libcrypto.so.0.9.8` and `libsccore.so`
bundled library files rather than rely on an old execstack exception SElinux
policy for `acroread`.
[Fedora Bugzilla# 630217](https://bugzilla.redhat.com/show_bug.cgi?id=630217),
SElinux error report states there is no reason `acroread` should be attempting
to make its stack executable as it is a potential security issue. The
suggestion from that bug report is used to clear the execstack flag from the
bundled library files that have it set.
- The original RPM in its %post scriptlet uses `xdg-desktop-icon`,
`xdg-desktop-menu`, `xdg-icon-resource` and `xdg-mime`to install the
following files :
  + `/root/Desktop/AdobeReader.desktop`
  + `/usr/local/share/applications/AdobeReader.desktop`
  + `/usr/local/share/applications/mimeinfo.cache`
  + `/usr/local/share/applications/defaults.list`
  + `/usr/share/icons/hicolor/*x*/apps/*.png`
  + `/usr/share/icons/hicolor/*x*/mimetype/application-*.png`
  + `/usr/share/mime/packages/AdobeReader.xml`

  The above files are not "owned" by the original RPM, e.g. `rpm -ql AdobeReader_enu`
does not list any of those files.

  Instead, the new RPM creates symlinks that are "owned" by the new RPM using the
%ghost directive and nothing is installed under either `/root/Desktop/` or
`/usr/local/share/applications/` directories.
- Has option to not include problematic Internet Access Plug-in (EFS.api)
in the RPM that is built. See top of
[AdobeReader.spec](https://github.com/eait-cups-printing/adobe-reader-rpm/blob/main/AdobeReader.spec)
file for more details.

## Prerequisites

Install prerequisite packages with:
```
sudo dnf install rpmdevtools git execstack
```

## Create directories for RPM building under your home directory

To build RPMs with an unprivileged user, create a directory structure under
your home directory with the following command :
```
rpmdev-setuptree
```
Which results in the following directory structure under your home
directory:
```
rpmbuild/
├── BUILD/
├── RPMS/
├── SOURCES/
├── SPECS/
└── SRPMS/
```

## Fetch files, extract library files and copy to rpmbuild sub-directories

```
git clone https://github.com/eait-cups-printing/adobe-reader-rpm.git
cd adobe-reader-rpm/
cp -p AdobeReader.spec ~/rpmbuild/SPECS/

curl -O ftp://ftp.adobe.com/pub/adobe/reader/unix/9.x/9.5.5/enu/AdbeRdr9.5.5-1_i486linux_enu.rpm
curl -O https://archives.fedoraproject.org/pub/archive/fedora/linux/releases/31/Everything/x86_64/os/Packages/p/pangox-compat-0.0.2-15.fc31.i686.rpm
curl -O https://vault.centos.org/8.5.2111/AppStream/x86_64/os/Packages/libidn-1.34-5.el8.i686.rpm

cp -p AdbeRdr9.5.5-1_i486linux_enu.rpm ~/rpmbuild/SOURCES/

rpm2cpio libidn-1.34-5.el8.i686.rpm | cpio -idm
cp -p usr/lib/libidn.so.11.6.18 ~/rpmbuild/SOURCES/

rpm2cpio pangox-compat-0.0.2-15.fc31.i686.rpm | cpio -idm
cp -p usr/lib/libpangox-1.0.so.0.0.0 ~/rpmbuild/SOURCES/
```

## Build the new AdobeReader-9.5.5-2.i686.rpm binary RPM

```
cd ~/rpmbuild/SPECS/
rpmbuild --target i686 -ba AdobeReader.spec
```

## Install the new AdobeReader-9.5.5-2.i686.rpm binary RPM

```
sudo dnf install ~/rpmbuild/RPMS/i686/AdobeReader-9.5.5-2.i686.rpm
```

If you encounter a "nothing provides libgdk_pixbuf_xlib-2.0.so.0" error,
then you will need to enable a PowerTools/CRB "*CodeReady Builder*"
repository which contains the missing **gdk-pixbuf2-xlib** i686 RPM:

#### CentOS 9 Stream, Alma Linux 9, Rocky Linux 9
```
sudo dnf config-manager --set-enabled crb
```

#### RedHat Enterprise Linux 9
```
sudo dnf config-manager --enable codeready-builder-for-rhel-9-x86_64-rpms
```

#### CentOS 8 Stream, Alma Linux 8, Rocky Linux 8
```
sudo dnf config-manager --set-enabled powertools
```

#### RedHat Enterprise Linux 8
```
sudo dnf config-manager --enable codeready-builder-for-rhel-8-x86_64-rpms
```

# cups-filters pdf2ps filter
[cups-filters 1.x](https://github.com/OpenPrinting/cups-filters/tree/1.x)
includes a `pdf2ps` filter that can be configured at build time to use
Adobe Reader to convert PDF to PostScript with the `--with-pdftops=acroread`
configure switch.

Similarily with cups-filters 2.x, [libppd](https://github.com/OpenPrinting/libppd)
can be configured with the `--with-pdftops=acroread` configure switch.

Alternatively, the following can be done on a per printer basis to use acroread
for the PDF to PostScript conversion:
```
lpadmin -p printer -o pdftops-renderer-default=acroread
```

and similarily the following can be done to remove it:
```
lpadmin -p printer -R pdftops-renderer-default
```

Adobe Reader seems to have fewer problems ingesting PDFs sent to the
print server and the generated PostScript has few problems with clone
PostScript interpreters on printers.
