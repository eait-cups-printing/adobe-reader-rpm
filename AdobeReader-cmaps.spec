Name:    AdobeReader-cmaps
Version: 9.5.5
Release: 1
Summary: CMap files for Adobe Reader
License: Commercial
Url:     http://www.adobe.com
Source0: ftp://ftp.adobe.com/pub/adobe/reader/unix/9.x/9.1/misc/FontPack910_chs_i486-linux.tar.bz2
Source1: ftp://ftp.adobe.com/pub/adobe/reader/unix/9.x/9.1/misc/FontPack910_cht_i486-linux.tar.bz2
Source2: ftp://ftp.adobe.com/pub/adobe/reader/unix/9.x/9.1/misc/FontPack910_jpn_i486-linux.tar.bz2
Source3: ftp://ftp.adobe.com/pub/adobe/reader/unix/9.x/9.1/misc/FontPack910_kor_i486-linux.tar.bz2
#Source4: ftp://ftp.adobe.com/pub/adobe/reader/unix/9.x/9.1/misc/FontPack910_xtd_i486-linux.tar.bz2

NoSource: 0
NoSource: 1
NoSource: 2
NoSource: 3

BuildArch: noarch

BuildRequires: fdupes

Provides: locale(AdobeReader:zh;jp;ko)

%description
Character Map files for Adobe Reader which are needed for Chinese, Japanese
and Korean.

%package -n AdobeReader-fonts-zh_CN
Requires: AdobeReader
Requires: AdobeReader-cmaps
Provides: locale(AdobeReader:zh)
Summary: Simplified Chinese fonts for Adobe Reader

%description -n AdobeReader-fonts-zh_CN
Simplified Chinese fonts for Adobe Reader

%package -n AdobeReader-fonts-zh_TW
Requires: AdobeReader
Requires: AdobeReader-cmaps
Provides: locale(AdobeReader:zh)
Summary: Traditional Chinese fonts for Adobe Reader

%description -n AdobeReader-fonts-zh_TW
Traditional Chinese fonts for Adobe Reader

%package -n AdobeReader-fonts-ja
Requires: AdobeReader
Requires: AdobeReader-cmaps
Provides: locale(AdobeReader:ja)
Summary: Japanese fonts for Adobe Reader

%description -n AdobeReader-fonts-ja
Japanese fonts for Adobe Reader

%package -n AdobeReader-fonts-ko
Requires: AdobeReader
Requires: AdobeReader-cmaps
Provides: locale(AdobeReader:ko)
Summary: Korean fonts for Adobe Reader

%description -n AdobeReader-fonts-ko
Korean fonts for Adobe Reader


%prep
# unpack the Source into a suitable directory
# there is the top-level directory "AdobeReader" in the source archive
%setup -T -c AdobeReader -n AdobeReader -a 0 -a 1 -a 2 -a 3 

%build
# there is nothing to build as this package is a binary-only package

%install
# install the extra font packages:
mkdir -p %{buildroot}/opt
for i in CHSKIT/*TAR CHTKIT/*TAR JPNKIT/*TAR KORKIT/*TAR
do
    tar xvf $i -C %{buildroot}/opt 
done
# Delete files which are already in the main AdobeReader package:
rm -f %{buildroot}/opt/Adobe/Reader9/Reader/intellinux/lib/libicudata.so.36.0
rm -f %{buildroot}/opt/Adobe/Reader9/Resource/CMap/Identity-H
rm -f %{buildroot}/opt/Adobe/Reader9/Resource/CMap/Identity-V

%fdupes %{buildroot}

%clean

%files -n AdobeReader-cmaps
%defattr(-,root,root)
%doc CHSKIT/LICREAD.TXT
%dir /opt/Adobe/
%dir /opt/Adobe/Reader9/
%dir /opt/Adobe/Reader9/Resource/
%dir /opt/Adobe/Reader9/Resource/CMap/
# the Identity* CMaps area already in the main AdobeReader package:
/opt/Adobe/Reader9/Resource/CMap/[0-9A-HJ-Z]*

%files -n AdobeReader-fonts-zh_CN
%defattr(-,root,root)
%doc CHSKIT/LICREAD.TXT
%dir /opt/Adobe/
%dir /opt/Adobe/Reader9/
%dir /opt/Adobe/Reader9/Resource/
%dir /opt/Adobe/Reader9/Resource/CIDFont/
/opt/Adobe/Reader9/Resource/CIDFont/AdobeSongStd*.otf
/opt/Adobe/Reader9/Resource/CIDFont/AdobeHeitiStd*.otf

%files -n AdobeReader-fonts-zh_TW
%defattr(-,root,root)
%doc CHTKIT/LICREAD.TXT
%dir /opt/Adobe/
%dir /opt/Adobe/Reader9/
%dir /opt/Adobe/Reader9/Resource/
%dir /opt/Adobe/Reader9/Resource/CIDFont/
/opt/Adobe/Reader9/Resource/CIDFont/AdobeMingStd*.otf

%files -n AdobeReader-fonts-ja
%defattr(-,root,root)
%doc JPNKIT/LICREAD.TXT
%dir /opt/Adobe/
%dir /opt/Adobe/Reader9/
%dir /opt/Adobe/Reader9/Resource/
%dir /opt/Adobe/Reader9/Resource/CIDFont/
/opt/Adobe/Reader9/Resource/CIDFont/KozMin*.otf

%files -n AdobeReader-fonts-ko
%defattr(-,root,root)
%doc KORKIT/LICREAD.TXT
%dir /opt/Adobe/
%dir /opt/Adobe/Reader9/
%dir /opt/Adobe/Reader9/Resource/
%dir /opt/Adobe/Reader9/Resource/CIDFont/
/opt/Adobe/Reader9/Resource/CIDFont/AdobeMyungjoStd*.otf

