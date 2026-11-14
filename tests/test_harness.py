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
        """Verify audit_typography detects and auto-fixes em dashes and KO/JA/ZH awkward literal translations."""
        em = chr(0x2014)
        sample_md = self.temp_dir / "guide.md"
        sample_md.write_text(
            f"# Title{em}Subtitle\n"
            "KO: 손으로 하는 실험실과 생각 예산이 생성되어집니다.\n"
            "JA: 手で触る実験室と走る本を用意します。\n"
            "ZH: 手把手的实验室与骨架代码。\n",
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
        self.assertIn("생성됩니다", fixed_text)
        self.assertIn("Hands-on Lab (ハンズオンラボ)", fixed_text)
        self.assertIn("Runbook (ランブック)", fixed_text)
        self.assertIn("Hands-on Lab (实战工作坊)", fixed_text)
        self.assertIn("Starter / Boilerplate Code (Starter 初始代码)", fixed_text)
        self.assertTrue(harness_cli.audit_typography(str(self.temp_dir), fix=False))

    def test_03_audit_models_detection_and_fix(self):
        """Verify audit_models detects deprecated model tags and auto-upgrades them to 2026 standards."""
        sample_py = self.temp_dir / "app.py"
        sample_py.write_text(
            'MODEL_A = "gemini-1.5-flash"\n'
            'MODEL_B = "gemini-2.5-pro"\n'
            'MODEL_C = "gpt-4o-mini"\n'
            'MODEL_D = "gemini-3.7-flash"\n'
            'MODEL_E = "gemini-omni-1.1-flash"\n'
            'MODEL_F = "gemini-embedding-2-preview"\n'
            'MODEL_G = "claude-fable-5.1"\n'
            'MODEL_H = "claude-sonnet-5.5"\n'
            'MODEL_I = "gpt-5.6-terra"\n'
            'MODEL_J = "gemma2:9b"\n'
            'MODEL_K = "gemma4:e12b"\n'
            'MODEL_L = "embeddinggemma:300m"\n',
            encoding="utf-8",
        )
        self.assertFalse(harness_cli.audit_models(str(self.temp_dir), fix=False))
        self.assertTrue(harness_cli.audit_models(str(self.temp_dir), fix=True))
        updated_text = sample_py.read_text(encoding="utf-8")
        self.assertIn("gemini-4-hydrogen", updated_text)
        self.assertIn("gemini-4-carbon", updated_text)
        self.assertIn("gpt-6-luna", updated_text)
        self.assertIn("gemini-omni-1.2-flash", updated_text)
        self.assertIn("gemini-embedding-2", updated_text)
        self.assertIn("claude-fable-5-2", updated_text)
        self.assertIn("claude-sonnet-5-5", updated_text)
        self.assertIn("gpt-6.1-terra", updated_text)
        self.assertIn("gemma4:12b", updated_text)
        self.assertIn("embeddinggemma-2:270m", updated_text)
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

    def test_08_multi_provider_claude_and_openai_scaffolding(self):
        """Verify Anthropic Claude, OpenAI Responses API, and ADK LiteLlm multi-provider scaffolding."""
        claude_dir = harness_cli.init_workshop(
            name="claude-agent-lab",
            topic="Agentic Workflows with Claude Sonnet 5.5",
            target_dir=str(self.temp_dir),
            stack_str="python,claude",
        )
        claude_pyproject = (claude_dir / "pyproject.toml").read_text(encoding="utf-8")
        claude_env = (claude_dir / ".env.sample").read_text(encoding="utf-8")
        claude_final = (claude_dir / "workshop" / "02_final" / "main.py").read_text(encoding="utf-8")
        self.assertIn("anthropic>=2.8.0", claude_pyproject)
        self.assertIn("ANTHROPIC_API_KEY", claude_env)
        self.assertIn("claude-sonnet-5-5", claude_final)
        self.assertTrue(harness_cli.export_colab(str(claude_dir)))
        self.assertTrue(harness_cli.test_workshop(str(claude_dir)))

        openai_dir = harness_cli.init_workshop(
            name="openai-responses-lab",
            topic="Structured Agents with OpenAI GPT-6.1 Sol",
            target_dir=str(self.temp_dir),
            stack_str="python,openai",
        )
        openai_pyproject = (openai_dir / "pyproject.toml").read_text(encoding="utf-8")
        openai_env = (openai_dir / ".env.sample").read_text(encoding="utf-8")
        openai_final = (openai_dir / "workshop" / "02_final" / "main.py").read_text(encoding="utf-8")
        self.assertIn("openai>=3.50.0", openai_pyproject)
        self.assertIn("OPENAI_API_KEY", openai_env)
        self.assertIn("gpt-6.1-sol", openai_final)
        self.assertTrue(harness_cli.export_colab(str(openai_dir)))
        self.assertTrue(harness_cli.test_workshop(str(openai_dir)))

        adk_claude_dir = harness_cli.init_workshop(
            name="adk-claude-lab",
            topic="Multi-Provider ADK Agents with LiteLlm",
            target_dir=str(self.temp_dir),
            stack_str="python,adk,claude",
        )
        adk_pyproject = (adk_claude_dir / "pyproject.toml").read_text(encoding="utf-8")
        adk_agent = (adk_claude_dir / "workshop" / "02_final" / "agent.py").read_text(encoding="utf-8")
        self.assertIn("litellm>=1.84.0", adk_pyproject)
        self.assertIn('LiteLlm(model="anthropic/claude-sonnet-5-5")', adk_agent)
        self.assertTrue(harness_cli.test_workshop(str(adk_claude_dir)))

        ts_openai_dir = harness_cli.init_workshop(
            name="ts-openai-lab",
            topic="TypeScript OpenAI Responses Workshop",
            target_dir=str(self.temp_dir),
            stack_str="typescript,openai",
        )
        ts_pkg = (ts_openai_dir / "workshop" / "02_final" / "package.json").read_text(encoding="utf-8")
        ts_agent = (ts_openai_dir / "workshop" / "02_final" / "src" / "agent.ts").read_text(encoding="utf-8")
        self.assertIn('"openai": "^7.55.0"', ts_pkg)
        self.assertIn("gpt-6.1-sol", ts_agent)
        self.assertTrue(harness_cli.test_workshop(str(ts_openai_dir)))

    def test_09_natural_language_prompt_instant_generation(self):
        """Verify natural language prompts (KO/EN) auto-infer provider, 2026 model, stack, and slug, and generate immediately."""
        p_claude = harness_cli.parse_natural_prompt("클로드 최신 모델로 1시간짜리 멀티 에이전트 RAG 워크숍 만들어줘")
        self.assertEqual(p_claude["model"], "claude-sonnet-5-5")
        self.assertIn("claude", p_claude["stack"].split(","))
        self.assertTrue(p_claude["name"].startswith("claude-multi-agent-rag"))
        self.assertNotIn("만들어줘", p_claude["topic"])

        p_fable = harness_cli.parse_natural_prompt("Build a Claude Fable enterprise coding workshop")
        self.assertEqual(p_fable["model"], "claude-fable-5-2")
        self.assertIn("claude", p_fable["stack"].split(","))

        p_openai = harness_cli.parse_natural_prompt("OpenAI GPT 최신 모델로 구조화 출력 핸즈온 랩 만들어줘")
        self.assertEqual(p_openai["model"], "gpt-6.1-sol")
        self.assertIn("openai", p_openai["stack"].split(","))

        p_legacy = harness_cli.parse_natural_prompt("gpt-4o로 데이터 분석 에이전트 만들어줘")
        self.assertEqual(p_legacy["model"], "gpt-6.1-sol")
        self.assertIn("openai", p_legacy["stack"].split(","))

        p_adk_claude = harness_cli.parse_natural_prompt("Google ADK랑 Claude로 멀티 에이전트 실습 만들어줘")
        self.assertEqual(p_adk_claude["model"], "claude-sonnet-5-5")
        self.assertIn("adk", p_adk_claude["stack"].split(","))
        self.assertIn("claude", p_adk_claude["stack"].split(","))

        p_gemma_emb = harness_cli.parse_natural_prompt("Gemma 4와 EmbeddingGemma 2로 로컬 멀티모달 RAG 워크숍 만들어줘")
        self.assertIn("gemma", p_gemma_emb["stack"].split(","))
        self.assertIn("embeddinggemma", p_gemma_emb["stack"].split(","))
        self.assertEqual(p_gemma_emb["model"], "gemma4:e4b")

        p_translate = harness_cli.parse_natural_prompt("TranslateGemma로 다국어 번역 핸즈온 만들어줘")
        self.assertEqual(p_translate["model"], "translategemma")
        self.assertIn("gemma", p_translate["stack"].split(","))

        # End-to-end prompt generation check (Claude + Gemma 4 / EmbeddingGemma 2)
        built_dir = harness_cli.generate_from_prompt(
            "클로드 최신 모델로 멀티 에이전트 워크숍 만들어줘",
            target_dir=str(self.temp_dir),
            init_only=True,
        )
        self.assertTrue(built_dir.exists())
        self.assertTrue((built_dir / "SETUP_GUIDE.md").exists())
        self.assertFalse((built_dir / "gemma4-local-setup-guide.md").exists())
        self.assertIn("anthropic>=2.8.0", (built_dir / "pyproject.toml").read_text(encoding="utf-8"))
        self.assertIn("Hands-on Lab (핸즈온 랩)", (built_dir / "README.md").read_text(encoding="utf-8"))
        self.assertIn("Runbook (런북)", (built_dir / "RUNBOOK.md").read_text(encoding="utf-8"))
        self.assertTrue(harness_cli.test_workshop(str(built_dir)))

        gemma_dir = harness_cli.generate_from_prompt(
            "Gemma 4와 EmbeddingGemma 2로 로컬 멀티모달 RAG 워크숍 만들어줘",
            target_dir=str(self.temp_dir),
            init_only=True,
        )
        self.assertTrue(gemma_dir.exists())
        gemma_final = (gemma_dir / "workshop" / "02_final" / "main.py").read_text(encoding="utf-8")
        self.assertIn("embed_with_embeddinggemma2", gemma_final)
        self.assertIn("embeddinggemma-2", gemma_final)
        self.assertTrue(harness_cli.test_workshop(str(gemma_dir)))

    def test_10_modular_package_and_language_detection(self):
        """Verify modular harness package structure, version sync, and KO/JA/ZH/EN prompt language detection."""
        from harness import auditors, exporters, registry, router, scaffolder

        self.assertTrue(hasattr(registry, "MODEL_REGISTRY"))
        self.assertTrue(hasattr(router, "parse_natural_prompt"))
        self.assertTrue(hasattr(scaffolder, "init_workshop"))
        self.assertTrue(hasattr(auditors, "audit_models"))
        self.assertTrue(hasattr(exporters, "generate_from_prompt"))

        self.assertEqual(router.detect_prompt_language("클로드로 실습 만들어줘"), "ko")
        self.assertEqual(router.detect_prompt_language("Claudeでハンズオンを作って"), "ja")
        self.assertEqual(router.detect_prompt_language("用Claude创建工作坊"), "zh")
        self.assertEqual(router.detect_prompt_language("Build a Claude agent workshop"), "en")


if __name__ == "__main__":
    unittest.main()
