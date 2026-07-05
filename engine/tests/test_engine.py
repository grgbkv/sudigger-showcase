"""Tests for the four properties the production system was built around."""
import csv
import os
import shutil
import unittest

from engine import demo, fixtures, publish, verify
from engine.state import OUT_DIR


class TestConservativeNames(unittest.TestCase):
    def test_legal_suffix_stripped(self):
        self.assertEqual(verify.clean_display_name("Aurora Robotics s.r.o."),
                         "Aurora Robotics")
        self.assertEqual(verify.clean_display_name("Datovka a.s."), "Datovka")
        self.assertEqual(verify.clean_display_name("Wisla Cloud Sp. z o.o."),
                         "Wisla Cloud")

    def test_brand_names_untouched(self):
        # the production lesson: aggressive cleaning broke real names
        self.assertEqual(verify.clean_display_name("QUANTA.IO"), "QUANTA.IO")
        self.assertEqual(verify.clean_display_name("Labs of Latvia"), "Labs of Latvia")

    def test_cross_script_dedup(self):
        # «Нордик Дата» and "Nordik Data OÜ" are the same company
        self.assertEqual(verify.dedup_key("Нордик Дата"),
                         verify.dedup_key("Nordik Data OÜ"))


class TestReplay(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.state, cls.meter, cls.catches = demo.run(verbose=False)

    def test_signal_gate_economics(self):
        # the whole point: a small fraction of the naive cost
        self.assertLess(self.meter.scoring_calls,
                        0.15 * self.meter.counterfactual_calls)

    def test_the_catch(self):
        aurora = [c for c in self.catches if c["company"] == "Aurora Robotics"]
        self.assertTrue(aurora, "Aurora Robotics catch missing")
        self.assertGreaterEqual(aurora[0]["lead"], 14)

    def test_geo_gate_rejects_foreign_branch(self):
        rejected = [e for e in self.state.changelog if e["event"] == "geo_reject"]
        self.assertTrue(any("Global Corp Prague" in e["company"] for e in rejected))
        self.assertNotIn(verify.dedup_key("Global Corp Prague s.r.o."),
                         self.state.companies)

    def test_linkedin_never_guessed(self):
        key = verify.dedup_key("Vector Analytics Sp. z o.o.")
        self.assertEqual(self.state.companies[key]["linkedin_company"], "Not found")

    def test_duplicate_collapsed(self):
        names = [r["company_name"] for r in self.state.companies.values()]
        self.assertEqual(sum(1 for n in names if "Nordik" in n), 1)


class TestHumanColumns(unittest.TestCase):
    def setUp(self):
        self._backup = None
        if os.path.exists(OUT_DIR):
            self._backup = OUT_DIR + ".bak_test"
            shutil.rmtree(self._backup, ignore_errors=True)
            shutil.move(OUT_DIR, self._backup)

    def tearDown(self):
        shutil.rmtree(OUT_DIR, ignore_errors=True)
        if self._backup:
            shutil.move(self._backup, OUT_DIR)

    def test_annotations_survive_rebuild(self):
        state, meter, catches = demo.run(verbose=False)
        publish.publish_top_targets(state)

        # a human annotates a row in the published surface
        with open(publish.TOP_TARGETS, newline="") as f:
            rows = list(csv.DictReader(f))
        rows[0]["ACCOUNT"] = "georgy"
        rows[0]["COMMENTS"] = "intro call booked"
        annotated = rows[0]["company_name"]
        with open(publish.TOP_TARGETS, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=rows[0].keys())
            w.writeheader()
            w.writerows(rows)

        # the nightly rebuild must not lose it
        publish.publish_top_targets(state)
        with open(publish.TOP_TARGETS, newline="") as f:
            after = {r["company_name"]: r for r in csv.DictReader(f)}
        self.assertEqual(after[annotated]["ACCOUNT"], "georgy")
        self.assertEqual(after[annotated]["COMMENTS"], "intro call booked")


if __name__ == "__main__":
    unittest.main()
