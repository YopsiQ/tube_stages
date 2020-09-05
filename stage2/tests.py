# -*- coding: utf-8 -*-
from hstest.test_case import TestCase

from base import HyperTubeTest


class HyperTubeTestRunner(HyperTubeTest):
    def generate(self):
        return [
            # 1 task
            TestCase(attach=self.check_server),
            TestCase(attach=self.check_create_videos),
            # 2 task
            TestCase(attach=self.check_main_header),
            TestCase(attach=self.check_main_page_login_link),
            TestCase(attach=self.check_main_page_upload_link),
            TestCase(attach=self.check_main_page_video_links),
            TestCase(attach=self.check_main_page_video_count),
        ]

    def check(self, reply, attach):
        return attach()


if __name__ == '__main__':
    HyperTubeTestRunner('hypertube.manage').run_tests()
