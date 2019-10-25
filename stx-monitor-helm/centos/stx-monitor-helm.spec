%global armada_folder  /usr/lib/armada
%global app_folder  /usr/lib/application

Summary: StarlingX Monitor Application Armada Helm Charts
Name: stx-monitor-helm
Version: 1.0
Release: %{tis_patch_ver}%{?_tis_dist}
License: Apache-2.0
Group: base
Packager: Wind River <info@windriver.com>
URL: unknown

Source0: %{name}-%{version}.tar.gz

BuildArch: noarch
BuildRequires: monitor-helm
BuildRequires: monitor-helm-elastic
Requires: monitor-helm
Requires: monitor-helm-elastic

%description
StarlingX Monitor Application Armada Helm Charts

%prep
%setup

%install
install -d -m 755 ${RPM_BUILD_ROOT}%{armada_folder}
install -p -D -m 755 manifests/*.yaml ${RPM_BUILD_ROOT}%{armada_folder}
install -d -m 755 ${RPM_BUILD_ROOT}%{app_folder}
install -p -D -m 755 files/metadata.yaml ${RPM_BUILD_ROOT}%{app_folder}

%files
%defattr(-,root,root,-)
%{armada_folder}/*
%{app_folder}/*
