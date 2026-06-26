# Harness for Codex

<p>
  <a href="#english"><kbd>English</kbd></a>
  <a href="#japanese"><kbd>日本語</kbd></a>
  <a href="#chinese"><kbd>中文</kbd></a>
  <a href="#korean"><kbd>한국어</kbd></a>
  <a href="#portuguese"><kbd>Português</kbd></a>
  <a href="#spanish"><kbd>Español</kbd></a>
</p>

> GitHub README files do not run custom JavaScript, so the language buttons jump
> to sections in this single file instead of switching tabs dynamically.

## English

Harness for Codex is a Codex-oriented port inspired by
[`revfactory/harness`](https://github.com/revfactory/harness). It provides a
project-local harness factory for designing, scaffolding, validating, and
evolving reusable Codex skills and workflow architectures.

The upstream Harness is focused on Claude Code. This repository maps the same
factory idea to Codex primitives: `skills/`, `SKILL.md`, `agents/openai.yaml`,
references, scripts, templates, validation checks, and optional sub-agent
protocols when the active Codex runtime supports them.

### Included

```text
skills/codex-harness/
  SKILL.md
  agents/openai.yaml
  references/
    agent-design-patterns.md
    orchestrator-template.md
    project-integration.md
    qa-agent-guide.md
    evaluation-prompts.md
    skill-testing-guide.md
    skill-writing-guide.md
    team-examples.md
  scripts/
    scaffold_codex_skill.py
    validate_codex_harness.py
skills/repo-review/
skills/feature-delivery/
skills/integration-qa/
skills/docs-maintenance/
skills/release-readiness/
scripts/sync_codex_skills.ps1
.codex-plugin/
  plugin.json
```

### Practical Skills

| Skill | Use for |
|---|---|
| `codex-harness` | designing, auditing, scaffolding, and evolving harnesses |
| `repo-review` | code review, PR review, repository audit, regression review |
| `feature-delivery` | planning, implementing, validating, and summarizing feature work |
| `integration-qa` | checking cross-boundary mismatches after changes |
| `docs-maintenance` | generating, updating, and verifying repository documentation |
| `release-readiness` | pre-release validation gates, changelog readiness, and deployment risk review |

### Use

Use the repository copy directly:

```text
Use $codex-harness at ./skills/codex-harness to design a project harness.
```

Typical prompts:

```text
Build a Codex harness for this repository.
Audit the existing Codex harness and evolve it.
Create reusable Codex skills for code review and release readiness.
Design a supervisor skill that routes frontend, backend, and QA workflows.
Use $feature-delivery at ./skills/feature-delivery to implement a bounded feature.
Use $repo-review at ./skills/repo-review to review the current diff.
```

### Scaffold a New Skill

```powershell
python .\skills\codex-harness\scripts\scaffold_codex_skill.py repo-review `
  --description "Review this repository for architecture, security, performance, tests, and integration risks. Use when asked for code review, PR review, regression review, or release readiness review." `
  --orchestrator `
  --resources references,scripts
```

### Validate

```powershell
python .\skills\codex-harness\scripts\validate_codex_harness.py .
python C:\Users\kkmia\.codex\skills\.system\skill-creator\scripts\quick_validate.py .\skills\codex-harness
```

Run the repository validator for every skill directory you create or edit:

```powershell
Get-ChildItem .\skills -Directory | ForEach-Object {
  python .\skills\codex-harness\scripts\validate_codex_harness.py $_.FullName
}
```

### Sync Local Skills

Install or update every repository skill into your local Codex skills directory:

```powershell
.\scripts\sync_codex_skills.ps1 -All
```

Install or update selected skills only:

```powershell
.\scripts\sync_codex_skills.ps1 -Skill codex-harness,repo-review
```

The script replaces only the selected skill directories under
`$env:USERPROFILE\.codex\skills` and does not delete unrelated local skills.

### License and Attribution

This repository is licensed under the Apache License 2.0. See `LICENSE`.

Harness for Codex is inspired by
[`revfactory/harness`](https://github.com/revfactory/harness), which is also
licensed under Apache-2.0.

## Japanese

Harness for Codex は
[`revfactory/harness`](https://github.com/revfactory/harness) に着想を得た、
Codex 向けの移植版です。プロジェクト内で再利用できる Codex スキルと
ワークフロー構成を設計、足場作成、検証、改善するためのハーネス
ファクトリです。

上流の Harness は Claude Code 向けです。このリポジトリでは同じ考え方を
Codex の構成要素である `skills/`、`SKILL.md`、`agents/openai.yaml`、
参照資料、スクリプト、テンプレート、検証チェック、必要に応じた
サブエージェント手順に対応させています。

### 含まれるもの

```text
skills/codex-harness/
  SKILL.md
  agents/openai.yaml
  references/
  scripts/
skills/repo-review/
skills/feature-delivery/
skills/integration-qa/
skills/docs-maintenance/
skills/release-readiness/
scripts/sync_codex_skills.ps1
.codex-plugin/
  plugin.json
```

### 実用スキル

| スキル | 用途 |
|---|---|
| `codex-harness` | ハーネスの設計、監査、足場作成、改善 |
| `repo-review` | コードレビュー、PR レビュー、リポジトリ監査、回帰確認 |
| `feature-delivery` | 機能作業の計画、実装、検証、要約 |
| `integration-qa` | 変更後の境界間の不整合確認 |
| `docs-maintenance` | README、API 文書、コマンド文書、例の検証 |
| `release-readiness` | リリース前検証、変更履歴確認、デプロイリスク確認 |

### 使い方

リポジトリ内のコピーを直接指定します。

```text
Use $codex-harness at ./skills/codex-harness to design a project harness.
```

代表的な依頼例:

```text
Build a Codex harness for this repository.
Audit the existing Codex harness and evolve it.
Use $feature-delivery at ./skills/feature-delivery to implement a bounded feature.
Use $repo-review at ./skills/repo-review to review the current diff.
```

### 新しいスキルの作成

```powershell
python .\skills\codex-harness\scripts\scaffold_codex_skill.py repo-review `
  --description "Review this repository for architecture, security, performance, tests, and integration risks. Use when asked for code review, PR review, regression review, or release readiness review." `
  --orchestrator `
  --resources references,scripts
```

### 検証

```powershell
python .\skills\codex-harness\scripts\validate_codex_harness.py .
python C:\Users\kkmia\.codex\skills\.system\skill-creator\scripts\quick_validate.py .\skills\codex-harness
```

各スキルを検証する場合:

```powershell
Get-ChildItem .\skills -Directory | ForEach-Object {
  python .\skills\codex-harness\scripts\validate_codex_harness.py $_.FullName
}
```

### ローカル同期

すべてのスキルをローカルの Codex スキルディレクトリへ同期します。

```powershell
.\scripts\sync_codex_skills.ps1 -All
```

指定したスキルだけ同期する場合:

```powershell
.\scripts\sync_codex_skills.ps1 -Skill codex-harness,repo-review
```

### ライセンスと帰属

このリポジトリは Apache License 2.0 でライセンスされています。詳細は
`LICENSE` を参照してください。Harness for Codex は Apache-2.0 ライセンスの
[`revfactory/harness`](https://github.com/revfactory/harness) に着想を得ています。

## Chinese

Harness for Codex 是受
[`revfactory/harness`](https://github.com/revfactory/harness) 启发的 Codex
版本。它提供一个项目本地的 harness factory，用于设计、生成、验证和演进可复用
的 Codex skills 与工作流架构。

上游 Harness 面向 Claude Code。本仓库将同样的思路映射到 Codex 结构：
`skills/`、`SKILL.md`、`agents/openai.yaml`、参考资料、脚本、模板、
验证检查，以及在运行时支持时可选的 sub-agent 协议。

### 包含内容

```text
skills/codex-harness/
skills/repo-review/
skills/feature-delivery/
skills/integration-qa/
skills/docs-maintenance/
skills/release-readiness/
scripts/sync_codex_skills.ps1
.codex-plugin/plugin.json
```

### 实用 Skills

| Skill | 用途 |
|---|---|
| `codex-harness` | 设计、审计、生成和改进 harness |
| `repo-review` | 代码审查、PR 审查、仓库审计、回归检查 |
| `feature-delivery` | 规划、实现、验证和总结功能交付 |
| `integration-qa` | 检查变更后的跨边界不一致 |
| `docs-maintenance` | 生成、更新和验证项目文档 |
| `release-readiness` | 发布前检查、changelog 准备和部署风险审查 |

### 使用

直接使用仓库中的 skill:

```text
Use $codex-harness at ./skills/codex-harness to design a project harness.
```

验证仓库:

```powershell
python .\skills\codex-harness\scripts\validate_codex_harness.py .
```

同步本地 skills:

```powershell
.\scripts\sync_codex_skills.ps1 -All
```

本仓库采用 Apache License 2.0。详情见 `LICENSE`。

## Korean

Harness for Codex는
[`revfactory/harness`](https://github.com/revfactory/harness)에서 영감을 받은
Codex용 포트입니다. 재사용 가능한 Codex skill과 워크플로 아키텍처를 설계,
스캐폴딩, 검증, 개선하기 위한 프로젝트 로컬 harness factory입니다.

상위 Harness는 Claude Code에 초점을 둡니다. 이 저장소는 같은 factory 개념을
Codex의 `skills/`, `SKILL.md`, `agents/openai.yaml`, 참조 문서, 스크립트,
템플릿, 검증 체크, 선택적 sub-agent 프로토콜로 매핑합니다.

### 포함 내용

```text
skills/codex-harness/
skills/repo-review/
skills/feature-delivery/
skills/integration-qa/
skills/docs-maintenance/
skills/release-readiness/
scripts/sync_codex_skills.ps1
.codex-plugin/plugin.json
```

### 실용 Skills

| Skill | 용도 |
|---|---|
| `codex-harness` | harness 설계, 감사, 스캐폴딩, 개선 |
| `repo-review` | 코드 리뷰, PR 리뷰, 저장소 감사, 회귀 확인 |
| `feature-delivery` | 기능 작업의 계획, 구현, 검증, 요약 |
| `integration-qa` | 변경 후 경계 간 불일치 확인 |
| `docs-maintenance` | 저장소 문서 생성, 업데이트, 검증 |
| `release-readiness` | 릴리스 전 검증, changelog 준비, 배포 위험 검토 |

### 사용

저장소의 skill을 직접 사용합니다.

```text
Use $codex-harness at ./skills/codex-harness to design a project harness.
```

검증:

```powershell
python .\skills\codex-harness\scripts\validate_codex_harness.py .
```

로컬 skills 동기화:

```powershell
.\scripts\sync_codex_skills.ps1 -All
```

이 저장소는 Apache License 2.0으로 라이선스됩니다. 자세한 내용은 `LICENSE`를
참조하세요.

## Portuguese

Harness for Codex é uma versão orientada ao Codex inspirada em
[`revfactory/harness`](https://github.com/revfactory/harness). Ela fornece uma
harness factory local ao projeto para desenhar, criar, validar e evoluir skills
reutilizáveis do Codex e arquiteturas de workflow.

O Harness original é focado no Claude Code. Este repositório mapeia a mesma
ideia para primitivas do Codex: `skills/`, `SKILL.md`, `agents/openai.yaml`,
referências, scripts, templates, validações e protocolos opcionais de
sub-agent quando o runtime do Codex oferece suporte.

### Conteúdo

```text
skills/codex-harness/
skills/repo-review/
skills/feature-delivery/
skills/integration-qa/
skills/docs-maintenance/
skills/release-readiness/
scripts/sync_codex_skills.ps1
.codex-plugin/plugin.json
```

### Skills Práticas

| Skill | Uso |
|---|---|
| `codex-harness` | desenhar, auditar, criar e evoluir harnesses |
| `repo-review` | revisão de código, revisão de PR, auditoria de repositório |
| `feature-delivery` | planejar, implementar, validar e resumir features |
| `integration-qa` | verificar inconsistências entre fronteiras após mudanças |
| `docs-maintenance` | gerar, atualizar e validar documentação |
| `release-readiness` | validação pré-release, changelog e risco de deploy |

### Uso

Use a skill diretamente a partir deste repositório:

```text
Use $codex-harness at ./skills/codex-harness to design a project harness.
```

Validar:

```powershell
python .\skills\codex-harness\scripts\validate_codex_harness.py .
```

Sincronizar skills locais:

```powershell
.\scripts\sync_codex_skills.ps1 -All
```

Este repositório usa a licença Apache License 2.0. Consulte `LICENSE`.

## Spanish

Harness for Codex es una versión orientada a Codex inspirada en
[`revfactory/harness`](https://github.com/revfactory/harness). Proporciona una
harness factory local al proyecto para diseñar, generar, validar y evolucionar
skills reutilizables de Codex y arquitecturas de workflow.

El Harness original está enfocado en Claude Code. Este repositorio adapta la
misma idea a primitivas de Codex: `skills/`, `SKILL.md`, `agents/openai.yaml`,
referencias, scripts, plantillas, validaciones y protocolos opcionales de
sub-agent cuando el runtime de Codex los soporta.

### Contenido

```text
skills/codex-harness/
skills/repo-review/
skills/feature-delivery/
skills/integration-qa/
skills/docs-maintenance/
skills/release-readiness/
scripts/sync_codex_skills.ps1
.codex-plugin/plugin.json
```

### Skills Prácticas

| Skill | Uso |
|---|---|
| `codex-harness` | diseñar, auditar, generar y evolucionar harnesses |
| `repo-review` | revisión de código, revisión de PR y auditoría del repositorio |
| `feature-delivery` | planificar, implementar, validar y resumir features |
| `integration-qa` | revisar inconsistencias entre límites después de cambios |
| `docs-maintenance` | generar, actualizar y verificar documentación |
| `release-readiness` | validación previa al release, changelog y riesgo de despliegue |

### Uso

Usa la skill directamente desde este repositorio:

```text
Use $codex-harness at ./skills/codex-harness to design a project harness.
```

Validar:

```powershell
python .\skills\codex-harness\scripts\validate_codex_harness.py .
```

Sincronizar skills locales:

```powershell
.\scripts\sync_codex_skills.ps1 -All
```

Este repositorio está licenciado bajo Apache License 2.0. Consulta `LICENSE`.
