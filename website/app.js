// Workshop Harness Landing Page Script with Multi-Language (i18n) Support
// & Apple-Style Dynamic Scroll Animations

const I18N_DICT = {
  en: {
    nav_features: 'Features',
    nav_skills: '13 Skills',
    nav_codelabs: 'Open Codelabs',
    nav_arch: 'Arch Matrix',
    nav_gen: 'CLI Generator',
    nav_docs: 'Docs',
    hero_title: 'One-Click AI Agent Harness &amp; 13 Skill Suite',
    hero_subtitle: 'Technical workshop orchestration and CLI automation toolkit designed for Google Antigravity, Gemini CLI, Claude Code, OpenAI Codex, Cursor, and all AI coding agents.',
    btn_gen: 'One-Click Generation',
    btn_skills: '13 Skills Catalog',
    btn_docs: 'MkDocs Official Docs',
    copy: 'Copy',
    supported_agents: 'SUPPORTED AI CODING AGENTS &amp; LLM PLATFORMS',
    feat_title: 'Why Workshop Harness?',
    feat_desc: 'Automates workshop facilitation workflows and reduces organizer setup time by over 90%.',
    f1_title: 'One-Click Full Pipeline',
    f1_desc: 'Executes repository scaffolding, smoke testing, PDF handouts, and Open Codelabs bundles in a single shell command.',
    f2_title: '13 Agent Skills Suite',
    f2_desc: 'Includes cross-architecture auditing, runbook generation, live hotfixes, persona loops, and Open Codelabs integration.',
    f3_title: 'Cross-Architecture Engine',
    f3_desc: 'Audits hardware risks across Apple Silicon, Intel Mac, Windows x64/ARM64, and Linux, providing mandatory fallback paths.',
    skills_title: '13 Agent Skills Explorer',
    skills_desc: 'Explore specifications and artifacts for all 13 native AI agent skills.',
    f_all: 'All (13)',
    f_core: 'Curriculum & Authoring',
    f_audit: 'Audit & Testing',
    f_platform: 'Platform & PDF',
    cl_title: 'Open Codelabs Integration',
    cl_desc: 'Seamlessly export workshop materials into Open Codelabs bundles (codelab.yaml) and publish via oc CLI & stdio MCP server (oc mcp serve).',
    s1_title: 'Auto-Manifest Export',
    s1_desc: 'Parses workshop/03_labs and setup guides into codelab.yaml specs.',
    s2_title: '1-Click oc Push',
    s2_desc: 'Syncs directly via oc codelab push --manifest output/open-codelabs/codelab.yaml.',
    s3_title: 'Agentic MCP Integration',
    s3_desc: 'AI Agents interactively manage codelabs, workspaces, and help queues via oc mcp serve.',
    btn_cl_guide: 'View Integration Guide',
    matrix_title: 'Cross-Architecture Matrix',
    matrix_desc: 'Diagnoses chipset & OS risks across participant laptops prior to the session.',
    th_arch: 'Architecture / OS',
    th_tool: 'Recommended Tool',
    th_risk: 'Known Risk',
    th_action: 'Mandatory Fallback Action',
    gen_title: 'CLI Command Generator',
    gen_desc: 'Customize parameters and copy your instant command.',
    lbl_name: 'Workshop Project Name',
    lbl_topic: 'Workshop Topic',
    lbl_stack: 'Tech Stack (Comma separated)',
    lbl_generated: 'GENERATED CLI COMMAND',
    copy_cmd: 'Copy Command'
  },
  ko: {
    nav_features: '주요 특징',
    nav_skills: '13개 스킬',
    nav_codelabs: 'Open Codelabs',
    nav_arch: '호환성 매트릭스',
    nav_gen: 'CLI 생성기',
    nav_docs: '공식 문서',
    hero_title: '원클릭 AI Agent Harness &amp; 13 Skill Suite',
    hero_subtitle: 'Google Antigravity, Gemini CLI, Claude Code, OpenAI Codex, Cursor 등 모든 AI 코딩 에이전트를 위한 기술 워크숍 오케스트레이션 및 CLI 자동화 툴킷',
    btn_gen: '원클릭 워크숍 생성하기',
    btn_skills: '13개 스킬 카탈로그',
    btn_docs: 'MkDocs 문서 보기',
    copy: '복사',
    supported_agents: '지원하는 AI 코딩 에이전트 &amp; LLM 플랫폼',
    feat_title: '왜 Workshop Harness 인가요?',
    feat_desc: '현장 워크숍 운영 노하우를 자동화하여 오거나이저와 발표자의 준비 시간을 90% 이상 단축합니다.',
    f1_title: '원클릭 종합 파이프라인',
    f1_desc: 'Scaffolding부터 코드 스모크 테스트, PDF 핸드아웃 및 Open Codelabs 번들까지 한 줄 명령어로 자동 생성합니다.',
    f2_title: '13개 에이전트 스킬',
    f2_desc: '아키텍처 호환성 검사, 런북 작성, 현장 라이브 핫픽스, Open Codelabs 연동 등 검증된 13개 에이전트 스킬을 탑재했습니다.',
    f3_title: '크로스 아키텍처 호환',
    f3_desc: 'Apple Silicon, Intel Mac, Windows x64/ARM64, Linux 환경의 호환성 리스크를 오디팅하고 Fallback 경로를 자동 구성합니다.',
    skills_title: '13개 에이전트 스킬 탐색기',
    skills_desc: '필터와 검색을 통해 Workshop Harness의 13개 네이티브 에이전트 스킬 명세서를 탐색해보세요.',
    f_all: '전체 (13)',
    f_core: '커리큘럼 &amp; 작성',
    f_audit: '검증 &amp; 호환성',
    f_platform: '플랫폼 연동 &amp; 핸드아웃',
    cl_title: 'Open Codelabs 원클릭 연동',
    cl_desc: 'Workshop Harness 산출물을 Open Codelabs 번들(codelab.yaml)로 자동 내보내고 oc CLI 및 stdio MCP 서버(oc mcp serve)를 통해 원클릭으로 발행합니다.',
    s1_title: '자동 번들 작성',
    s1_desc: 'workshop/03_labs 및 가이드 문서를 codelab.yaml 규격으로 파싱',
    s2_title: '1-Click oc Push',
    s2_desc: 'oc codelab push --manifest output/open-codelabs/codelab.yaml 서버 자동 동기화',
    s3_title: 'Agentic MCP 연동',
    s3_desc: 'oc mcp serve로 AI 에이전트가 실시간 대화식으로 코드랩 및 질문 큐 조율',
    btn_cl_guide: '연동 가이드 문서 보기',
    matrix_title: '크로스 아키텍처 호환성 진단기',
    matrix_desc: '참석자 노트북 칩셋별 리스크를 사전에 감지하고 필수 우회 경로(Fallback)를 제안합니다.',
    th_arch: '아키텍처 / OS',
    th_tool: '추천 메인 도구',
    th_risk: '알려진 리스크 &amp; 방지책',
    th_action: '필수 Fallback Action',
    gen_title: '맞춤형 워크숍 CLI 커맨드 생성기',
    gen_desc: '옵션을 선택하고 실행할 명령어를 1-Click 복사하세요.',
    lbl_name: '워크숍 프로젝트 이름',
    lbl_topic: '워크숍 주제 (Topic)',
    lbl_stack: '기술 스택 (Comma separated)',
    lbl_generated: '생성된 CLI 명령어',
    copy_cmd: '명령어 복사'
  },
  ja: {
    nav_features: '特徴',
    nav_skills: '13のスキル',
    nav_codelabs: 'Open Codelabs',
    nav_arch: '互換性',
    nav_gen: 'CLI生成',
    nav_docs: 'ドキュメント',
    hero_title: 'ワンクリック AI Agent Harness &amp; 13 Skill Suite',
    hero_subtitle: 'Google Antigravity、Gemini CLI、Claude Code、OpenAI Codex、CursorなどすべてのAIコーディングエージェントのためのワークショップ自動化ツールキット。',
    btn_gen: 'ワンクリック生成',
    btn_skills: '13スキルカタログ',
    btn_docs: 'MkDocs公式ドキュメント',
    copy: 'コピー',
    supported_agents: '対応AIエージェント &amp; LLMプラットフォーム',
    feat_title: 'Workshop Harnessを選ぶ理由',
    feat_desc: 'ワークショップの準備と運用を自動化し、主催者の準備時間を90%以上削減します。',
    f1_title: 'ワンクリック・パイプライン',
    f1_desc: 'リポジトリ構築、コードテスト、PDF配布資料、Open Codelabsバンドルを単一コマンドで生成。',
    f2_title: '13のエージェントスキル',
    f2_desc: 'アーキテクチャ診断、ランブック作成、ライブ障害対応、Open Codelabs連携など検証済みスキルを搭載。',
    f3_title: 'クロスアーキテクチャ対応',
    f3_desc: 'Apple Silicon、Intel Mac、Windows、Linuxにおける互換性リスクを診断しFallbackを提供。',
    skills_title: '13エージェントスキル・エクスプローラー',
    skills_desc: '13のネイティブAIエージェントスキルの仕様と成果物を探索できます。',
    f_all: 'すべて (13)',
    f_core: 'カリキュラム &amp; 作成',
    f_audit: '検証 &amp; 互換性',
    f_platform: 'プラットフォーム連携 &amp; PDF',
    cl_title: 'Open Codelabs ワンクリック連携',
    cl_desc: 'Workshop Harnessの成果物をOpen Codelabsバンドル(codelab.yaml)に自動変換し、oc CLIやMCPサーバーでデプロイします。',
    s1_title: '自動マニフェスト出力',
    s1_desc: 'workshop/03_labsとガイドをcodelab.yaml仕様にパース',
    s2_title: '1-Click oc Push',
    s2_desc: 'oc codelab push --manifest output/open-codelabs/codelab.yamlで自動同期',
    s3_title: 'Agentic MCP 連携',
    s3_desc: 'oc mcp serveによりAIエージェントがリアルタイムでコードラボや質問キューを管理',
    btn_cl_guide: '連携ガイドを見る',
    matrix_title: 'クロスアーキテクチャ互換性マトリクス',
    matrix_desc: '参加者PCのチップセットリスクを事前診断し、必要なFallback手順を提案します。',
    th_arch: 'アーキテクチャ / OS',
    th_tool: '推奨メインツール',
    th_risk: '既知のリスク',
    th_action: '必須Fallbackアクション',
    gen_title: 'CLIコマンドジェネレーター',
    gen_desc: 'パラメータをカスタマイズして、ワンクリックでコマンドをコピーします。',
    lbl_name: 'ワークショッププロジェクト名',
    lbl_topic: 'ワークショップトピック',
    lbl_stack: '技術スタック (カンマ区切り)',
    lbl_generated: '生成されたCLIコマンド',
    copy_cmd: 'コマンドをコピー'
  },
  zh: {
    nav_features: '核心特性',
    nav_skills: '13项技能',
    nav_codelabs: 'Open Codelabs',
    nav_arch: '架构矩阵',
    nav_gen: 'CLI生成器',
    nav_docs: '官方文档',
    hero_title: '一键式 AI Agent Harness &amp; 13项技能套件',
    hero_subtitle: '专为 Google Antigravity、Gemini CLI、Claude Code、OpenAI Codex、Cursor 等所有 AI 编程 Agent 打造的技术工作坊自动化工具包。',
    btn_gen: '一键生成',
    btn_skills: '13项技能目录',
    btn_docs: 'MkDocs 官方文档',
    copy: '复制',
    supported_agents: '支持的 AI 编程 Agent 及 LLM 平台',
    feat_title: '为什么选择 Workshop Harness？',
    feat_desc: '自动化技术工作坊筹备流程，将组织者的准备时间缩短 90% 以上。',
    f1_title: '一键式完整流水线',
    f1_desc: '单条 Shell 命令即可执行仓库脚手架、代码测试、PDF 手册及 Open Codelabs Bundle 生成。',
    f2_title: '13 项 Agent 技能套件',
    f2_desc: '包含跨架构审计、Runbook 生成、现场热修复、Persona 循环审查及 Open Codelabs 集成。',
    f3_title: '跨架构引擎',
    f3_desc: '审计 Apple Silicon、Intel Mac、Windows x64/ARM64 及 Linux 上的硬件风险并提供 Fallback 方案。',
    skills_title: '13 项 Agent 技能浏览器',
    skills_desc: '探索 13 项原生 AI Agent 技能的规范与产物。',
    f_all: '全部 (13)',
    f_core: '课程与撰写',
    f_audit: '审计与测试',
    f_platform: '平台与 PDF',
    cl_title: 'Open Codelabs 一键集成',
    cl_desc: '无缝将工作坊产物导出为 Open Codelabs Bundle (codelab.yaml)，并通过 oc CLI 与 stdio MCP 部署。',
    s1_title: '自动 Manifest 导出',
    s1_desc: '解析 workshop/03_labs 及准备指南至 codelab.yaml 规范。',
    s2_title: '1-Click oc Push',
    s2_desc: '通过 oc codelab push --manifest output/open-codelabs/codelab.yaml 直接同步。',
    s3_title: 'Agentic MCP 集成',
    s3_desc: 'AI Agent 通过 oc mcp serve 交互式管理 Codelab、工作区及提问队列。',
    btn_cl_guide: '查看集成指南',
    matrix_title: '跨架构兼容性矩阵',
    matrix_desc: '在活动开始前诊断参会者笔记本电脑的芯片及 OS 风险。',
    th_arch: '架构 / OS',
    th_tool: '推荐主工具',
    th_risk: '已知风险',
    th_action: '必要 Fallback 措施',
    gen_title: 'CLI 命令生成器',
    gen_desc: '自定义参数并一键复制即用命令。',
    lbl_name: '工作坊项目名称',
    lbl_topic: '工作坊主题',
    lbl_stack: '技术栈 (逗号分隔)',
    lbl_generated: '生成的 CLI 命令',
    copy_cmd: '复制命令'
  }
};

const SKILLS_DATA = [
  {
    num: "01",
    id: "workshop-scaffolder",
    title: "workshop-scaffolder",
    cat: "core",
    desc: "Scaffolds standard workshop repository structure (docs/, workshop/, prompt-pack/, scripts/) & boilerplate",
    input: "Workshop name & topic",
    output: "Standard workshop repository layout"
  },
  {
    num: "02",
    id: "cross-architecture-checker",
    title: "cross-architecture-checker",
    cat: "audit",
    desc: "Audits Apple Silicon, Intel Mac, Windows, and Linux chipset risks & generates fallback guides",
    input: "Tech stack list",
    output: "docs/00-architecture-matrix.md"
  },
  {
    num: "03",
    id: "prerequisite-checker",
    title: "prerequisite-checker",
    cat: "core",
    desc: "Generates OS-specific setup guide (gemma4-local-setup-guide.md) & check_env verification scripts",
    input: "Prerequisites specification",
    output: "Setup guide & check_env.sh/ps1"
  },
  {
    num: "04",
    id: "hands-on-curriculum-builder",
    title: "hands-on-curriculum-builder",
    cat: "core",
    desc: "Builds step-by-step lab guides (03_labs/README.md), starter & completed final solution templates",
    input: "Session goals & timing",
    output: "Lab guides, 01_starter & 02_final code"
  },
  {
    num: "05",
    id: "pdf-handout-generator",
    title: "pdf-handout-generator",
    cat: "platform",
    desc: "Builds publication-ready PDF handouts (output/pdf/) & thumbnail contact sheets via ReportLab & PyMuPDF",
    input: "docs/ markdown directory",
    output: "output/pdf/*.pdf & preview PNG"
  },
  {
    num: "06",
    id: "workshop-troubleshooter",
    title: "workshop-troubleshooter",
    cat: "audit",
    desc: "Generates troubleshooting matrix by RAM (8G/16G/32G+) and OS in docs/20-faq.md",
    input: "Hardware specs & OS",
    output: "docs/troubleshooting.md & FAQ"
  },
  {
    num: "07",
    id: "workshop-runbook-generator",
    title: "workshop-runbook-generator",
    cat: "core",
    desc: "Creates minute-by-minute facilitator timeline runbook (RUNBOOK.md) & cue cards",
    input: "Session duration & TAs",
    output: "RUNBOOK.md timeline"
  },
  {
    num: "08",
    id: "live-debug-assistant",
    title: "live-debug-assistant",
    cat: "audit",
    desc: "Diagnoses live terminal errors with 10-second hotfix commands & enforces API Key security",
    input: "Terminal error log",
    output: "10-second hotfix command & .env.sample"
  },
  {
    num: "09",
    id: "workshop-faq-generator",
    title: "workshop-faq-generator",
    cat: "core",
    desc: "Automatically compiles attendee FAQ (hardware, network, code setup)",
    input: "Topic & level",
    output: "docs/20-faq.md"
  },
  {
    num: "10",
    id: "workshop-tester",
    title: "workshop-tester",
    cat: "audit",
    desc: "Audits Python code execution smoke tests and relative markdown broken links",
    input: "Workshop project path",
    output: "verify_workshop.py audit result"
  },
  {
    num: "11",
    id: "workshop-web-researcher",
    title: "workshop-web-researcher",
    cat: "audit",
    desc: "Real-time web auditing of latest tool/SDK releases & breaking changes",
    input: "Tool/Model query",
    output: "Release tags & docs audit report"
  },
  {
    num: "12",
    id: "workshop-persona-loop-evaluator",
    title: "workshop-persona-loop-evaluator",
    cat: "audit",
    desc: "Multi-persona loop engineering audit for beginner, intermediate, and advanced attendees",
    input: "Topic & materials",
    output: "docs/00-persona-loop-review-report.md"
  },
  {
    num: "13",
    id: "open-codelabs-integrator",
    title: "open-codelabs-integrator",
    cat: "platform",
    desc: "Converts workshop artifacts to Open Codelabs manifests (codelab.yaml) & pushes via oc CLI/MCP",
    input: "Workshop project path",
    output: "output/open-codelabs/ (codelab.yaml, steps/)"
  },
  {
    num: "14",
    id: "colab-workshop-integrator",
    title: "colab-workshop-integrator",
    cat: "platform",
    desc: "Generates Google Colab interactive notebooks (.ipynb), badges, and automates headless smoke tests via colab CLI",
    input: "Workshop project path",
    output: "output/colab/ (*.ipynb, badges), colab CLI test"
  }
];

document.addEventListener("DOMContentLoaded", () => {
  renderSkills("all");
  setupTabSwitcher();
  setupSkillFilter();
  setupCommandGenerator();
  setupCopyButtons();
  setupLanguageSelector();
  setupAppleScrollAnimations();
});

// Apple-style Scroll Animations & Interactions
function setupAppleScrollAnimations() {
  // 1. Scroll Progress Bar
  const progressBar = document.getElementById("scrollProgress");
  window.addEventListener("scroll", () => {
    const totalHeight = document.documentElement.scrollHeight - window.innerHeight;
    if (totalHeight > 0 && progressBar) {
      const progress = (window.scrollY / totalHeight) * 100;
      progressBar.style.width = `${progress}%`;
    }
  });

  // 2. IntersectionObserver Scroll Reveal
  const reveals = document.querySelectorAll(".reveal");
  const observerOptions = {
    threshold: 0.15,
    rootMargin: "0px 0px -50px 0px"
  };

  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("active");
        
        // Trigger stat counters if stats-bar is revealed
        if (entry.target.classList.contains("stats-bar")) {
          animateStatCounters();
        }
      }
    });
  }, observerOptions);

  reveals.forEach(el => revealObserver.observe(el));

  // 3. Perspective Tilt on Terminal Showcase
  const terminal = document.getElementById("terminalShowcase");
  if (terminal) {
    window.addEventListener("scroll", () => {
      const rect = terminal.getBoundingClientRect();
      if (rect.top < window.innerHeight && rect.bottom > 0) {
        const factor = Math.max(0, (rect.top / window.innerHeight));
        if (factor < 0.4) {
          terminal.classList.add("flatten");
        } else {
          terminal.classList.remove("flatten");
        }
      }
    });
  }
}

// Animate Stat Counters Smoothly
function animateStatCounters() {
  const statNumbers = document.querySelectorAll(".stat-number");
  statNumbers.forEach(numEl => {
    if (numEl.getAttribute("data-animated")) return;
    numEl.setAttribute("data-animated", "true");

    const target = parseInt(numEl.getAttribute("data-target"), 10);
    const suffix = numEl.getAttribute("data-suffix") || "";
    let current = 0;
    const duration = 1200; // ms
    const increment = target / (duration / 16);

    const timer = setInterval(() => {
      current += increment;
      if (current >= target) {
        numEl.textContent = `${target}${suffix}`;
        clearInterval(timer);
      } else {
        numEl.textContent = `${Math.floor(current)}${suffix}`;
      }
    }, 16);
  });
}

// Setup Language Selector (en, ko, ja, zh)
function setupLanguageSelector() {
  const select = document.getElementById("langSelect");
  if (!select) return;

  select.addEventListener("change", (e) => {
    const lang = e.target.value;
    applyLanguage(lang);
  });
}

function applyLanguage(lang) {
  const dict = I18N_DICT[lang] || I18N_DICT.en;

  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    if (dict[key]) {
      el.innerHTML = dict[key];
    }
  });
}

// Render 13 Agent Skills Grid
function renderSkills(filterCat = "all", searchQuery = "") {
  const container = document.getElementById("skillsGridContainer");
  if (!container) return;

  const query = searchQuery.toLowerCase().trim();
  const filtered = SKILLS_DATA.filter(skill => {
    const matchCat = filterCat === "all" || skill.cat === filterCat;
    const matchQuery = !query || 
      skill.title.toLowerCase().includes(query) ||
      skill.desc.toLowerCase().includes(query) ||
      skill.input.toLowerCase().includes(query);
    return matchCat && matchQuery;
  });

  if (filtered.length === 0) {
    container.innerHTML = `
      <div style="grid-column: 1 / -1; text-align: center; padding: 40px; color: var(--colors-body-mid);">
        <p>No matching agent skills found.</p>
      </div>
    `;
    return;
  }

  container.innerHTML = filtered.map(skill => `
    <div class="skill-card spot-card">
      <div>
        <div class="skill-header">
          <span class="skill-num">Skill #${skill.num}</span>
          <span class="badge-v">${skill.cat.toUpperCase()}</span>
        </div>
        <h4 class="skill-title">${skill.title}</h4>
        <p class="skill-desc">${skill.desc}</p>
      </div>
      <div class="skill-meta">
        <span><strong>Input:</strong> ${skill.input}</span>
        <span><strong>Output:</strong> ${skill.output}</span>
      </div>
    </div>
  `).join("");
}

// Terminal Showcase Tab Switcher
function setupTabSwitcher() {
  const tabs = document.querySelectorAll(".terminal-tabs .tab-btn");
  const contents = document.querySelectorAll(".terminal-body .tab-content");

  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      tabs.forEach(t => t.classList.remove("active"));
      contents.forEach(c => c.classList.remove("active"));

      tab.classList.add("active");
      const targetId = tab.getAttribute("data-tab");
      const targetContent = document.getElementById(targetId);
      if (targetContent) targetContent.classList.add("active");
    });
  });
}

// Skill Filter Chips & Search Box
function setupSkillFilter() {
  const chips = document.querySelectorAll(".filter-chips .chip-btn");
  const searchInput = document.getElementById("skillSearchInput");

  let currentFilter = "all";

  chips.forEach(chip => {
    chip.addEventListener("click", () => {
      chips.forEach(c => c.classList.remove("active"));
      chip.classList.add("active");
      currentFilter = chip.getAttribute("data-filter");
      renderSkills(currentFilter, searchInput ? searchInput.value : "");
    });
  });

  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      renderSkills(currentFilter, e.target.value);
    });
  }
}

// Interactive Command Generator
function setupCommandGenerator() {
  const nameInput = document.getElementById("inputProjName");
  const topicInput = document.getElementById("inputTopic");
  const stackInput = document.getElementById("inputStack");
  const codeOutput = document.getElementById("generatedCommandCode");

  function updateCommand() {
    const name = nameInput.value.trim() || "my-bwai-workshop";
    const topic = topicInput.value.trim() || "BWAI Workshop";
    const stack = stackInput.value.trim() || "python,ollama,docker";

    codeOutput.textContent = `uv run harness_cli.py generate-all --name "${name}" --topic "${topic}" --stack "${stack}"`;
  }

  [nameInput, topicInput, stackInput].forEach(inp => {
    if (inp) inp.addEventListener("input", updateCommand);
  });
}

// Copy Buttons Functionality
function setupCopyButtons() {
  const copyTabBtn = document.getElementById("copyTabCodeBtn");
  if (copyTabBtn) {
    copyTabBtn.addEventListener("click", () => {
      const activeContent = document.querySelector(".terminal-body .tab-content.active");
      if (activeContent) {
        navigator.clipboard.writeText(activeContent.innerText);
        copyTabBtn.innerHTML = 'Copied!';
        setTimeout(() => {
          copyTabBtn.innerHTML = 'Copy';
        }, 2000);
      }
    });
  }

  const copyGenBtn = document.getElementById("btnCopyGenerated");
  const genCode = document.getElementById("generatedCommandCode");
  if (copyGenBtn && genCode) {
    copyGenBtn.addEventListener("click", () => {
      navigator.clipboard.writeText(genCode.innerText);
      copyGenBtn.innerHTML = 'Copied!';
      setTimeout(() => {
        copyGenBtn.innerHTML = 'Copy Command';
      }, 2000);
    });
  }
}
