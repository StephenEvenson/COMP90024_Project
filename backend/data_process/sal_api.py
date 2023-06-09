#
# Part of Assignment 2 - COMP90024
#
# Cluster and Cloud Computing - Team 72
#
# Authors:
#
#  - Juntao Lu (Student ID: 1290513)
#  - Runtian Zhang (Student ID: 1290379)
#  - Jiahao Shen (Student ID: 1381187)
#  - Yuchen Liu (Student ID: 1313394)
#  - Jie Shen (Student ID: 1378708)
#
# Location: Melbourne
#
import json


class SALAPI:
    def __init__(self, sal_json_file):
        self.gcc_memory = {}
        self.gcc_key_set = {'1gsyd', '2gmel', '3gbri', '4gade', '5gper', '6ghob', '7gdar', '8acte', '9oter'}
        with open(sal_json_file, 'r', encoding='utf-8') as sal_f:
            data = json.load(sal_f)
            self.sal_data = {k: v for k, v in data.items() if v['gcc'] in self.gcc_key_set}

    def get_gcc_by_name(self, name):
        if name in self.gcc_memory:
            gcc = self.gcc_memory[name]
            return gcc
        else:
            if name in self.sal_data:
                gcc = self.sal_data[name]['gcc']
                self.gcc_memory[name] = gcc
                return gcc
            else:
                return None
