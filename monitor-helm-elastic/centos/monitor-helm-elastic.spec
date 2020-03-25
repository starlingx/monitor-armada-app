%global sha 2bd7616ceddbdf2eee88965e2028ee37d304c79c
%global helm_folder  /usr/lib/helm
%global helmchart_version 0.1.0
%global _default_patch_flags --no-backup-if-mismatch --prefix=/tmp/junk

Summary: Monitor-Helm-Elastic charts
Name: monitor-helm-elastic
Version: 1.0
Release: %{tis_patch_ver}%{?_tis_dist}
License: Apache-2.0
Group: base
Packager: Wind River <info@windriver.com>
URL: https://github.com/elastic/helm-charts/

Source0: helm-charts-elastic-%{sha}.tar.gz
Source1: repositories.yaml
Source2: index.yaml

BuildArch:     noarch

Patch01: 0001-add-makefile.patch
Patch02: 0002-Add-compatibility-for-k8s-1.16.patch
Patch03: 0003-use-oss-image.patch
Patch04: 0004-Update-to-Elastic-7.4.0-Release.patch
Patch05: 0005-set-initial-masters-to-master-0.patch
Patch06: 0006-readiness-probe-enhancements.patch

BuildRequires: helm

%description
Monitor Helm elasticsearch charts

%prep
%setup -n helm-charts-elastic
%patch01 -p1
%patch02 -p1
%patch03 -p1
%patch04 -p1
%patch05 -p1
%patch06 -p1

%build
# initialize helm and build the toolkit
# helm init --client-only does not work if there is no networking
# The following commands do essentially the same as: helm init
%define helm_home %{getenv:HOME}/.helm
mkdir %{helm_home}
mkdir %{helm_home}/repository
mkdir %{helm_home}/repository/cache
mkdir %{helm_home}/repository/local
mkdir %{helm_home}/plugins
mkdir %{helm_home}/starters
mkdir %{helm_home}/cache
mkdir %{helm_home}/cache/archive

# Stage a repository file that only has a local repo
cp %{SOURCE1} %{helm_home}/repository/repositories.yaml

# Stage a local repo index that can be updated by the build
cp %{SOURCE2} %{helm_home}/repository/local/index.yaml

# Host a server for the charts
helm serve --repo-path . &
helm repo rm local
helm repo add local http://localhost:8879/charts

# Create the tgz files
rm elasticsearch/Makefile
make elasticsearch

# terminate helm server (the last backgrounded task)
kill %1

%install
install -d -m 755 ${RPM_BUILD_ROOT}%{helm_folder}
install -p -D -m 755 *.tgz ${RPM_BUILD_ROOT}%{helm_folder}

%files
%defattr(-,root,root,-)
%{helm_folder}/*
