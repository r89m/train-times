import dataclasses
import functools
import json
from builtins import staticmethod
from pathlib import Path
from typing import List
from unittest import TestCase

from tests.resources import get
from traintimes.models import DepartureJson
from traintimes.timetable import combine_timetables, sort_timetable, sort_timetable_comparison_function


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


class TestTimetableSort(TestCase):

    @staticmethod
    def _DepartureJsonDecoder(departure_json_dict: dict) -> DepartureJson:
        return DepartureJson(**departure_json_dict)

    def _load_raw_timetable(self, json_path: Path) -> List[DepartureJson]:
        timetable_str = json_path.read_text()
        return json.loads(timetable_str, object_hook=TestTimetableSort._DepartureJsonDecoder)

    def _encode_timetable(self, timetable: List[DepartureJson]) -> str:
        return json.dumps(timetable, indent=2, cls=EnhancedJSONEncoder, sort_keys=True)

    def test_sort_timetable_simple(self):
        self._test_sort_timetable("clj", "simple")
        self._test_sort_timetable("lbg", "simple")

    def test_sort_timetable_near_midnight(self):
        self._test_sort_timetable("clj", "midnight")
        self._test_sort_timetable("lbg", "midnight")

    def _test_sort_timetable(self, csr: str, timetable_type: str) -> None:
        original_timetable_obj = self._load_raw_timetable(get(f"timetable-{timetable_type}-{csr}.json"))
        sorted_timetable = sorted(original_timetable_obj, key=functools.cmp_to_key(sort_timetable_comparison_function))

        expected_sorted_timetable = get("sorted", f"timetable-{timetable_type}-{csr}.json").read_text()
        self.assertEqual(expected_sorted_timetable, self._encode_timetable(sorted_timetable))

    def test_sort_timetable_combined(self):
        timetable_clj = sort_timetable(self._load_raw_timetable(get("timetable-simple-clj.json")))
        timetable_lbg = sort_timetable(self._load_raw_timetable(get("timetable-simple-lbg.json")))

        combined_timetable = combine_timetables(timetable_clj, timetable_lbg)

        expected_combined_timetable = get("combined", "timetable-simple.json").read_text()
        self.assertEqual(expected_combined_timetable, self._encode_timetable(combined_timetable))
