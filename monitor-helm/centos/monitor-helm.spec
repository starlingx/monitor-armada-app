%global sha 92b6289ae93816717a8453cfe62bad51cbdb8ad0
%global helm_folder  /usr/lib/helm
%global helmchart_version 0.1.0
%global _default_patch_flags --no-backup-if-mismatch --prefix=/tmp/junk

Summary: Monitor-Helm charts
Name: monitor-helm
Version: 1.0
Release: %{tis_patch_ver}%{?_tis_dist}
License: Apache-2.0
Group: base
Packager: Wind River <info@windriver.com>
URL: https://github.com/helm/charts/

Source0: helm-charts-%{sha}.tar.gz
Source1: repositories.yaml
Source2: index.yaml

BuildArch:     noarch

Patch01: 0001-Add-Makefile-for-helm-charts.patch
Patch02: 0002-kibana-workaround-checksum-for-configmap.yaml.patch
Patch03: 0003-helm-chart-changes-for-stx-monitor.patch
Patch04: 0004-ipv6-helm-chart-changes.patch
Patch05: 0005-decouple-config.patch
Patch06: 0006-add-system-info.patch
Patch07: 0007-three-masters.patch
Patch08: 0008-Update-stx-monitor-for-kubernetes-API-1.16.patch
Patch09: 0009-add-curator-as-of-2019-10-10.patch
Patch10: 0010-Update-kube-state-metrics-1.8.0-to-commit-09daf19.patch
Patch11: 0011-update-init-container-env-to-include-node-name.patch 
Patch12: 0012-Add-imagePullSecrets.patch

BuildRequires: helm

%description
Monitor Helm charts

%prep
%setup -n helm-charts
%patch01 -p1
%patch02 -p1
%patch03 -p1
%patch04 -p1
%patch05 -p1
%patch06 -p1
%patch07 -p1
%patch08 -p1
%patch09 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1

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
cd stable
make filebeat
make metricbeat
make kube-state-metrics
make kibana
make nginx-ingress
make logstash
make elasticsearch-curator

# terminate helm server (the last backgrounded task)
kill %1

%install
install -d -m 755 ${RPM_BUILD_ROOT}%{helm_folder}
install -p -D -m 755 stable/*.tgz ${RPM_BUILD_ROOT}%{helm_folder}

%files
%defattr(-,root,root,-)
%{helm_folder}/*
