# -*- coding: utf-8 -*-
from hstest.test_case import TestCase

from base import HyperTubeTest


class HyperTubeTestRunner(HyperTubeTest):
    def generate(self):
        return [
            # 1 task
            TestCase(attach=self.check_server),
            TestCase(attach=self.check_create_videos),
        ]

    def check(self, reply, attach):
        return attach()


if __name__ == '__main__':
    HyperTubeTestRunner('hypertube.manage').run_tests()
