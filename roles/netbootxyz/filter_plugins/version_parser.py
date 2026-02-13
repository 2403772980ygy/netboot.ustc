import re
from hashlib import md5

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

    def download_paths(self, endpoints, upstream, path):
        ret = []
        for dist, obj in endpoints.items():
            for ff in obj["files"]:
                ret.append({"url":upstream+obj["path"]+ff,"path":path + md5(str(obj["path"]).encode()).hexdigest() + "/" + ff})
        return ret

    def new_paths(self, endpoints, path):
        ret = endpoints
        for dist, obj in endpoints.items():
            ret[str(dist)]["path"] = path + md5(str(obj["path"]).encode()).hexdigest() + "/"
        return ret
    
