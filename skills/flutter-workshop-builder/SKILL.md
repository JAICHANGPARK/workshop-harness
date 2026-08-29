---
name: flutter-workshop-builder
description: Builds cross-platform Flutter Generative AI hands-on workshops using Flutter 3.x, Dart 3.x, the official google_generative_ai package, official Flutter Agent Plugins (flutter/agent-plugins), and Dart Package Skills. Enforces Material 3 design, reactive state management, streaming chat responses, Dart/Flutter MCP server tooling, and zero-install Flutter Web fallback strategies.
---

# Flutter Hands-on Workshop Builder Skill

## Purpose

Automates the end-to-end creation of technical hands-on workshops focused on **Flutter Generative AI** cross-platform applications. Enforces clean architecture, **Material 3 UI design**, state management best practices, the official **`google_generative_ai`** Dart SDK, and official **Flutter Agent Plugins (`github.com/flutter/agent-plugins`)** & **Package Skills (`docs.flutter.dev/ai/package-skills`)**.

> Pre-Flight Web Research Protocol:
> Before generating Flutter workshop materials or code, verify the latest versions on `pub.dev` for `google_generative_ai`, `genui`, and check Flutter AI tooling documentation at `docs.flutter.dev/ai/get-started`.

---

## 🛠️ Official Flutter Agent Plugins & Skills Ecosystem

Flutter hands-on workshops should actively leverage the official **Flutter Agent Plugins (`github.com/flutter/agent-plugins`)**, the **Dart & Flutter MCP Server**, and **Package Skills (`docs.flutter.dev/ai/package-skills`)** to automate layout generation, UI debugging, and testing:

### 1. Installing Official Flutter Agent Skills

```bash
# Option A: Install via Universal Skills CLI
npx skills add flutter/agent-plugins --skill '*' --agent universal --yes

# Option B: Scan & discover bundled skills from pub.dev dependencies
dart run skills@ get
```

### 2. Official Flutter Agent Skills Integration Matrix

When building hands-on labs, AI coding assistants should invoke these specialized skills for specific development tasks:

| Specialized Flutter / Dart Skill | Workshop Lab Application |
|---|---|
| `flutter-build-responsive-layout` | Build adaptive layouts with `LayoutBuilder` / `MediaQuery` across Web, Tablet, and Mobile |
| `flutter-fix-layout-issues` | Diagnose and resolve `RenderFlex overflowed` errors and unbounded constraints in AI chat UI |
| `flutter-apply-architecture-best-practices` | Structure clean layered architecture (UI, Business Logic, Data layer) |
| `flutter-setup-declarative-routing` | Configure declarative URL-based routing via `go_router` for Web & deep linking |
| `flutter-implement-json-serialization` | Create type-safe data models with `fromJson` / `toJson` for Gemini API payloads |
| `flutter-add-widget-test` | Implement component-level tests with `WidgetTester` for prompt input & streaming views |
| `flutter-add-integration-test` | Automate end-to-end user flows on emulator, physical device, or Chrome |
| `dart-run-static-analysis` | Run `dart analyze` and execute `dart fix --apply` for mechanical code cleanup |
| `dart-fix-runtime-errors` | Fetch active runtime stack traces, locate failing lines, and verify with hot reload |

### 3. Dart & Flutter MCP Server Integration

The Dart/Flutter MCP server provides real-time access to live IDE diagnostics:
- **`analyze_files`**: Run real-time static analysis on edited Dart files.
- **`hot_reload` / `hot_restart`**: Instantly push code updates to running Flutter devices.
- **`widget_inspector`**: Inspect the live widget hierarchy and state.

---

## Technical Stack & Dependency Matrix

| Layer | Component | Recommended Package / Version | File Location |
|---|---|---|---|
| **Framework & Language** | Flutter & Dart | Flutter 3.24+ / Dart 3.5+ | `pubspec.yaml` |
| **GenAI SDK** | Google Generative AI Dart | `google_generative_ai: ^0.4.6` | `pubspec.yaml` |
| **Generative UI** | Flutter GenUI | `genui: ^0.1.0` | `pubspec.yaml` |
| **Design System** | Flutter Material 3 | `useMaterial3: true` | `lib/main.dart` |
| **Image & Multimodal** | Image Picker | `image_picker: ^1.1.2` | `pubspec.yaml` |
| **Environment Variables** | Flutter Dotenv | `flutter_dotenv: ^5.2.1` | `pubspec.yaml` |

---

## 3-Stage Hands-on Lab Curriculum

```mermaid
flowchart TD
    Lab1["Lab 01: Flutter Scaffold & Gemini Client Setup (20-25 min)<br>Initialize project, configure google_generative_ai, build Material 3 streaming chat UI"]
    Lab2["Lab 02: Responsive Chat UI & Multimodal Vision (35-40 min)<br>Use flutter-build-responsive-layout, attach images via image_picker & DataPart"]
    Lab3["Lab 03: Structured Outputs, Widget Tests & Web Deployment (25-30 min)<br>Implement flutter-add-widget-test, test on Flutter Web (flutter run -d chrome)"]

    Lab1 --> Lab2 --> Lab3
```

---

## Architectural Patterns for Flutter Workshops

### 1. Generative AI Service & Stream Handling

```dart
// Flutter Generative AI Service Example
import 'dart:typed_data';
import 'package:google_generative_ai/google_generative_ai.dart';

class GeminiService {
  final GenerativeModel _model;
  ChatSession? _chatSession;

  GeminiService({required String apiKey, String modelName = 'gemini-3.7-flash'})
      : _model = GenerativeModel(
          model: modelName,
          apiKey: apiKey,
          generationConfig: GenerationConfig(
            temperature: 0.7,
            maxOutputTokens: 1024,
          ),
        );

  void initChat() {
    _chatSession = _model.startChat();
  }

  Stream<GenerateContentResponse> sendMessageStream(String prompt) {
    if (_chatSession == null) initChat();
    return _chatSession!.sendMessageStream(Content.text(prompt));
  }

  Future<String> analyzeImage(String prompt, Uint8List imageBytes, String mimeType) async {
    final content = [
      Content.multi([
        TextPart(prompt),
        DataPart(mimeType, imageBytes),
      ]),
    ];
    final response = await _model.generateContent(content);
    return response.text ?? 'No response';
  }
}
```

---

## Cross-Platform Workshop Strategy & Friction Reducers

Workshops often run into venue WiFi bottlenecks or laptop emulator performance issues. Follow these rules when organizing a Flutter hands-on:

1. **Default Target: Flutter Web (`flutter run -d chrome`)**:
   - Zero emulator installation required.
   - Works uniformly across Windows, macOS, Linux, and ChromeOS.
   - Allows instant browser preview and rapid hot restart.
2. **Package Skills Discovery (`dart run skills@ get`)**:
   - Instruct attendees to run `dart run skills@ get` to install bundled agent skills from newly added dependencies.
3. **Mobile Target: Physical Device USB Debugging**:
   - For Android: Enable Developer Options and USB Debugging.
   - For iOS: Requires macOS and Xcode signing certificate.
4. **API Key Handling**:
   - Pass keys via `--dart-define=GEMINI_API_KEY=your_key` during `flutter run` to avoid hardcoding secrets.

---

## Facilitator Verification Checklist

1. Run `flutter doctor -v` to ensure Flutter SDK and Dart toolchain are healthy.
2. Run `dart run skills@ get` to verify package skills installation.
3. Run `flutter test` to ensure unit and widget test suites pass before distributing materials.

