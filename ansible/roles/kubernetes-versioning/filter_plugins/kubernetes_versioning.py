import re


class FilterModule(object):

    KUBERNETES_VERSIONS = [
        {
            "kubernetes": "1.12.7",
            "etcd": "3.2.24",
            "cni": "0.7.5",
            "coredns": "1.2.2",
            "cri-tools": "1.12.0"
        },
        {
            "kubernetes": "1.13.0",
            "etcd": "3.2.24",
            "cni": "0.7.5",
            "coredns": "1.2.6",
            "cri-tools": "1.12.0"
        },
        {  "kubernetes": "1.14.0",
            "etcd": "3.3.10",
            "cni": "0.7.5",
            "coredns": "1.3.1",
            "cri-tools": "1.12.0"
        },
    ]

    LATEST_KUBERNETES_VERSIONS = [
        "1.12": "1.12.8",
        "1.13": "1.13.6",
        "1.14": "1.14.1",
    ]

    def kubernetes_versions:
        map(lambda x: x['kubernetes'], KUBERNETES_VERSIONS)

    def match_version(self, version):
        components: version.split(".")
        major_version = components[0]
        minor_version =

    def filters(self):
        return {
            'kube_platform_version': self.kube_platform_version,
            'kube_debian_distro_version': self.kube_debian_distro_version,
        }

    def kube_platform_version(self, version, platform):
        match = re.match('(\d+\.\d+.\d+)\-(\d+)', version)
        if not match:
            raise Exception("Version '%s' does not appear to be a "
                            "kubernetes version." % version)
        sub = match.groups(1)[1]
        if len(sub) == 1:
            if platform.lower() == "debian":
                return "%s-%s" % (match.groups(1)[0], '{:02d}'.format(sub))
            else:
                return version
        if len(sub) == 2:
            if platform.lower() == "redhat":
                return "%s-%s" % (match.groups(1)[0], int(sub))
            else:
                return version

        raise Exception("Could not parse kubernetes version")

    def kube_debian_distro_version(self, distro):
        if distro.lower() in ("xenial", "bionic",):
            return "kubernetes-xenial"
        return "kubernetes-%s" % distro.lower()
