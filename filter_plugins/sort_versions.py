"""
# based on: https://github.com/diodonfrost/ansible-role-vagrant/pull/1#issuecomment-683432330
Sort complex versions
"""

from distutils.version import LooseVersion
from ansible.module_utils.common.text.converters import to_native


def filter_sort_versions(value):
    """
        Ansible entrypoint function
    """
    try:
        # forcing string
        str_val = [x if x.startswith('v') else 'v{}'.format(x) for x in value]
        sorted_stuff = sorted(str_val, key=LooseVersion)
    except Exception as e:
        raise AnsibleError('Something happened, this was original exception: %s' % to_native(e))
    
    # replace old version format, so urls don't break
    for old_version in value:
        if old_version.startswith('v'):
            pass
        else:
            for index, version in enumerate(sorted_stuff):
                if old_version in version:
                    sorted_stuff[index] = old_version
    return sorted_stuff


class FilterModule(object):
    """
        Sort complex versions like 0.10.2, 0.1.1, 0.10.12
    """
    filter_sort = {
        'sort_versions': filter_sort_versions,
    }

    def filters(self):
        """
            Return the sorted values
        """
        return self.filter_sort
