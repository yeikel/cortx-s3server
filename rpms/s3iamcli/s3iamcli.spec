# build number
%define build_num  %( test -n "$build_number" && echo "$build_number" || echo 1 )

%global py_ver 3.6

# pybasever without the dot:
%global py_short_ver 36

# XXX For strange reason setup.py uses /usr/lib
# but %{_libdir} resolves to /usr/lib64 with python3.6
#%global py36_sitelib %{_libdir}/python%{py_ver}
%global py36_sitelib /usr/lib/python%{py_ver}/site-packages

Name:       s3iamcli
Version:    %{_s3iamcli_version}
Release:    %{build_num}_%{_s3iamcli_git_ver}
Summary:    Seagate S3 IAM CLI.

Group:      Development/Tools
License:    Seagate
URL:        http://gerrit.mero.colo.seagate.com:8080/s3server
Source0:    %{name}-%{version}-%{_s3iamcli_git_ver}.tar.gz

BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix:     %{_prefix}
BuildArch:  noarch
Vendor:     Seagate

BuildRequires:  python3-rpm-macros
BuildRequires:  python%{py_short_ver}
BuildRequires:  python%{py_short_ver}-devel
%if 0%{?s3_with_python36_ver8:1}
BuildRequires:  python3-setuptools
%else
BuildRequires:  python%{py_short_ver}-setuptools
%endif

Requires:  python%{py_short_ver}
%if 0%{?s3_with_python36_ver8:1}
Requires:  python3-pyyaml
Requires:  python3-xmltodict >= 0.9.0
Requires:  python3-jmespath >= 0.7.1
Requires:  python3-botocore >= 1.5.0
Requires:  python3-s3transfer >= 0.1.10
Requires:  python3-boto3 >= 1.4.6
%else
Requires:  python%{py_short_ver}-yaml
Requires:  python%{py_short_ver}-xmltodict >= 0.9.0
Requires:  python%{py_short_ver}-jmespath >= 0.7.1
Requires:  python%{py_short_ver}-botocore >= 1.5.0
Requires:  python%{py_short_ver}-s3transfer >= 0.1.10
Requires:  python%{py_short_ver}-boto3 >= 1.4.6
%endif

%description
Seagate S3 IAM CLI

%package        devel
Summary:        Development files for %{name}
Group:          Development/Tools

BuildRequires:  python3-rpm-macros
BuildRequires:  python%{py_short_ver}
BuildRequires:  python%{py_short_ver}-devel
%if 0%{?s3_with_python36_ver8:1}
BuildRequires:  python3-setuptools
%else
BuildRequires:  python%{py_short_ver}-setuptools
%endif

Requires:  python%{py_short_ver}
%if 0%{?s3_with_python36_ver8:1}
Requires:  python3-pyyaml
Requires:  python3-xmltodict >= 0.9.0
Requires:  python3-jmespath >= 0.7.1
Requires:  python3-botocore >= 1.5.0
Requires:  python3-s3transfer >= 0.1.10
Requires:  python3-boto3 >= 1.4.6
%else
Requires:  python%{py_short_ver}-yaml
Requires:  python%{py_short_ver}-xmltodict >= 0.9.0
Requires:  python%{py_short_ver}-jmespath >= 0.7.1
Requires:  python%{py_short_ver}-botocore >= 1.5.0
Requires:  python%{py_short_ver}-s3transfer >= 0.1.10
Requires:  python%{py_short_ver}-boto3 >= 1.4.6
%endif

%description    devel
This package contains development files for %{name}.


%prep
%setup -n %{name}-%{version}-%{_s3iamcli_git_ver}

%build
mkdir -p %{_builddir}/%{name}-%{version}-%{_s3iamcli_git_ver}/build/lib/%{name}
cd %{name}
python%{py_ver} -m compileall -b *.py
cp  *.pyc %{_builddir}/%{name}-%{version}-%{_s3iamcli_git_ver}/build/lib/%{name}
echo "build complete"

%install
cd %{_builddir}/%{name}-%{version}-%{_s3iamcli_git_ver}
python%{py_ver} setup.py install --no-compile --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_bindir}/%{name}
%{py36_sitelib}/%{name}/config/*.yaml
%{py36_sitelib}/%{name}-%{version}-py?.?.egg-info
%{py36_sitelib}/%{name}/*.pyc
%exclude %{py36_sitelib}/%{name}/__pycache__/*
%exclude %{py36_sitelib}/%{name}/*.py
%exclude %{py36_sitelib}/%{name}/%{name}
%defattr(-,root,root)

%files devel
%{_bindir}/%{name}
%{py36_sitelib}/%{name}/*.py
%{py36_sitelib}/%{name}/config/*.yaml
%{py36_sitelib}/%{name}-%{version}-py?.?.egg-info
%exclude %{py36_sitelib}/%{name}/*.pyc
%exclude %{py36_sitelib}/%{name}/__pycache__/*
%exclude %{py36_sitelib}/%{name}/%{name}
%defattr(-,root,root)
