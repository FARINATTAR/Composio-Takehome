"""
Comprehensive verification test suite for Composio Take-Home deliverables.
Validates dataset integrity, edge-case catches, agent execution, and dashboard artifacts.
"""

import unittest
import json
import os
from composio_agent import ResearchPipeline, ComposioToolkitSynthesizer

class TestComposioDatasetAndPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data_path = "data/apps_100.json"
        with open(cls.data_path, "r", encoding="utf-8") as f:
            cls.apps = json.load(f)
        cls.pipeline = ResearchPipeline(cls.data_path)

    def test_dataset_count_and_uniqueness(self):
        """Verify exactly 100 unique applications."""
        self.assertEqual(len(self.apps), 100, "Dataset must contain exactly 100 apps.")
        ids = [a["id"] for a in self.apps]
        self.assertEqual(len(ids), len(set(ids)), "App IDs must be unique.")
        names = [a["name"].lower() for a in self.apps]
        self.assertEqual(len(names), len(set(names)), "App names must be unique.")

    def test_ten_categories_distribution(self):
        """Verify each of the 10 specified categories contains 10 apps."""
        categories = {}
        for a in self.apps:
            cat = a["category"]
            categories[cat] = categories.get(cat, 0) + 1
        
        self.assertEqual(len(categories), 10, "There must be exactly 10 categories.")
        for cat, count in categories.items():
            self.assertEqual(count, 10, f"Category '{cat}' must contain exactly 10 apps, found {count}.")

    def test_required_fields_presence(self):
        """Verify all mandatory fields are populated with valid data."""
        required_fields = [
            "id", "name", "domain", "category", "purpose", "auth_methods",
            "primary_auth", "gating_status", "api_surface", "buildability_verdict",
            "evidence_url", "pass1_extracted", "pass2_verification", "composio_fit_score"
        ]
        for a in self.apps:
            for field in required_fields:
                self.assertIn(field, a, f"App '{a.get('name')}' missing field '{field}'")
            self.assertTrue(a["evidence_url"].startswith("http"), f"Invalid evidence URL for {a['name']}")

    def test_whatsapp_edge_case(self):
        """Verify WhatsApp Business catches Meta Verification Gate."""
        app = self.pipeline.run_for_app("WhatsApp Business")
        p2 = app["verification_result"]["pass2_verified"]
        self.assertTrue(p2["correction_applied"])
        self.assertIn("Meta Verification Gate", p2["gating"])
        self.assertEqual(p2["verdict"], "Feasible with Gating")

    def test_dealcloud_edge_case(self):
        """Verify DealCloud catches Partner/Enterprise Gate."""
        app = self.pipeline.run_for_app("DealCloud")
        p2 = app["verification_result"]["pass2_verified"]
        self.assertTrue(p2["correction_applied"])
        self.assertIn("Enterprise", p2["gating"])
        self.assertEqual(p2["verdict"], "Feasible with Gating")

    def test_notebooklm_edge_case(self):
        """Verify NotebookLM catches consumer web app divergence into Vertex AI."""
        app = self.pipeline.run_for_app("NotebookLM")
        p2 = app["verification_result"]["pass2_verified"]
        self.assertTrue(p2["correction_applied"])
        self.assertIn("Vertex AI", p2["gating"])

    def test_fanbasis_edge_case(self):
        """Verify fanbasis is identified as Blocked due to lack of public API."""
        app = self.pipeline.run_for_app("fanbasis")
        p2 = app["verification_result"]["pass2_verified"]
        self.assertEqual(p2["verdict"], "Blocked")

    def test_sherlock_cli_edge_case(self):
        """Verify Sherlock OSINT tool is marked Ready via CLI Wrapper."""
        app = self.pipeline.run_for_app("Sherlock")
        p2 = app["verification_result"]["pass2_verified"]
        self.assertIn("CLI", p2["verdict"])

    def test_composio_spec_synthesis(self):
        """Verify Composio action toolkit specification generator."""
        shopify = next(a for a in self.apps if a["name"] == "Shopify")
        spec = ComposioToolkitSynthesizer.generate_composio_spec(shopify)
        self.assertEqual(spec["composio_app_key"], "shopify")
        self.assertEqual(spec["auth_configuration"]["auth_scheme"], "OAUTH2")
        self.assertGreaterEqual(len(spec["actions"]), 1)

    def test_dashboard_file_integrity(self):
        """Verify index.html exists and contains key UI anchors."""
        self.assertTrue(os.path.exists("index.html"), "index.html must exist.")
        with open("index.html", "r", encoding="utf-8") as f:
            html = f.read()
        self.assertIn("Farin Attar", html)
        self.assertIn("100-App Intelligence Grid", html)
        self.assertIn("Live Verification Agent Terminal Simulator", html)
        self.assertIn("WhatsApp Business", html)
        self.assertIn("DealCloud", html)

if __name__ == "__main__":
    unittest.main()
