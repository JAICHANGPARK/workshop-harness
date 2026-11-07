#!/usr/bin/env python3
"""
test_harness.py - Automated Unit and Integration Test Suite for Workshop Harness
Verifies CLI functions, model/typography audits, skill frontmatter, multi-stack scaffolding,
and end-to-end bundle exporters (Open Codelabs, Google Colab, Presentation Slides).
"""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

import harness_cli


class TestWorkshopHarness(unittest.TestCase):
    """Comprehensive unit and integration tests for harness_cli and agent skills."""

    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp(prefix="wh_test_"))

    def tearDown(self):
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_01_sanitize_no_em_dash(self):
        """Verify forbidden em dash characters are replaced with standard hyphens."""
        em = chr(0x2014)
        self.assertEqual(harness_cli.sanitize_no_em_dash(f"word1{em}word2"), "word1 - word2")
        self.assertEqual(harness_cli.sanitize_no_em_dash(f"word1 {em} word2"), "word1 - word2")
        self.assertEqual(harness_cli.sanitize_no_em_dash("clean-text"), "clean-text")

    def test_02_audit_typography_and_terminology_fix(self):
        """Verify audit_typography detects and auto-fixes em dashes and awkward literal translations."""
        em = chr(0x2014)
        sample_md = self.temp_dir / "guide.md"
        sample_md.write_text(
            f"# Title{em}Subtitle\n이 문서는 손으로 하는 실험실과 생각 예산을 설명합니다.\n",
            encoding="utf-8",
        )
        # Should fail before fix
        self.assertFalse(harness_cli.audit_typography(str(self.temp_dir), fix=False))
        # Should pass and fix when fix=True
        self.assertTrue(harness_cli.audit_typography(str(self.temp_dir), fix=True))
        fixed_text = sample_md.read_text(encoding="utf-8")
        self.assertNotIn(em, fixed_text)
        self.assertIn("Hands-on Lab (핸즈온 랩)", fixed_text)
        self.assertIn("Thinking Budget (추론 예산)", fixed_text)
        self.assertTrue(harness_cli.audit_typography(str(self.temp_dir), fix=False))

    def test_03_audit_models_detection_and_fix(self):
        """Verify audit_models detects deprecated model tags and auto-upgrades them to 2026 standards."""
        sample_py = self.temp_dir / "app.py"
        sample_py.write_text(
            'MODEL_A = "gemini-1.5-flash"\nMODEL_B = "gemini-2.5-pro"\nMODEL_C = "gpt-4o-mini"\n',
            encoding="utf-8",
        )
        self.assertFalse(harness_cli.audit_models(str(self.temp_dir), fix=False))
        self.assertTrue(harness_cli.audit_models(str(self.temp_dir), fix=True))
        updated_text = sample_py.read_text(encoding="utf-8")
        self.assertIn("gemini-3.8-flash", updated_text)
        self.assertIn("gemini-4-argon", updated_text)
        self.assertIn("gpt-6-luna", updated_text)
        self.assertTrue(harness_cli.audit_models(str(self.temp_dir), fix=False))

    def test_04_skills_yaml_frontmatter_integrity(self):
        """Verify all SKILL.md files in skills/ have valid YAML frontmatter and zero em dashes."""
        skills_dir = harness_cli.HARNESS_ROOT / "skills"
        skill_files = sorted(skills_dir.glob("*/SKILL.md"))
        self.assertGreaterEqual(len(skill_files), 21)
        em = chr(0x2014)
        for sf in skill_files:
            content = sf.read_text(encoding="utf-8")
            self.assertTrue(content.startswith("---"), f"Missing YAML frontmatter in {sf}")
            self.assertIn("name:", content, f"Missing name field in {sf}")
            self.assertIn("description:", content, f"Missing description field in {sf}")
            self.assertNotIn(em, content, f"Forbidden em dash found in {sf}")

    def test_05_init_workshop_path_name_sanitization_and_bundles(self):
        """Verify init_workshop sanitizes path-prefixed --name and passes all export and integrity gates."""
        target_path = self.temp_dir / "path-based-workshop"
        proj_dir = harness_cli.init_workshop(
            name=str(target_path),
            topic="Gemma 4 & ADK Multi-Agent Lab",
            stack_str="python,adk,agents-cli,polyglot,ollama",
        )
        self.assertEqual(proj_dir.resolve(), target_path.resolve())
        pyproject_text = (proj_dir / "pyproject.toml").read_text(encoding="utf-8")
        self.assertIn('name = "path-based-workshop"', pyproject_text)
        self.assertNotIn(str(self.temp_dir), pyproject_text)

        # Verify all 5 ADK language tracks exist (Python + Go, Java, Kotlin, TypeScript)
        self.assertTrue((proj_dir / "workshop" / "02_final" / "agent.py").exists())
        self.assertTrue((proj_dir / "workshop" / "02_final" / "sre_agent" / "agent.py").exists())
        self.assertTrue((proj_dir / "workshop" / "02_final" / "polyglot" / "go" / "main.go").exists())
        self.assertTrue(
            (proj_dir / "workshop" / "02_final" / "polyglot" / "java" / "src" / "main" / "java" / "com" / "example" / "adk" / "SreAdkJavaApp.java").exists()
        )
        self.assertTrue(
            (proj_dir / "workshop" / "02_final" / "polyglot" / "kotlin" / "src" / "main" / "kotlin" / "com" / "example" / "adk" / "SreAdkKotlinApp.kt").exists()
        )
        self.assertTrue((proj_dir / "workshop" / "02_final" / "polyglot" / "typescript" / "src" / "agent.ts").exists())

        # Verify compatibility audit, persona loop review, codelab, colab, slides, and test_workshop
        issues = harness_cli.audit_compatibility("python,adk,agents-cli,ollama", str(proj_dir))
        self.assertGreaterEqual(len(issues), 3)
        harness_cli.audit_persona_loop("Gemma 4 & ADK Multi-Agent Lab", str(proj_dir))
        self.assertTrue((proj_dir / "docs" / "00-persona-loop-review-report.md").exists())

        self.assertTrue(harness_cli.export_codelab(str(proj_dir)))
        self.assertTrue((proj_dir / "output" / "open-codelabs" / "codelab.yaml").exists())

        self.assertTrue(harness_cli.export_colab(str(proj_dir)))
        self.assertTrue((proj_dir / "output" / "colab" / "workshop_starter.ipynb").exists())
        self.assertTrue((proj_dir / "output" / "colab" / "workshop_solution.ipynb").exists())
        sol_nb_text = (proj_dir / "output" / "colab" / "workshop_solution.ipynb").read_text(encoding="utf-8")
        self.assertIn("adlc_root_coordinator", sol_nb_text)
        self.assertIn("verify_release_gate", sol_nb_text)

        self.assertTrue(harness_cli.build_slides(str(proj_dir)))
        self.assertTrue((proj_dir / "output" / "slides" / "slides.md").exists())
        self.assertTrue((proj_dir / "output" / "slides" / "index.html").exists())

        self.assertTrue(harness_cli.test_workshop(str(proj_dir)))

    def test_06_multi_stack_scaffolding_modes(self):
        """Verify Flutter/GenUI, Android Compose, TypeScript, and Go scaffolding modes pass integrity checks."""
        for stack_name, expected_rel_file in [
            ("flutter,genui,a2ui", "workshop/01_starter/lib/main.dart"),
            ("android", "workshop/01_starter/app/build.gradle.kts"),
            ("typescript", "workshop/01_starter/src/agent.ts"),
            ("go", "workshop/01_starter/main.go"),
        ]:
            slug = stack_name.split(",")[0] + "-lab"
            proj_dir = harness_cli.init_workshop(
                name=slug,
                topic=f"Workshop for {stack_name}",
                target_dir=str(self.temp_dir),
                stack_str=stack_name,
            )
            self.assertTrue((proj_dir / expected_rel_file).exists(), f"Missing {expected_rel_file} for {stack_name}")
            self.assertTrue(harness_cli.test_workshop(str(proj_dir)))

    def test_07_non_existent_target_returns_false(self):
        """Verify CLI helper functions return False gracefully when given a non-existent directory."""
        missing = str(self.temp_dir / "does-not-exist")
        self.assertFalse(harness_cli.audit_models(missing))
        self.assertFalse(harness_cli.audit_typography(missing))
        self.assertFalse(harness_cli.test_workshop(missing))
        self.assertFalse(harness_cli.build_pdf(missing))
        self.assertFalse(harness_cli.export_codelab(missing))
        self.assertFalse(harness_cli.export_colab(missing))
        self.assertFalse(harness_cli.build_slides(missing))


if __name__ == "__main__":
    unittest.main()
