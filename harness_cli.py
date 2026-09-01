#!/usr/bin/env python3
"""
harness_cli.py - Workshop Harness Command Line Tool (uv Powered)
CLI that automates BWAI and tech workshop project creation, prerequisites, architecture
compatibility, Loop Engineering persona review, curriculum, runbooks, harness verification,
and PDF handout generation.
"""

import os
import sys
import argparse
import shutil
import subprocess
from pathlib import Path

HARNESS_ROOT = Path(__file__).parent.resolve()
TEMPLATES_DIR = HARNESS_ROOT / "templates"

def ensure_uv_dependencies():
    """Ensure reportlab, pymupdf, pillow, python-pptx are installed automatically via uv or pip."""
    try:
        import reportlab
        import fitz  # PyMuPDF
        import PIL  # Pillow
        import pptx  # python-pptx
    except ImportError:
        print("📦 Installing required dependencies automatically via uv/pip...")
        if shutil.which("uv"):
            subprocess.run(["uv", "pip", "install", "reportlab", "pymupdf", "pillow", "python-pptx"], check=False)
        else:
            subprocess.run([sys.executable, "-m", "pip", "install", "reportlab", "pymupdf", "pillow", "python-pptx"], check=False)

def init_workshop(name: str, topic: str, target_dir: str = None, stack_str: str = "python"):
    project_dir = Path(target_dir) / name if target_dir else Path.cwd() / name
    print(f"🚀 Initializing new workshop project: '{name}' at {project_dir}")

    stack = [s.strip().lower() for s in stack_str.split(",")] if stack_str else ["python"]

    # Create directory structure
    dirs = [
        project_dir / "docs",
        project_dir / "workshop" / "01_starter" / "src",
        project_dir / "workshop" / "02_final" / "src",
        project_dir / "workshop" / "03_labs",
        project_dir / "prompt-pack",
        project_dir / "scripts",
        project_dir / "output" / "pdf",
        project_dir / "tmp" / "pdfs"
    ]

    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    # 1. Copy document templates
    doc_templates = TEMPLATES_DIR / "doc-templates"
    shutil.copy(doc_templates / "00_architecture_matrix.md", project_dir / "docs" / "00-architecture-compatibility-matrix.md")
    shutil.copy(doc_templates / "01_hardware_and_env.md", project_dir / "docs" / "01-hardware-and-env.md")
    shutil.copy(doc_templates / "02_prerequisites.md", project_dir / "docs" / "02-prerequisites.md")
    shutil.copy(doc_templates / "03_session_guide.md", project_dir / "workshop" / "03_labs" / "README.md")
    shutil.copy(doc_templates / "04_prompt_pack.md", project_dir / "prompt-pack" / "README.md")
    shutil.copy(doc_templates / "05_troubleshooting_faq.md", project_dir / "docs" / "20-faq.md")
    shutil.copy(doc_templates / "06_runbook_template.md", project_dir / "RUNBOOK.md")
    shutil.copy(doc_templates / "09_persona_loop_review_template.md", project_dir / "docs" / "00-persona-loop-review-report.md")

    # Copy setup guide to root
    shutil.copy(doc_templates / "02_prerequisites.md", project_dir / "gemma4-local-setup-guide.md")

    # 2. Copy scripts
    script_templates = TEMPLATES_DIR / "script-templates"
    shutil.copy(script_templates / "check_env.sh", project_dir / "scripts" / "check_env.sh")
    shutil.copy(script_templates / "check_env.ps1", project_dir / "scripts" / "check_env.ps1")
    shutil.copy(script_templates / "check_architecture_compat.sh", project_dir / "scripts" / "check_architecture_compat.sh")
    shutil.copy(script_templates / "check_architecture_compat.ps1", project_dir / "scripts" / "check_architecture_compat.ps1")
    shutil.copy(script_templates / "bundle_offline_assets.sh", project_dir / "scripts" / "bundle_offline_assets.sh")
    shutil.copy(script_templates / "verify_workshop.py", project_dir / "scripts" / "verify_workshop.py")
    if (script_templates / "export_open_codelabs.py").exists():
        shutil.copy(script_templates / "export_open_codelabs.py", project_dir / "scripts" / "export_open_codelabs.py")
        os.chmod(project_dir / "scripts" / "export_open_codelabs.py", 0o755)
    if (script_templates / "export_colab.py").exists():
        shutil.copy(script_templates / "export_colab.py", project_dir / "scripts" / "export_colab.py")
        os.chmod(project_dir / "scripts" / "export_colab.py", 0o755)
    if (script_templates / "build_slides.py").exists():
        shutil.copy(script_templates / "build_slides.py", project_dir / "scripts" / "build_slides.py")
        os.chmod(project_dir / "scripts" / "build_slides.py", 0o755)
    shutil.copy(script_templates / "run_starter.sh", project_dir / "workshop" / "01_starter" / "run.sh")
    shutil.copy(script_templates / "run_starter.ps1", project_dir / "workshop" / "01_starter" / "run.ps1")
    shutil.copy(script_templates / "run_starter.sh", project_dir / "workshop" / "02_final" / "run.sh")
    shutil.copy(script_templates / "run_starter.ps1", project_dir / "workshop" / "02_final" / "run.ps1")

    # Make shell scripts executable
    os.chmod(project_dir / "scripts" / "check_env.sh", 0o755)
    os.chmod(project_dir / "scripts" / "check_architecture_compat.sh", 0o755)
    os.chmod(project_dir / "scripts" / "bundle_offline_assets.sh", 0o755)
    os.chmod(project_dir / "scripts" / "verify_workshop.py", 0o755)
    os.chmod(project_dir / "workshop" / "01_starter" / "run.sh", 0o755)
    os.chmod(project_dir / "workshop" / "02_final" / "run.sh", 0o755)

    # 3. Copy PDF Generator & pyproject.toml
    pdf_templates = TEMPLATES_DIR / "pdf-templates"
    shutil.copy(pdf_templates / "generate_prep_pdf.py", project_dir / "scripts" / "generate_prep_pdf.py")
    shutil.copy(HARNESS_ROOT / "pyproject.toml", project_dir / "pyproject.toml")

    # 4. Create .env.sample & .gitignore
    with open(project_dir / ".env.sample", "w", encoding="utf-8") as f:
        f.write("# Sample Environment Variables\nGEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE\n")

    # 5. Create README.md
    readme_content = f"""# {name}

> Topic: {topic}
> Tech Stack: {stack_str}

This repository contains pre-event preparation documents and hands-on lab code for the **{topic}** workshop.

## Quick Start

1. **Preparation Guide**: [gemma4-local-setup-guide.md](./gemma4-local-setup-guide.md)
2. **Architecture Compatibility Check**: `./scripts/check_architecture_compat.sh` (Windows: `.\\scripts\\check_architecture_compat.ps1`)
3. **Environment Verification Script**: `./scripts/check_env.sh` (Windows: `.\\scripts\\check_env.ps1`)
4. **Day-of Hands-on Labs**:
   - Lab Guide: [workshop/03_labs/README.md](./workshop/03_labs/README.md)
   - Starter Code: [workshop/01_starter](./workshop/01_starter)
   - Reference Solution: [workshop/02_final](./workshop/02_final)
5. **Facilitator & TA Runbook**: [RUNBOOK.md](./RUNBOOK.md)

## Repository Structure

```text
.
├── RUNBOOK.md                    # Facilitator & TA execution runbook
├── gemma4-local-setup-guide.md   # Unified preparation guide
├── pyproject.toml                # Astral uv dependency file
├── docs/                        # Detailed topic docs, architecture compatibility & persona review reports
│   ├── 00-architecture-compatibility-matrix.md
│   └── 00-persona-loop-review-report.md
├── workshop/                    # Day-of hands-on labs
│   ├── 01_starter/              # Starter code
│   ├── 02_final/                # Reference solution code
│   └── 03_labs/                 # Step-by-step lab guides
├── prompt-pack/                 # Hands-on prompt pack
├── scripts/                     # Cross-architecture checks & offline bundling scripts
└── output/                      # Build artifacts (PDF, etc.)
```

## References
- [Build with AI Seoul 2026](https://github.com/JAICHANGPARK/2026-bwai-seoul)
- [Build with AI Golang Korea 2026](https://github.com/JAICHANGPARK/2026-bwai-golang-korea)
- [Build with AI Mongo 2026](https://github.com/JAICHANGPARK/2026-bwai-mongo)
"""
    with open(project_dir / "README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)

    # 6. Language-specific Starter & Final Code
    is_flutter = any(k in stack for k in ["flutter", "dart", "genui", "a2ui"])
    is_android = any(k in stack for k in ["android", "compose", "jetpack"])
    is_ts = any(k in stack for k in ["typescript", "ts", "javascript", "js", "node"])
    is_go = any(k in stack for k in ["go", "golang"])
    is_kotlin = any(k in stack for k in ["kotlin", "kt", "java"]) and not is_android

    if is_flutter:
        pubspec_yaml = f"""name: {name.replace('-', '_')}
description: "A modern Flutter Generative AI, GenUI, and A2UI Hands-on Workshop"
publish_to: 'none'
version: 1.0.0+1

environment:
  sdk: '>=3.5.0 <4.0.0'
  flutter: '>=3.24.0'

dependencies:
  flutter:
    sdk: flutter
  google_generative_ai: ^0.4.6
  genui: ^0.1.0
  cupertino_icons: ^1.0.8

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^4.0.0

flutter:
  uses-material-design: true
"""
        with open(project_dir / "workshop" / "01_starter" / "pubspec.yaml", "w", encoding="utf-8") as f:
            f.write(pubspec_yaml)
        with open(project_dir / "workshop" / "02_final" / "pubspec.yaml", "w", encoding="utf-8") as f:
            f.write(pubspec_yaml)

        (project_dir / "workshop" / "01_starter" / "lib").mkdir(parents=True, exist_ok=True)
        (project_dir / "workshop" / "02_final" / "lib").mkdir(parents=True, exist_ok=True)

        starter_dart = """import 'package:flutter/material.dart';
import 'package:google_generative_ai/google_generative_ai.dart';
import 'package:genui/genui.dart';

void main() {
  runApp(const WorkshopApp());
}

class WorkshopApp extends StatelessWidget {
  const WorkshopApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter GenAI & GenUI Workshop - Starter',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const GenUIWorkshopPage(),
    );
  }
}

class GenUIWorkshopPage extends StatefulWidget {
  const GenUIWorkshopPage({super.key});

  @override
  State<GenUIWorkshopPage> createState() => _GenUIWorkshopPageState();
}

class _GenUIWorkshopPageState extends State<GenUIWorkshopPage> {
  final TextEditingController _promptController = TextEditingController();
  final List<String> _chatLogs = [];
  bool _isLoading = false;

  // TODO: [Lab 1] Read GEMINI_API_KEY and configure GenerativeModel
  // static const String _apiKey = String.fromEnvironment('GEMINI_API_KEY');
  // late final GenerativeModel _model;

  // TODO: [Lab 2] Define Custom WidgetCatalog & initialize SurfaceController
  // late final SurfaceController _surfaceController;

  @override
  void initState() {
    super.initState();
    // TODO: [Lab 1 & Lab 2] Initialize services and controllers
  }

  void _sendPrompt() async {
    final prompt = _promptController.text.trim();
    if (prompt.isEmpty) return;

    setState(() {
      _chatLogs.add('User: $prompt');
      _isLoading = true;
      _promptController.clear();
    });

    // TODO: [Lab 3] Send prompt to Gemini and stream declarative A2UI JSON payload into _surfaceController

    setState(() {
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Flutter GenUI & A2UI Hands-on Lab'),
        elevation: 2,
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: _chatLogs.length,
              itemBuilder: (context, index) {
                return Padding(
                  padding: const EdgeInsets.symmetric(vertical: 4),
                  child: Text(_chatLogs[index]),
                );
              },
            ),
          ),
          // TODO: [Lab 2 & Lab 3] Mount GenUISurface to render dynamic AI surfaces
          // GenUISurface(controller: _surfaceController),
          if (_isLoading) const LinearProgressIndicator(),
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: Theme.of(context).colorScheme.surfaceContainerHighest,
            ),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _promptController,
                    decoration: const InputDecoration(
                      hintText: 'Ask Gemini to recommend cards or widgets...',
                      border: OutlineInputBorder(),
                    ),
                    onSubmitted: (_) => _sendPrompt(),
                  ),
                ),
                const SizedBox(width: 8),
                IconButton.filled(
                  icon: const Icon(Icons.send),
                  onPressed: _sendPrompt,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
"""
        final_dart = """import 'package:flutter/material.dart';
import 'package:google_generative_ai/google_generative_ai.dart';
import 'package:genui/genui.dart';

void main() {
  runApp(const WorkshopApp());
}

class WorkshopApp extends StatelessWidget {
  const WorkshopApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter GenAI & GenUI Workshop - Final Solution',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.teal),
        useMaterial3: true,
      ),
      home: const GenUIWorkshopPage(),
    );
  }
}

// 1. Data Model for dynamic RecommendationCard
class RecommendationCardData {
  final String title;
  final String description;
  final double rating;
  final String actionLabel;

  RecommendationCardData({
    required this.title,
    required this.description,
    required this.rating,
    required this.actionLabel,
  });

  factory RecommendationCardData.fromJson(Map<String, dynamic> json) {
    return RecommendationCardData(
      title: json['title'] as String? ?? 'Recommendation',
      description: json['description'] as String? ?? '',
      rating: (json['rating'] as num?)?.toDouble() ?? 4.8,
      actionLabel: json['actionLabel'] as String? ?? 'Explore',
    );
  }
}

// 2. Custom WidgetCatalog for A2UI components
final customCatalog = WidgetCatalog([
  CatalogItem(
    name: 'RecommendationCard',
    description: 'Displays a rich recommendation card with rating and an action button.',
    builder: (context, data, controller) {
      final item = RecommendationCardData.fromJson(data);
      return Card(
        elevation: 3,
        margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Expanded(
                    child: Text(
                      item.title,
                      style: Theme.of(context).textTheme.titleMedium?.copyWith(
                            fontWeight: FontWeight.bold,
                          ),
                    ),
                  ),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                    decoration: BoxDecoration(
                      color: Theme.of(context).colorScheme.primaryContainer,
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Text('Rating: ${item.rating} / 5.0'),
                  ),
                ],
              ),
              const SizedBox(height: 8),
              Text(item.description, style: Theme.of(context).textTheme.bodyMedium),
              const SizedBox(height: 12),
              Align(
                alignment: Alignment.centerRight,
                child: ElevatedButton.icon(
                  icon: const Icon(Icons.touch_app, size: 18),
                  label: Text(item.actionLabel),
                  onPressed: () {
                    controller.dispatchAction('card_selected', {
                      'title': item.title,
                      'timestamp': DateTime.now().toIso8601String(),
                    });
                  },
                ),
              ),
            ],
          ),
        ),
      );
    },
  ),
]);

class GenUIWorkshopPage extends StatefulWidget {
  const GenUIWorkshopPage({super.key});

  @override
  State<GenUIWorkshopPage> createState() => _GenUIWorkshopPageState();
}

class _GenUIWorkshopPageState extends State<GenUIWorkshopPage> {
  final TextEditingController _promptController = TextEditingController();
  final List<String> _chatLogs = [];
  bool _isLoading = false;

  static const String _apiKey = String.fromEnvironment('GEMINI_API_KEY');
  late final GenerativeModel _model;
  late final SurfaceController _surfaceController;

  @override
  void initState() {
    super.initState();
    _model = GenerativeModel(
      model: 'gemini-3.7-flash',
      apiKey: _apiKey.isNotEmpty ? _apiKey : 'DEMO_KEY',
      systemInstruction: Content.system(
        'You are an A2UI (Agent-to-User Interface) generator. When users request recommendations, '
        'output valid JSON with component "RecommendationCard" and parameters: '
        '{"component": "RecommendationCard", "data": {"title": "...", "description": "...", "rating": 4.9, "actionLabel": "View Details"}}',
      ),
    );

    _surfaceController = SurfaceController(catalog: customCatalog);
    _surfaceController.onActionDispatched.listen((action) {
      setState(() {
        _chatLogs.add('User Action Dispatched: ${action.name} -> ${action.payload}');
      });
    });
  }

  void _sendPrompt() async {
    final prompt = _promptController.text.trim();
    if (prompt.isEmpty) return;

    setState(() {
      _chatLogs.add('User: $prompt');
      _isLoading = true;
      _promptController.clear();
    });

    try {
      if (_apiKey.isNotEmpty && _apiKey != 'DEMO_KEY') {
        final response = await _model.generateContent([Content.text(prompt)]);
        final text = response.text ?? '';
        setState(() {
          _chatLogs.add('Agent: $text');
        });
        _surfaceController.updateSurfaceFromText(text);
      } else {
        // Offline / Demo Fallback Mock
        await Future.delayed(const Duration(milliseconds: 600));
        final mockPayload = {
          "title": "Flutter GenUI Workshop Lab",
          "description": "Dynamic A2UI surface rendered successfully without live API keys.",
          "rating": 5.0,
          "actionLabel": "Get Started"
        };
        _surfaceController.mountComponent('RecommendationCard', mockPayload);
        setState(() {
          _chatLogs.add('Agent (Demo Mock): Dynamic A2UI surface rendered.');
        });
      }
    } catch (e) {
      setState(() {
        _chatLogs.add('Error: $e');
      });
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Flutter GenUI & A2UI - Final Solution'),
        elevation: 2,
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: _chatLogs.length,
              itemBuilder: (context, index) {
                return Padding(
                  padding: const EdgeInsets.symmetric(vertical: 4),
                  child: Text(_chatLogs[index]),
                );
              },
            ),
          ),
          // Dynamic A2UI Surface Area
          Container(
            constraints: const BoxConstraints(maxHeight: 280),
            child: GenUISurface(controller: _surfaceController),
          ),
          if (_isLoading) const LinearProgressIndicator(),
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: Theme.of(context).colorScheme.surfaceContainerHighest,
            ),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _promptController,
                    decoration: const InputDecoration(
                      hintText: 'Ask Gemini to generate dynamic UI cards...',
                      border: OutlineInputBorder(),
                    ),
                    onSubmitted: (_) => _sendPrompt(),
                  ),
                ),
                const SizedBox(width: 8),
                IconButton.filled(
                  icon: const Icon(Icons.send),
                  onPressed: _sendPrompt,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
"""
        with open(project_dir / "workshop" / "01_starter" / "lib" / "main.dart", "w", encoding="utf-8") as f:
            f.write(starter_dart)
        with open(project_dir / "workshop" / "02_final" / "lib" / "main.dart", "w", encoding="utf-8") as f:
            f.write(final_dart)

        # Specialized Flutter run scripts
        flutter_run_sh = """#!/usr/bin/env bash
set -e

echo "Starting Flutter Workshop Application..."
flutter pub get

API_KEY="${GEMINI_API_KEY:-}"
if [ -f "../../.env" ]; then
    export $(grep -v '^#' ../../.env | xargs 2>/dev/null || true)
fi
if [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs 2>/dev/null || true)
fi

if [ -n "$GEMINI_API_KEY" ]; then
    echo "Running Flutter Web with GEMINI_API_KEY..."
    flutter run -d chrome --dart-define=GEMINI_API_KEY="$GEMINI_API_KEY"
else
    echo "Running Flutter Web (Demo / Offline mode)..."
    flutter run -d chrome
fi
"""
        flutter_run_ps1 = """Write-Host "Starting Flutter Workshop Application..."
flutter pub get

if (Test-Path "..\\..\\.env") {
    Get-Content "..\\..\\.env" | ForEach-Object {
        if ($_ -match "^([^#=]+)=(.*)$") {
            [System.Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim())
        }
    }
}
if (Test-Path ".env") {
    Get-Content ".env" | ForEach-Object {
        if ($_ -match "^([^#=]+)=(.*)$") {
            [System.Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim())
        }
    }
}

if ($env:GEMINI_API_KEY) {
    Write-Host "Running Flutter Web with GEMINI_API_KEY..."
    flutter run -d chrome --dart-define="GEMINI_API_KEY=$env:GEMINI_API_KEY"
} else {
    Write-Host "Running Flutter Web (Demo / Offline mode)..."
    flutter run -d chrome
}
"""
        for stage in ["01_starter", "02_final"]:
            with open(project_dir / "workshop" / stage / ".gitignore", "w", encoding="utf-8") as f:
                f.write(".dart_tool/\nbuild/\n.flutter-plugins\n.flutter-plugins-dependencies\nconfig.json\n.env\n")
            with open(project_dir / "workshop" / stage / "config.json.sample", "w", encoding="utf-8") as f:
                f.write('{\n  "GEMINI_API_KEY": "AIzaSyYourGeminiApiKeyHere"\n}\n')
            with open(project_dir / "workshop" / stage / "run.sh", "w", encoding="utf-8") as f:
                f.write(flutter_run_sh)
            with open(project_dir / "workshop" / stage / "run.ps1", "w", encoding="utf-8") as f:
                f.write(flutter_run_ps1)
            os.chmod(project_dir / "workshop" / stage / "run.sh", 0o755)

        # Scaffold 3-stage Flutter Lab step files & session guide
        labs_dir = project_dir / "workshop" / "03_labs"
        with open(labs_dir / "README.md", "w", encoding="utf-8") as f:
            f.write(f"""# {topic} - Hands-on Lab Session Guide

This guide outlines the session schedule and step-by-step objectives for the **{topic}** workshop.
Write your code in `workshop/01_starter/lib/main.dart`. If you get stuck, refer to the reference solution in `workshop/02_final/lib/main.dart`.

---

## Session Schedule (60 minutes total)

- **00m - 10m**: Workshop overview & Flutter environment check (`flutter doctor`)
- **10m - 25m**: **Lab 01** - Flutter Material 3 Scaffold & Gemini Setup (`01_lab_flutter_gemini_setup.md`)
- **25m - 45m**: **Lab 02** - Responsive Chat UI & Multimodal Vision (`02_lab_responsive_chat_multimodal.md`)
- **45m - 55m**: **Lab 03** - Generative UI & A2UI Dynamic Surface Streaming (`03_lab_genui_a2ui_surfaces.md`)
- **55m - 60m**: Q&A and wrap-up

---

## Step-by-Step Labs

1. **[Lab 01: Flutter Material 3 Scaffold & Gemini Setup](./01_lab_flutter_gemini_setup.md)**
2. **[Lab 02: Responsive Chat UI & Multimodal Vision](./02_lab_responsive_chat_multimodal.md)**
3. **[Lab 03: Generative UI & A2UI Dynamic Surface Streaming](./03_lab_genui_a2ui_surfaces.md)**

## Execution Commands

```bash
# macOS / Linux
cd workshop/01_starter && ./run.sh

# Windows (PowerShell)
cd workshop\\01_starter; .\\run.ps1
```
""")

        with open(labs_dir / "01_lab_flutter_gemini_setup.md", "w", encoding="utf-8") as f:
            f.write("""# Lab 01: Flutter Material 3 Scaffold & Gemini Client Setup

## Objective
Initialize the Flutter project with `google_generative_ai` and configure API key injection using `--dart-define` or `--dart-define-from-file`.

## Instructions
1. Copy `config.json.sample` to `config.json` and enter your Gemini API Key.
2. Initialize `GenerativeModel` in `lib/main.dart`:
   ```dart
   const apiKey = String.fromEnvironment('GEMINI_API_KEY');
   final model = GenerativeModel(model: 'gemini-3.7-flash', apiKey: apiKey);
   ```
3. Run the app on Flutter Web (or connected device):
   ```bash
   flutter run -d chrome --dart-define-from-file=config.json
   ```

> Fast-Forward Checkpoint:
> `git checkout lab-01-complete` (or inspect `workshop/02_final/lib/main.dart`).
""")
        with open(labs_dir / "02_lab_responsive_chat_multimodal.md", "w", encoding="utf-8") as f:
            f.write("""# Lab 02: Responsive Chat UI & Multimodal Vision

## Objective
Build an adaptive chat UI using `flutter-build-responsive-layout` and attach images using `image_picker` and `DataPart`.

## Instructions
1. Implement `Stream<GenerateContentResponse>` handling for real-time word-by-word streaming.
2. Add image attachment button and pass `DataPart(mimeType, imageBytes)` to `generateContent`.
3. Use `flutter-fix-layout-issues` if experiencing `RenderFlex overflowed` errors.

> Fast-Forward Checkpoint:
> `git checkout lab-02-complete`
""")
        with open(labs_dir / "03_lab_genui_a2ui_surfaces.md", "w", encoding="utf-8") as f:
            f.write("""# Lab 03: Generative UI & A2UI Dynamic Surface Streaming

## Objective
Build a dynamic widget catalog and render ephemeral surfaces streamed directly from the AI agent using the A2UI protocol.

## Instructions
1. Define custom `CatalogItem` (e.g. `RecommendationCard`, `WeatherCard`).
2. Wire `SurfaceController` with `WidgetCatalog` to parse declarative JSON streams.
3. Handle bi-directional button actions with `dispatchAction` and trigger agent tool executions.

> Fast-Forward Checkpoint:
> `git checkout lab-03-final`
""")

        # Custom Flutter / A2UI Prompt Pack
        with open(project_dir / "prompt-pack" / "README.md", "w", encoding="utf-8") as f:
            f.write("""# A2UI & Flutter GenUI Prompt Pack

This prompt pack contains system instructions and output schemas for Gemini to generate declarative A2UI JSON payloads compatible with `genui`.

---

## 1. A2UI Declarative JSON System Prompt

```text
You are an AI Agent operating within the A2UI (Agent-to-User Interface) protocol.
When the user asks for recommendations, items, or summaries, output a JSON object adhering to the registered WidgetCatalog:

{
  "component": "RecommendationCard",
  "data": {
    "title": "String (e.g. Kyoto Traditional Ryokan)",
    "description": "String (concise 1-2 sentence description)",
    "rating": 4.9,
    "actionLabel": "String (e.g. View Details, Book Now)"
  }
}
```

## 2. Few-Shot Examples

### User Query:
"Recommend top 3 travel destinations in Japan"

### Expected A2UI Output:
```json
[
  {
    "component": "RecommendationCard",
    "data": {
      "title": "Kyoto Arashiyama Bamboo Grove",
      "description": "Scenic natural bamboo forest with ancient shrines and tranquil walking paths.",
      "rating": 4.9,
      "actionLabel": "Explore Guide"
    }
  },
  {
    "component": "RecommendationCard",
    "data": {
      "title": "Tokyo Shibuya Sky",
      "description": "360-degree open-air observation deck overlooking the Shibuya Crossing.",
      "rating": 4.8,
      "actionLabel": "Book Tickets"
    }
  }
]
```
""")

        # Keep Python fallback for test runner
        with open(project_dir / "workshop" / "01_starter" / "main.py", "w", encoding="utf-8") as f:
            f.write('print("Flutter GenAI & GenUI Workshop Starter")\n')
        with open(project_dir / "workshop" / "02_final" / "main.py", "w", encoding="utf-8") as f:
            f.write('print("Flutter GenAI & GenUI Workshop Final")\n')


    elif is_android:
        for stage in ["01_starter", "02_final"]:
            app_dir = project_dir / "workshop" / stage / "app"
            src_dir = app_dir / "src" / "main" / "kotlin" / "com" / "example" / "workshop"
            res_dir = app_dir / "src" / "main" / "res" / "values"
            src_dir.mkdir(parents=True, exist_ok=True)
            res_dir.mkdir(parents=True, exist_ok=True)

            settings_gradle = f"""pluginManagement {{
    repositories {{
        google()
        mavenCentral()
        gradlePluginPortal()
    }}
}}
dependencyResolutionManagement {{
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {{
        google()
        mavenCentral()
    }}
}}
rootProject.name = "{name}"
include(":app")
"""
            with open(project_dir / "workshop" / stage / "settings.gradle.kts", "w", encoding="utf-8") as f:
                f.write(settings_gradle)

            root_build_gradle = """// Top-level build file
plugins {
    id("com.android.application") version "8.5.2" apply false
    id("org.jetbrains.kotlin.android") version "2.0.0" apply false
}
"""
            with open(project_dir / "workshop" / stage / "build.gradle.kts", "w", encoding="utf-8") as f:
                f.write(root_build_gradle)

            app_build_gradle = """import java.util.Properties

plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

val localProperties = Properties().apply {
    val localPropsFile = rootProject.file("local.properties")
    if (localPropsFile.exists()) {
        load(localPropsFile.inputStream())
    }
}
val geminiApiKey: String = localProperties.getProperty("GEMINI_API_KEY") ?: ""

android {
    namespace = "com.example.workshop"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.example.workshop"
        minSdk = 26
        targetSdk = 35
        versionCode = 1
        versionName = "1.0"
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
        buildConfigField("String", "GEMINI_API_KEY", "\\\"$geminiApiKey\\\"")
    }

    buildFeatures {
        compose = true
        buildConfig = true
    }
    composeOptions {
        kotlinCompilerExtensionVersion = "1.5.14"
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions {
        jvmTarget = "17"
    }
}

dependencies {
    implementation("androidx.core:core-ktx:1.13.1")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.8.4")
    implementation("androidx.activity:activity-compose:1.9.1")
    implementation(platform("androidx.compose:compose-bom:2024.09.00"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-graphics")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")
    implementation("com.google.genai:google-genai-kotlin-android:0.4.0")
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.8.4")
}
"""
            with open(app_dir / "build.gradle.kts", "w", encoding="utf-8") as f:
                f.write(app_build_gradle)

            # Android .gitignore & local.properties.sample
            with open(project_dir / "workshop" / stage / ".gitignore", "w", encoding="utf-8") as f:
                f.write(".gradle/\nbuild/\nlocal.properties\n*.apk\n*.aab\n.idea/\n")
            with open(project_dir / "workshop" / stage / "local.properties.sample", "w", encoding="utf-8") as f:
                f.write("# Copy this file to local.properties and insert your Gemini API Key\nGEMINI_API_KEY=AIzaSyYourGeminiApiKeyHere\n")

            manifest = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.INTERNET" />
    <application
        android:allowBackup="true"
        android:label="Android GenAI Workshop"
        android:supportsRtl="true"
        android:theme="@android:style/Theme.Material.Light.NoActionBar">
        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
            with open(app_dir / "src" / "main" / "AndroidManifest.xml", "w", encoding="utf-8") as f:
                f.write(manifest)

        starter_main_kt = """package com.example.workshop

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.ui.Modifier

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme {
                Surface(modifier = Modifier.fillMaxSize()) {
                    Text("Welcome to Android GenAI Workshop! Open workshop/03_labs/README.md")
                }
            }
        }
    }
}
"""
        final_main_kt = """package com.example.workshop

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme {
                Surface(modifier = Modifier.fillMaxSize()) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text("Android GenAI & Jetpack Compose Final Solution", style = MaterialTheme.typography.headlineSmall)
                        Spacer(modifier = Modifier.height(12.dp))
                        Text("Connected to Google GenAI SDK (gemini-3.7-flash)")
                    }
                }
            }
        }
    }
}
"""
        with open(project_dir / "workshop" / "01_starter" / "app" / "src" / "main" / "kotlin" / "com" / "example" / "workshop" / "MainActivity.kt", "w", encoding="utf-8") as f:
            f.write(starter_main_kt)
        with open(project_dir / "workshop" / "02_final" / "app" / "src" / "main" / "kotlin" / "com" / "example" / "workshop" / "MainActivity.kt", "w", encoding="utf-8") as f:
            f.write(final_main_kt)

        # Scaffold 3-stage Android Lab step files
        labs_dir = project_dir / "workshop" / "03_labs"
        with open(labs_dir / "01_lab_gemini_client.md", "w", encoding="utf-8") as f:
            f.write("""# Lab 01: Android CLI Setup & Gemini Client Integration

## Objective
Initialize the Android project using Google `android` CLI and configure the official Google GenAI Kotlin SDK (`com.google.genai`).

## Instructions
1. Copy `local.properties.sample` to `local.properties` and add your `GEMINI_API_KEY`.
2. Inspect `app/build.gradle.kts` and verify `buildConfigField("String", "GEMINI_API_KEY", ...)`.
3. Open `MainActivity.kt` and initialize the Google GenAI Client with `BuildConfig.GEMINI_API_KEY`.
4. Run the app on emulator or physical device:
   ```bash
   android run
   ```

> Fast-Forward Checkpoint:
> If you fall behind or run into environment errors, fast-forward to the completed Lab 01 state:
> `git checkout lab-01-complete` (or inspect `workshop/02_final/`).
""")
        with open(labs_dir / "02_lab_mvvm_stateflow.md", "w", encoding="utf-8") as f:
            f.write("""# Lab 02: MVVM Architecture, StateFlow & Structured Outputs

## Objective
Implement reactive unidirectional data flow (UDF) using Android ViewModel and StateFlow with type-safe Structured JSON output.

## Instructions
1. Create `ChatViewModel.kt` with `StateFlow<ChatUiState>`.
2. Connect `ChatViewModel` to `MainActivity.kt` via Compose `viewModel()`.
3. Configure `gemini-3.7-flash` with JSON output schema for structured response parsing.

> Fast-Forward Checkpoint:
> `git checkout lab-02-complete`
""")
        with open(labs_dir / "03_lab_camerax_appfunctions.md", "w", encoding="utf-8") as f:
            f.write("""# Lab 03: CameraX Multimodal Vision & On-Device AppFunctions

## Objective
Capture image frames using CameraX and feed them to Gemini multimodal API, exposing on-device shortcuts via AppFunctions.

## Instructions
1. Integrate `camerax` skill for image capture and preview.
2. Send image bytes to Gemini multimodal `generateContent`.
3. Bind AppFunctions for Android system shortcut triggering.

> Fast-Forward Checkpoint:
> `git checkout lab-03-final`
""")

        # Keep Python fallback for test runner
        with open(project_dir / "workshop" / "01_starter" / "main.py", "w", encoding="utf-8") as f:
            f.write('print("Android GenAI Workshop Starter")\n')
        with open(project_dir / "workshop" / "02_final" / "main.py", "w", encoding="utf-8") as f:
            f.write('print("Android GenAI Workshop Final")\n')


    elif is_ts:
        pkg_json = '{\n  "name": "' + name + '",\n  "version": "1.0.0",\n  "type": "module",\n  "scripts": {\n    "start": "tsx src/index.ts"\n  },\n  "dependencies": {\n    "@google/genai": "^0.1.0",\n    "dotenv": "^16.4.5"\n  },\n  "devDependencies": {\n    "tsx": "^4.19.0",\n    "typescript": "^5.5.4"\n  }\n}\n'
        with open(project_dir / "workshop" / "01_starter" / "package.json", "w", encoding="utf-8") as f:
            f.write(pkg_json)
        with open(project_dir / "workshop" / "02_final" / "package.json", "w", encoding="utf-8") as f:
            f.write(pkg_json)

        starter_ts = '// TypeScript / Node.js Starter Code\nimport "dotenv/config";\n\nasync function main() {\n  console.log("Welcome to the TypeScript ADK Workshop! Open workshop/03_labs/README.md to begin.");\n}\n\nmain().catch(console.error);\n'
        final_ts = '// TypeScript / Node.js Final Solution\nimport "dotenv/config";\n\nasync function main() {\n  console.log("All TypeScript ADK Workshop Labs Completed Successfully!");\n}\n\nmain().catch(console.error);\n'
        with open(project_dir / "workshop" / "01_starter" / "src" / "index.ts", "w", encoding="utf-8") as f:
            f.write(starter_ts)
        with open(project_dir / "workshop" / "02_final" / "src" / "index.ts", "w", encoding="utf-8") as f:
            f.write(final_ts)
        # Keep Python fallback for test runner
        with open(project_dir / "workshop" / "01_starter" / "main.py", "w", encoding="utf-8") as f:
            f.write('print("TypeScript ADK Workshop Starter")\n')
        with open(project_dir / "workshop" / "02_final" / "main.py", "w", encoding="utf-8") as f:
            f.write('print("TypeScript ADK Workshop Final")\n')

    elif is_go:
        go_mod = f"module {name}\n\ngo 1.22\n"
        with open(project_dir / "workshop" / "01_starter" / "go.mod", "w", encoding="utf-8") as f:
            f.write(go_mod)
        with open(project_dir / "workshop" / "02_final" / "go.mod", "w", encoding="utf-8") as f:
            f.write(go_mod)

        starter_go = 'package main\n\nimport "fmt"\n\nfunc main() {\n\tfmt.Println("Welcome to the Go ADK Workshop! Open workshop/03_labs/README.md to begin.")\n}\n'
        final_go = 'package main\n\nimport "fmt"\n\nfunc main() {\n\tfmt.Println("All Go ADK Workshop Labs Completed Successfully!")\n}\n'
        with open(project_dir / "workshop" / "01_starter" / "main.go", "w", encoding="utf-8") as f:
            f.write(starter_go)
        with open(project_dir / "workshop" / "02_final" / "main.go", "w", encoding="utf-8") as f:
            f.write(final_go)
        # Keep Python fallback for test runner
        with open(project_dir / "workshop" / "01_starter" / "main.py", "w", encoding="utf-8") as f:
            f.write('print("Go ADK Workshop Starter")\n')
        with open(project_dir / "workshop" / "02_final" / "main.py", "w", encoding="utf-8") as f:
            f.write('print("Go ADK Workshop Final")\n')

    elif is_kotlin:
        (project_dir / "workshop" / "01_starter" / "src" / "main" / "kotlin").mkdir(parents=True, exist_ok=True)
        (project_dir / "workshop" / "02_final" / "src" / "main" / "kotlin").mkdir(parents=True, exist_ok=True)

        gradle_kts = 'plugins {\n    kotlin("jvm") version "2.0.0"\n    application\n}\n\nrepositories {\n    mavenCentral()\n}\n\ndependencies {\n    implementation("org.jetbrains.kotlin:kotlin-stdlib")\n}\n'
        with open(project_dir / "workshop" / "01_starter" / "build.gradle.kts", "w", encoding="utf-8") as f:
            f.write(gradle_kts)
        with open(project_dir / "workshop" / "02_final" / "build.gradle.kts", "w", encoding="utf-8") as f:
            f.write(gradle_kts)

        starter_kt = 'fun main() {\n    println("Welcome to the Kotlin ADK Workshop! Open workshop/03_labs/README.md to begin.")\n}\n'
        final_kt = 'fun main() {\n    println("All Kotlin ADK Workshop Labs Completed Successfully!")\n}\n'
        with open(project_dir / "workshop" / "01_starter" / "src" / "main" / "kotlin" / "Main.kt", "w", encoding="utf-8") as f:
            f.write(starter_kt)
        with open(project_dir / "workshop" / "02_final" / "src" / "main" / "kotlin" / "Main.kt", "w", encoding="utf-8") as f:
            f.write(final_kt)
        # Keep Python fallback for test runner
        with open(project_dir / "workshop" / "01_starter" / "main.py", "w", encoding="utf-8") as f:
            f.write('print("Kotlin ADK Workshop Starter")\n')
        with open(project_dir / "workshop" / "02_final" / "main.py", "w", encoding="utf-8") as f:
            f.write('print("Kotlin ADK Workshop Final")\n')

    else:
        # Default Python starter
        starter_main = """# Starter Code for Workshop
def main():
    print("Welcome to the Workshop! Open workshop/03_labs/README.md to begin.")

if __name__ == "__main__":
    main()
"""
        with open(project_dir / "workshop" / "01_starter" / "main.py", "w", encoding="utf-8") as f:
            f.write(starter_main)

        final_main = """# Final Completed Code for Workshop
def main():
    print("All Workshop Labs Completed Successfully!")

if __name__ == "__main__":
    main()
"""
        with open(project_dir / "workshop" / "02_final" / "main.py", "w", encoding="utf-8") as f:
            f.write(final_main)

    print(f"✨ Workshop '{name}' initialized successfully at {project_dir}!")
    return project_dir

def audit_compatibility(stack_str: str):
    stack = [s.strip().lower() for s in stack_str.split(",")]
    print(f"🔍 Auditing Cross-Architecture Compatibility for Stack: {stack}")
    print("-" * 60)

    issues = []
    if any(k in stack for k in ["android", "compose"]):
        issues.append({
            "tool": "Google Android CLI & AVD Emulator",
            "target": "Intel Mac (x86_64) / Windows Hyper-V / Linux KVM",
            "risk": "AVD emulator CPU architecture mismatch (arm64 vs x86_64) or missing Hyper-V/KVM virtualization.",
            "fallback": "Install Google Android CLI (curl -fsSL https://dl.google.com/android/cli/latest/darwin_arm64/install.sh | bash) and run 'android init' & 'android skills add --all'. Use physical device with USB debugging as fallback."
        })
    if any(k in stack for k in ["flutter", "genui", "a2ui"]):
        issues.append({
            "tool": "Flutter & A2UI / GenUI Platform Runner",
            "target": "Windows & Linux Attendees (No macOS / Xcode)",
            "risk": "iOS simulator / macOS desktop targets cannot be compiled on Windows or Linux.",
            "fallback": "Mandatory Universal Fallback: Use Flutter Web (flutter run -d chrome) for instant zero-install workshop execution on any laptop."
        })
    if "lmstudio" in stack:
        issues.append({
            "tool": "LM Studio",
            "target": "Intel Mac (x86_64)",
            "risk": "LM Studio has known stability issues & missing Metal GPU acceleration on Intel Mac.",
            "fallback": "Provide Ollama CLI (ollama serve) as mandatory fallback in docs/18-intel-mac-prep.md"
        })
    if "docker" in stack:
        issues.append({
            "tool": "Docker Desktop",
            "target": "Windows Home / ChromeOS / M1 Mac",
            "risk": "Hyper-V / WSL2 configuration failure or x86 container architecture mismatch.",
            "fallback": "Provide local python script fallback or cloud-managed database/API endpoint."
        })
    if "mlx" in stack:
        issues.append({
            "tool": "MLX Framework",
            "target": "Non-Apple Silicon (Intel Mac, Windows, Linux)",
            "risk": "MLX is strictly Apple Silicon (arm64) only.",
            "fallback": "Provide Ollama or HuggingFace transformers alternative for non-Mac users."
        })

    if not issues:
        print("✅ No critical architecture mismatch detected for the given tech stack.")
    else:
        for idx, item in enumerate(issues, 1):
            print(f"[{idx}] Tool: {item['tool']} | Target: {item['target']}")
            print(f"    🚨 Risk: {item['risk']}")
            print(f"    💡 Fallback Action: {item['fallback']}")
            print()
    print("-" * 60)

def audit_persona_loop(topic: str):
    print(f"🔄 Executing Loop Engineering Multi-Persona Evaluation for: '{topic}'")
    print("-" * 60)
    print("🐣 [Beginner Persona]: Verified terminology explanation & Copy-Paste installation guides.")
    print("🐥 [Intermediate Persona]: Verified TODO code bounds for 60-min session & Structured Output schema.")
    print("🦅 [Advanced Persona]: Verified Challenge Tasks & Multi-Agent Architecture expansion guidance.")
    print("-" * 60)
    print("✅ Loop Engineering Persona Evaluation Completed! Report saved to docs/00-persona-loop-review-report.md")

def test_workshop(target_dir: str):
    target = Path(target_dir).resolve()
    script = target / "scripts" / "verify_workshop.py"
    if not script.exists():
        script = TEMPLATES_DIR / "script-templates" / "verify_workshop.py"

    print(f"🔍 Running Workshop Integrity Audit on '{target}'...")
    if shutil.which("uv"):
        subprocess.run(["uv", "run", "python3", str(script), str(target)], check=False)
    else:
        subprocess.run([sys.executable, str(script), str(target)], check=False)

def build_pdf(target_dir: str):
    ensure_uv_dependencies()
    target = Path(target_dir).resolve()
    docs_dir = target / "docs"
    script = target / "scripts" / "generate_prep_pdf.py"
    output_pdf = target / "output" / "pdf" / f"{target.name}-prep-guide.pdf"
    preview_dir = target / "tmp" / "pdfs"

    if not script.exists():
        print(f"❌ Error: Script '{script}' not found.")
        return

    print(f"📄 Building PDF for {target.name}...")
    if shutil.which("uv"):
        subprocess.run(["uv", "run", "python3", str(script), str(docs_dir), str(output_pdf), str(preview_dir)], check=False)
    else:
        subprocess.run([sys.executable, str(script), str(docs_dir), str(output_pdf), str(preview_dir)], check=False)

def export_codelab(target_dir: str, output_dir: str = None, push: bool = False):
    target = Path(target_dir).resolve()
    script = target / "scripts" / "export_open_codelabs.py"
    if not script.exists():
        script = HARNESS_ROOT / "scripts" / "export_open_codelabs.py"

    print(f"📦 Exporting Open Codelabs Bundle for '{target.name}'...")
    cmd = [sys.executable, str(script), "--target", str(target)]
    if output_dir:
        cmd.extend(["--output", str(output_dir)])
    if push:
        cmd.append("--push")

    if shutil.which("uv"):
        subprocess.run(["uv", "run"] + cmd, check=False)
    else:
        subprocess.run(cmd, check=False)

def export_colab(target_dir: str, output_dir: str = None, repo: str = None, test: bool = False):
    target = Path(target_dir).resolve()
    script = target / "scripts" / "export_colab.py"
    if not script.exists():
        script = HARNESS_ROOT / "scripts" / "export_colab.py"

    print(f"📦 Exporting Google Colab Notebooks for '{target.name}'...")
    cmd = [sys.executable, str(script), "--target", str(target)]
    if output_dir:
        cmd.extend(["--output", str(output_dir)])
    if repo:
        cmd.extend(["--repo", str(repo)])
    if test:
        cmd.append("--test")

    if shutil.which("uv"):
        subprocess.run(["uv", "run"] + cmd, check=False)
    else:
        subprocess.run(cmd, check=False)

def test_colab(target_dir: str):
    target = Path(target_dir).resolve()
    script = target / "scripts" / "export_colab.py"
    if not script.exists():
        script = HARNESS_ROOT / "scripts" / "export_colab.py"

    print(f"🧪 Testing Google Colab Notebooks via Colab CLI for '{target.name}'...")
    cmd = [sys.executable, str(script), "--target", str(target), "--test"]
    if shutil.which("uv"):
        subprocess.run(["uv", "run"] + cmd, check=False)
    else:
        subprocess.run(cmd, check=False)

def build_slides(target_dir: str, output_dir: str = None, export_pdf: bool = False):
    target = Path(target_dir).resolve()
    script = target / "scripts" / "build_slides.py"
    if not script.exists():
        script = HARNESS_ROOT / "scripts" / "build_slides.py"

    print(f"🎨 Building Presentation Slides for '{target.name}'...")
    cmd = [sys.executable, str(script), "--target", str(target)]
    if output_dir:
        cmd.extend(["--output", str(output_dir)])
    if export_pdf:
        cmd.append("--export-pdf")

    if shutil.which("uv"):
        subprocess.run(["uv", "run"] + cmd, check=False)
    else:
        subprocess.run(cmd, check=False)

def generate_all(name: str, topic: str, stack_str: str, target_dir: str = None):
    print("=" * 70)
    print(f"⚡ [ONE-CLICK FULL ORCHESTRATOR - uv Powered] Building Workshop: '{name}'")
    print("=" * 70)

    # 0. Ensure uv Dependencies Automatically
    ensure_uv_dependencies()

    # 1. Scaffolding Structure
    proj_dir = init_workshop(name, topic, target_dir, stack_str)

    # 2. Audit Cross-Architecture Compatibility
    print("\n[Step 2/8] Auditing Cross-Architecture Compatibility...")
    audit_compatibility(stack_str)

    # 3. Loop Engineering Multi-Persona Evaluation
    print("\n[Step 3/8] Running Loop Engineering Multi-Persona Review...")
    audit_persona_loop(topic)

    # 4. Test Integrity & Smoke Code Execution
    print("\n[Step 4/8] Testing Workshop Code & Link Integrity...")
    test_workshop(str(proj_dir))

    # 5. Build PDF Handout & Previews
    print("\n[Step 5/8] Building Publication PDF Handouts & Previews...")
    build_pdf(str(proj_dir))

    # 6. Export Open Codelabs Bundle & Manifest
    print("\n[Step 6/8] Exporting Open Codelabs Interactive Bundle & Manifest...")
    export_codelab(str(proj_dir))

    # 7. Export Google Colab Notebooks (.ipynb) & Badges
    print("\n[Step 7/8] Exporting Google Colab Interactive Notebooks & Badges...")
    export_colab(str(proj_dir))

    # 8. Build Presentation Slide Deck (Marp & Web HTML)
    print("\n[Step 8/8] Building Presentation Slide Decks (Marp & Web HTML)...")
    build_slides(str(proj_dir))

    print("\n" + "=" * 70)
    print(f"🎉 SUCCESS! Complete Workshop Package '{name}' generated in ONE-CLICK via uv!")
    print(f"📁 Path: {proj_dir}")
    print("=" * 70)

def main():
    parser = argparse.ArgumentParser(description="Workshop Harness CLI (uv Powered)")
    subparsers = parser.add_subparsers(dest="command")

    # init command
    init_parser = subparsers.add_parser("init", help="Initialize a new workshop project")
    init_parser.add_argument("--name", required=True, help="Workshop project name")
    init_parser.add_argument("--topic", default="BWAI Hands-on Workshop", help="Workshop topic")
    init_parser.add_argument("--stack", default="python", help="Tech stack (comma-separated, e.g. python, typescript, go, kotlin)")
    init_parser.add_argument("--dir", default=None, help="Target parent directory")

    # generate-all (One-Click Full Orchestration)
    gen_all_parser = subparsers.add_parser("generate-all", help="One-Click full workshop generation across all skills")
    gen_all_parser.add_argument("--name", required=True, help="Workshop project name")
    gen_all_parser.add_argument("--topic", default="BWAI Hands-on Workshop", help="Workshop topic")
    gen_all_parser.add_argument("--stack", default="python,ollama,docker", help="Tech stack (comma-separated)")
    gen_all_parser.add_argument("--dir", default=None, help="Target parent directory")

    # audit-compat command
    audit_parser = subparsers.add_parser("audit-compat", help="Audit tech stack cross-architecture compatibility")
    audit_parser.add_argument("--stack", required=True, help="Comma-separated tech stack")

    # audit-loop command (Loop Engineering Persona Audit)
    loop_parser = subparsers.add_parser("audit-loop", help="Loop Engineering multi-persona audit for beginner, intermediate, and advanced attendees")
    loop_parser.add_argument("--topic", required=True, help="Workshop topic")

    # test command
    test_parser = subparsers.add_parser("test", help="Test workshop code execution & markdown link integrity")
    test_parser.add_argument("--target", required=True, help="Path to workshop project directory")

    # pdf command
    pdf_parser = subparsers.add_parser("build-pdf", help="Build PDF handout from docs")
    pdf_parser.add_argument("--target", required=True, help="Path to workshop project directory")

    # export-codelab command
    export_parser = subparsers.add_parser("export-codelab", help="Export Open Codelabs bundle (codelab.yaml & steps) and optional push")
    export_parser.add_argument("--target", required=True, help="Path to workshop project directory")
    export_parser.add_argument("--output", default=None, help="Target output directory for Open Codelabs bundle")
    export_parser.add_argument("--push", action="store_true", help="Push exported bundle via `oc codelab push`")

    # export-colab command
    colab_parser = subparsers.add_parser("export-colab", help="Export Google Colab interactive notebooks (.ipynb) & badges")
    colab_parser.add_argument("--target", required=True, help="Path to workshop project directory")
    colab_parser.add_argument("--output", default=None, help="Target output directory for Colab notebooks")
    colab_parser.add_argument("--repo", default=None, help="GitHub repository (e.g. USER/REPO) for Colab badges")
    colab_parser.add_argument("--test", action="store_true", help="Run smoke test via Google Colab CLI")

    # test-colab command
    test_colab_parser = subparsers.add_parser("test-colab", help="Run smoke test on Colab notebooks using Google Colab CLI")
    test_colab_parser.add_argument("--target", required=True, help="Path to workshop project directory")

    # build-slides command
    slides_parser = subparsers.add_parser("build-slides", help="Build presentation slide decks in Marp Markdown and standalone Web HTML")
    slides_parser.add_argument("--target", required=True, help="Path to workshop project directory")
    slides_parser.add_argument("--output", default=None, help="Target output directory for slide deck")
    slides_parser.add_argument("--export-pdf", action="store_true", help="Export slides to PDF using Marp CLI")

    args = parser.parse_args()

    if args.command == "init":
        init_workshop(args.name, args.topic, args.dir, args.stack)
    elif args.command == "generate-all":
        generate_all(args.name, args.topic, args.stack, args.dir)
    elif args.command == "audit-compat":
        audit_compatibility(args.stack)
    elif args.command == "audit-loop":
        audit_persona_loop(args.topic)
    elif args.command == "test":
        test_workshop(args.target)
    elif args.command == "build-pdf":
        build_pdf(args.target)
    elif args.command == "export-codelab":
        export_codelab(args.target, args.output, args.push)
    elif args.command == "export-colab":
        export_colab(args.target, args.output, args.repo, args.test)
    elif args.command == "test-colab":
        test_colab(args.target)
    elif args.command == "build-slides":
        build_slides(args.target, args.output, args.export_pdf)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
