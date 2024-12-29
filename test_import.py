#!/usr/bin/env python3

import filecmp
import json
import os
import shutil
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

import hydroquebec_peak_events_ical as hical


class TestStringMethods(unittest.TestCase):
    @patch("time.time")
    def test_empty(self, mock_time):
        mock_time.return_value = 1643723900  # Set the mock time to a specific value
        self._test_generate_files("empty.json", "empty")

    @patch("time.time")
    def test_add_events(self, mock_time):
        mock_time.return_value = 1643723900  # Set the mock time to a specific value
        self._test_generate_files("2024.12.23.json", "add_events")

    @patch("time.time")
    def test_keep_previous_events(self, mock_time):
        mock_time.return_value = 1643723900  # Set the mock time to a specific value
        self._test_generate_files(
            "2024.12.29.json", "keep_previous_events", "add_events"
        )

    @patch("time.time")
    def test_already_present(self, mock_time):
        mock_time.return_value = 1643723900  # Set the mock time to a specific value
        self._test_generate_files("2024.12.23.json", "add_events", "add_events")

    def _test_generate_files(self, input, expected_output, previous_output=None):
        data = json.loads(Path("fixtures", "input", input).read_bytes())
        expected_output_dir = Path("fixtures", "output", expected_output)
        with tempfile.TemporaryDirectory() as output_dir:
            if previous_output:
                previous_output_dir = Path("fixtures", "output", previous_output)
                shutil.copytree(previous_output_dir, output_dir, dirs_exist_ok=True)

            if "SAVE_TEST_RESULTS" in os.environ:
                output_dir = expected_output_dir
                if not expected_output_dir.exists():
                    expected_output_dir.mkdir()

            hical.generate_files(data, output_dir)

            # Compare directories
            comparison = filecmp.dircmp(expected_output_dir, output_dir, shallow=False)
            self._assert_filecmp(comparison)

    def _assert_filecmp(self, cmp):
        for subcmp in cmp.subdirs.values():
            self._assert_filecmp(subcmp)

        self.assertEqual([], cmp.right_only, "")
        self.assertEqual([], cmp.left_only, "")

        for f in cmp.diff_files:
            left_content = Path(cmp.left, f).read_text()
            right_content = Path(cmp.right, f).read_text()
            self.assertEqual(left_content, right_content, Path(cmp.left, f))


if __name__ == "__main__":
    unittest.main()
