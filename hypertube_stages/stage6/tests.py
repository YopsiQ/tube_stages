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
            # 3 task
            TestCase(attach=self.check_main_page_search),
            TestCase(attach=self.check_main_page_tag_filtering),
            # 4 task
            TestCase(attach=self.check_signup),
            TestCase(attach=self.check_login),
            # 5 task
            TestCase(attach=self.check_uploading_video),
            TestCase(attach=self.check_forbid_anonymous_upload),
            TestCase(attach=self.check_upload_page_main_link),
            # 6 task
            TestCase(attach=self.check_watch_and_video_response),
        ]

    def check(self, reply, attach):
        return attach()


if __name__ == '__main__':
    HyperTubeTestRunner('hypertube.manage').run_tests()
