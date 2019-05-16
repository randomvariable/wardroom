# kubernetes-common

#### Table of Contents

- [kubernetes-common](#kubernetes-common)
      - [Table of Contents](#table-of-contents)
  - [Description](#description)
  - [Setup](#setup)
    - [What kubernetes-common affects](#what-kubernetes-common-affects)
    - [Setup Requirements](#setup-requirements)
    - [Beginning with kubernetes-common](#beginning-with-kubernetes-common)
  - [Usage](#usage)
  - [Reference](#reference)
    - [Parameters](#parameters)
        - [Extended configuration blocks](#extended-configuration-blocks)
          - [`kubernetes_common_auditing`](#kubernetes_common_auditing)
          - [`kubernetes_common_encryption_provider`](#kubernetes_common_encryption_provider)
  - [Limitations](#limitations)

## Description

This role primarily controls the configuration of a Kubernetes cluster,
via Kubeadm. This role encodes some typical customisations via
it's variable interface.

## Setup

### What kubernetes-common affects

kubernetes-common creates the configuration that kubeadm will use to initialise
the cluster and allow more nodes to join it.

### Setup Requirements

This role requires the machine to have been made ready for bootstrapping,
running either Docker or containerd, and have the kubelet, kubeadm and
kubernetes-cni installed for the version that will be bootstrapped

### Beginning with kubernetes-common

The very basic steps needed for a user to get the module up and running. This can include setup steps, if necessary, or it can be an example of the most basic use of the module.

## Usage

This section is where you describe how to customize, configure, and do the fancy stuff with your module here. It's especially helpful if you include usage examples and code samples for doing things with your module.

## Reference

### Parameters

* `kubernetes_common_disable_swap`: Disables swap. Default: `True`
* `kubernetes_common_manage_etc_hosts`: Manage `/etc/hosts`. Default: `False`
* `kubernetes_common_api_fqdn`: The DNS name of the API server, typically a load balancer. Default: `k8s.example.com`
* `kubernetes_common_api_ip`: The common, load balancer IP of the API server. Default: `10.10.10.3`
* `kubernetes_common_cluster_tls_cipher_suites`: The TLS cipher suites that will be used for running Kubernetes. Default: `Mozilla Modern`.
* `kubernetes_common_feature_gates`: A dictionary of feature-gates with True or False to toggle them. Default: `{}`
* `kubernetes_common_profiling_enabled`: Enables profiling on the control plane components. Default: `False`

##### Extended configuration blocks

###### `kubernetes_common_auditing`

This block enables audit logging to file as well as enabling dynamic audit logging via webhooks.

```yaml
kubernetes_common_auditing:
  enabled: False # Switch to true to turn on this block.
```

No other configuration is needed to enable a default logging setup to
`/var/log/kubernetes/audit.log`

###### `kubernetes_common_encryption_provider`

```yaml
kubernetes_common_encryption_provider:
  enabled: False
```





kubernetes_common_feature_gates: {}
kubernetes_common_feature_gates_string: "{{ kubernetes_common_feature_gates | dict2items | map('format', '%s=%s', item.key, item.value) | join(',') }}"

kubernetes_common_profiling_enabled: False


kubernetes_common_auditing:
  enabled: False
  cluster_configuration:
    apiServer:
      extraArgs:
        audit-dynamic-configuration: "true"
        audit-log-path: /var/log/kubernetes/audit.log
        audit-log-maxsize: "256"
        audit-policy-file: "/etc/kubernetes/audit-policy.yaml"
        audit-log-maxbackup: "5"
        runtime-config: "auditregistration.k8s.io/v1alpha1=true"
      extraVolumes:
      - name: "audit-policy"
        hostPath: "/etc/kubernetes/audit-policy.yaml"
        mountPath: "/etc/kubernetes/audit-policy.yaml"
        readOnly: true
        pathType: FileOrCreate
      - name: "admission-control-config"
        hostPath: "/etc/kubernetes/admission-control-config.yaml"
        mountPath: "/etc/kubernetes/admission-control-config.yaml"
        readOnly: true
        pathType: FileOrCreate
      - name: "event-rate-limit"
        hostPath: "/etc/kubernetes/event-rate-limit.yaml"
        mountPath: "/etc/kubernetes/event-rate-limit.yaml"
        readOnly: true
        pathType: FileOrCreate

kubernetes_common_kubeadm_config:
  apiVersion: kubeadm.k8s.io/v1beta1
  kind: ClusterConfiguration
  apiServer:
    timeoutForControlPlane: 4m0s
    certSANs: "{{ kubernetes_common_api_ip | kube_lookup_hostname(kubernetes_common_api_fqdn, True) }}"
    extraArgs:
      profiling: "{{kubernetes_common_profiling_enabled}}"
      feature-gates: "{{kubernetes_common_feature_gates_string}}"
      encryption-provider-config: /etc/kubernetes/encryption-provider-config.yaml
      admission-control-config-file: /etc/kubernetes/admission-control-config.yaml
      enable-admission-plugins: EventRateLimit,AlwaysPullImages,PodSecurityPolicy,ResourceQuota,NodeRestriction,OwnerReferencesPermissionEnforcement,PersistentVolumeClaimResize,PodTolerationRestriction,StorageObjectInUseProtection
      tls-cipher-suites: "{{kubernetes_common_cluster_tls_cipher_suites_string}}"
    extraVolumes:
    - name: "log"
      hostPath: "/var/log/kubernetes"
      mountPath: "/var/log/kubernetes"
      readOnly: false
      pathType: DirectoryOrCreate
  controlPlaneEndpoint: "{{ kubernetes_common_api_fqdn }}"
  controllerManager:
    extraArgs:
      feature-gates: "{{kubernetes_common_feature_gates_string}}"
      terminated-pod-gc-threshold: "1000"
      profiling: "{{kubernetes_common_profiling_enabled}}"
      tls-cipher-suites: "{{kubernetes_common_cluster_tls_cipher_suites_string}}"
  networking:
    dnsDomain: cluster.internal.randomvariable.co.uk
    podSubnet: 172.16.0.0/13
    serviceSubnet: 172.24.0.0/13
  scheduler:
    extraArgs:
      feature-gates: "{{kubernetes_common_feature_gates_string}}"
      profiling: "{{kubernetes_common_profiling_enabled}}"
      tls-cipher-suites: "{{kubernetes_common_cluster_tls_cipher_suites_string}}"

kubernetes_common_service_account_volume_token_projection_configuration:
  enabled: False
  cluster_configuration:
    apiServer:
      service-account-issuer: "{{kubernetes_common_api_ip | kube_lookup_hostname(kubernetes_common_api_fqdn, True)}}"
      service-account-signing-key-file: "/etc/kubernetes/pki/sa.key"

kubernetes_common_oidc_configuration:
  enabled: False
  cluster_configuration:
    apiServer:
      oidc-client-id: "replace_me"
      oidc-issuer-url: "replace_me"
      oidc-username-claim: "sub"
      oidc-groups-claim: "groups"
      oidc-username-prefix: "oidc:user:"
      oidc-groups-prefix: "oidc:group:"

kubernetes_common_etcd_external_configuration:
  enabled: False
  cluster_configuration:
    etcd:
      external:
        endpoints: "{{ etcd_client_endpoints }}"

kubernetes_common_kubelet_configuration:
  apiVersion: kubelet.config.k8s.io/v1beta1
  kind: KubeletConfiguration
  cgroupDriver: systemd
  eventRecordQPS: 0
  readOnlyPort: 0
  featureGates: "{{kubernetes_common_feature_gates}}"
  protectKernelDefaults: true
  tlsCipherSuites: "{{kubernetes_common_cluster_tls_cipher_suites}}"


kubernetes_common_encryption_provider:
  enabled: False
  cluster_configuration:
    apiServer:
      extraVolumes:
      - name: "kmsplugin"
        hostPath: "/var/run/kmsplugin"
        mountPath: "/var/run/kmsplugin"
        readOnly: false
        pathType: DirectoryOrCreate
      - name: "encryption-provider"
        hostPath: "/etc/kubernetes/encryption-provider-config.yaml"
        mountPath: "/etc/kubernetes/encryption-provider-config.yaml"
    encryption_provider_configuration:
      kind: EncryptionConfiguration
      apiVersion: apiserver.config.k8s.io/v1
      resources:
        - resources:
          - secrets
          providers:
          - kms:
              name: kms
              endpoint: unix:///var/run/kmsplugin/socket.sock
              cachesize: 255
              timeout: 5s
          - identity: {}


## Limitations

* Variables may need to migrated from an older version of Kubernetes.
