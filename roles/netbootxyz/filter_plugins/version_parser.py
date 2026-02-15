import re
from hashlib import md5
from copy import deepcopy

class FilterModule(object):

    def filters(self):
        return {
            "parse_versions": self.parse_versions,
            "update_versions": self.update_versions,
            "download_paths": self.download_paths,
            "new_paths": self.new_paths
        }

    def parse_versions(self, content, distro):
        if distro == 'archlinux':
            return self.parse_versions_arch(content)
        elif distro == 'almalinux':
            return self.parse_versions_alma(content)
        elif distro == 'centos':
            return self.parse_versions_centos(content)
    
    def parse_versions_alma(self, content):
        pattern = r"<span class=\"name\">(\d*?)/</span>"
        ms = re.findall(pattern, content)
        ms = sorted([int(m) for m in list(set(ms))])
        return [{"code_name": m, "name": m} for m in ms]

    def parse_versions_arch(self, content):
        pattern = r"(\d{4}\.\d{2}\.\d{2})/"
        ms = re.findall(pattern, content)
        ms = sorted([str(m) for m in list(set(ms))])
        return [{"code_name": m, "name": m} for m in ms]

    def parse_versions_centos(self, content):
        pattern = r"((\d*)-stream)"
        ms = re.findall(pattern, content)
        ms =  sorted(list(set(ms)), key=lambda x:int(x[1]))
        return [{"code_name": m[0], "name": m[1]+".0 Stream"} for m in ms]

    def update_versions(self, releases, content, distro):
        distro = str(distro)
        ret = releases
        ret[distro]["versions"] = self.parse_versions(content, distro)
        return ret

    def download_paths(self, endpoints, upstream, path, oss=None):
        ret = []
        for dist, obj in endpoints.items():
            if oss and obj["os"] not in oss:
                continue
            op = str(obj["path"])
            subdir = md5(op.encode()).hexdigest()
            for ff in obj["files"]:
                ret.append({"url": f"{upstream}{op}{ff}", "path": f"{path}{subdir}/{ff}"})
        return ret

    def new_paths(self, endpoints, path, lst=None):
        ret = endpoints
        for dist, obj in endpoints.items():
            if not lst or obj["os"] in lst:
                ret[str(dist)]["path"] = "/" + path + md5(str(obj["path"]).encode()).hexdigest() + "/"
                ret[str(dist)]["use_endpoint_mirror"] = True
            else:
                ret[str(dist)]["use_endpoint_mirror"] = False
        return ret
    
