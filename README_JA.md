# Codex 用 Harness

[English README](README.md)

このリポジトリは、`revfactory/harness` の中心的な考え方を Codex 向けに移植したものです。プロジェクト内で再利用できる Codex スキルとワークフロー構成を設計、足場作成、検証、改善するためのハーネスファクトリです。

上流の Harness は Claude Code を前提にしています。この版では同じファクトリの考え方を Codex の構成要素に対応させています。対象は `skills/`、`SKILL.md`、`agents/openai.yaml`、参照ドキュメント、スクリプト、テンプレート、検証チェック、必要に応じたサブエージェントプロトコルです。

## 含まれるもの

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
```

## 実用スキル

| スキル | 用途 |
|---|---|
| `codex-harness` | ハーネスの設計、監査、足場作成、改善 |
| `repo-review` | コードレビュー、PR レビュー、リポジトリ監査、回帰確認 |
| `feature-delivery` | 機能作業の計画、実装、検証、要約 |
| `integration-qa` | 変更後の境界またぎの不整合確認 |
| `docs-maintenance` | README、API ドキュメント、コマンドドキュメント、例の検証 |
| `release-readiness` | リリース前検証、ゲート確認、変更履歴確認、デプロイリスクレビュー |

## 使い方

リポジトリ内のコピーをそのまま使います。

```text
Use $codex-harness at ./skills/codex-harness to design a project harness.
```

代表的な依頼例:

```text
Build a Codex harness for this repository.
Audit the existing Codex harness and evolve it.
Create reusable Codex skills for code review and release readiness.
Design a supervisor skill that routes frontend, backend, and QA workflows.
Use $feature-delivery at ./skills/feature-delivery to implement a bounded feature.
Use $repo-review at ./skills/repo-review to review the current diff.
```

## 新しいスキルの足場作成

```powershell
python .\skills\codex-harness\scripts\scaffold_codex_skill.py repo-review `
  --description "Review this repository for architecture, security, performance, tests, and integration risks. Use when asked for code review, PR review, regression review, or release readiness review." `
  --orchestrator `
  --resources references,scripts
```

スキルを追加するときは、少なくとも `SKILL.md` と `agents/openai.yaml` を含めます。必要に応じて `references/`、`scripts/`、`templates/` を追加します。

## 検証

リポジトリ全体の構造検証:

```powershell
python .\skills\codex-harness\scripts\validate_codex_harness.py .
```

Codex の quick validator がローカルにある場合:

```powershell
python C:\Users\kkmia\.codex\skills\.system\skill-creator\scripts\quick_validate.py .\skills\codex-harness
```

作成または編集した各スキルディレクトリに対して quick validator を実行します。ローカルでスキルごとに検証する例:

```powershell
Get-ChildItem .\skills -Directory | ForEach-Object {
  python .\skills\codex-harness\scripts\validate_codex_harness.py $_.FullName
}
```

GitHub Actions は push と pull request で `.github/workflows/validate.yml` を実行します。このワークフローはリポジトリ全体の検証に加えて、`skills/*` の各スキルを個別に検証し、失敗したスキルディレクトリが分かるようにします。

## ローカルインストール

このハーネスをローカルの Codex セッション全体で使えるようにするには、対象スキルを `~/.codex/skills` にコピーします。

```powershell
$name = "codex-harness"
$dest = Join-Path $env:USERPROFILE ".codex\skills\$name"
New-Item -ItemType Directory -Force -Path (Split-Path $dest) | Out-Null
Copy-Item -Recurse -Force ".\skills\$name" $dest
```

このリポジトリを正本として扱い、ローカルインストール先はキャッシュとして扱います。更新時はリポジトリ側を先に変更し、検証後にローカルへ同期します。

## Issue 駆動の進め方

このリポジトリは小さな issue 単位で前進させます。初期バックログは [docs/issue-roadmap.md](docs/issue-roadmap.md) にあります。

進め方:

1. 上流 Harness から欠けている具体的な機能を 1 つ選ぶ。
2. 1 issue につき 1 つのワークフロー、スキル、検証、またはドキュメント改善に絞る。
3. 変更対象のスキルやドキュメントを更新する。
4. 構造検証と、可能なら代表シナリオでの動作確認を実行する。
5. 変更内容、実行した検証、残るリスクをまとめて issue または PR を閉じる。

スキルを追加または変更した場合は、README の実用スキル表、参照ドキュメント、検証手順も必要に応じて更新します。
