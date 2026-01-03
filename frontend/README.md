# Frontend - Japan Fertility Workstyle Analysis

React + TypeScriptを使用したフロントエンドアプリケーション。パネルデータ分析のユーザーインターフェースを提供します。

## 📋 概要

このフロントエンドは以下の責務を担っています：

- CSVファイルのアップロードUI
- 従属変数・独立変数の選択インターフェース
- バックエンドAPIとの通信
- 分析結果の可視化と表示
- エラーメッセージの表示
- レスポンシブデザイン対応

## 🛠️ 技術スタック

| カテゴリ | 技術 | バージョン | 用途 |
|---------|------|----------|------|
| 言語 | TypeScript | 5.9+ | 型安全なJavaScript |
| フレームワーク | React | 19.2+ | UIライブラリ |
| ビルドツール | Vite | 7.2+ | 高速開発サーバー・ビルド |
| スタイリング | Tailwind CSS | 4.1+ | ユーティリティファーストCSS |
| リンター | ESLint | 9.39+ | コード品質チェック |
| 型チェック | TypeScript | 5.9+ | 静的型検証 |

## 🏗️ ディレクトリ構造

```
src/
├── api/                      # APIクライアント
│   └── analysisApi.ts        # 分析APIとの通信
├── components/               # 再利用可能なコンポーネント
│   ├── AnalysisForm.tsx      # 分析フォーム
│   └── AnalysisResult.tsx    # 分析結果表示
├── hooks/                    # カスタムフック
│   └── useAnalysis.ts        # 分析ロジックのフック
├── pages/                    # ページコンポーネント
│   └── AnalysisPage.tsx      # メイン分析ページ
├── types/                    # TypeScript型定義
│   └── analysis.ts           # 分析関連の型
├── utils/                    # ユーティリティ関数
├── App.tsx                   # ルートコンポーネント
├── main.tsx                  # アプリケーションエントリーポイント
└── index.css                 # グローバルスタイル
```

### 主要コンポーネント

#### 1. AnalysisPage (`pages/AnalysisPage.tsx`)
- メイン画面を構成
- フォームと結果表示を統合
- スクロール動作の制御

#### 2. AnalysisForm (`components/AnalysisForm.tsx`)
- CSVファイルアップロード
- 従属変数・独立変数の選択
- フォーム送信
- エラー表示

#### 3. AnalysisResult (`components/AnalysisResult.tsx`)
- 分析結果の表形式表示
- 係数、標準誤差、t統計量、p値の表示
- R²統計量の表示
- 除外された変数の警告表示

#### 4. useAnalysis (`hooks/useAnalysis.ts`)
- 分析ロジックの状態管理
- API呼び出し
- エラーハンドリング

## 🚀 セットアップ

### 前提条件
- Node.js 18以上
- npm または yarn

### インストール

```bash
cd frontend
npm install
```

## 🏃 実行方法

### 開発サーバーの起動

```bash
npm run dev
```

開発サーバーが http://localhost:5173 で起動します。

**特徴**:
- ホットリロード（HMR）による高速な開発体験
- TypeScriptの型チェック
- ESLintによる自動リンティング

### 本番ビルド

```bash
npm run build
```

ビルド成果物は `dist/` ディレクトリに出力されます。

### ビルド結果のプレビュー

```bash
npm run preview
```

本番ビルドをローカルで確認できます。

## 🧪 テストとリンティング

### リンティング

```bash
npm run lint
```

ESLintによるコード品質チェックを実行します。

### 型チェック

```bash
npm run typecheck
```

TypeScriptの型エラーをチェックします。

## 📡 API連携

### バックエンドAPIとの通信

`src/api/analysisApi.ts` でバックエンドAPIとの通信を実装しています。

```typescript
export async function analyzeData(
  csvFile: File,
  dependentVar: string,
  independentVars: string[]
): Promise<AnalysisResult>
```

**使用例**:
```typescript
import { analyzeData } from './api/analysisApi';

const result = await analyzeData(
  csvFile,
  'fertility_rate',
  ['working_hours', 'childcare_leave_rate']
);
```

### API接続先の設定

開発環境では `vite.config.ts` でプロキシを設定しています。

```typescript
export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
});
```

本番環境では環境変数 `VITE_API_BASE_URL` で設定可能です。

## 🎨 スタイリング

### Tailwind CSS 4

Utility-firstアプローチでスタイリングを実装しています。

**主な設定**:
- Tailwind CSS 4のViteプラグインを使用
- レスポンシブデザイン対応
- カスタムカラーパレット設定可能

**カスタマイズ**:
`tailwind.config.ts` でカラー、スペーシング等を設定できます。

### グローバルスタイル

`src/index.css` にグローバルスタイルを定義しています。

## 🔧 設定ファイル

### Vite設定 (`vite.config.ts`)
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  // プロキシ、ビルド設定等
})
```

### TypeScript設定

#### `tsconfig.json` (プロジェクト全体)
基本的なTypeScript設定

#### `tsconfig.app.json` (アプリケーション用)
```json
{
  "extends": "./tsconfig.json",
  "compilerOptions": {
    "target": "ES2020",
    "jsx": "react-jsx",
    "strict": true
  }
}
```

#### `tsconfig.node.json` (Node.js用)
Vite設定ファイル用の型設定

### ESLint設定 (`eslint.config.js`)
```javascript
import js from '@eslint/js'
import reactHooks from 'eslint-plugin-react-hooks'
import reactRefresh from 'eslint-plugin-react-refresh'
import tseslint from 'typescript-eslint'

export default tseslint.config(
  // ... ルール設定
)
```

## 📦 主要な依存関係

### 本番依存関係
```json
{
  "react": "^19.2.0",           // UIライブラリ
  "react-dom": "^19.2.0",       // DOMレンダリング
  "tailwindcss": "^4.1.18",     // CSSフレームワーク
  "@tailwindcss/vite": "^4.1.18" // Viteプラグイン
}
```

### 開発依存関係
```json
{
  "@vitejs/plugin-react": "^5.1.1",      // React用Viteプラグイン
  "typescript": "~5.9.3",                // TypeScriptコンパイラ
  "eslint": "^9.39.1",                   // リンター
  "vite": "^7.2.4"                       // ビルドツール
}
```

## 🔒 型安全性

### 主要な型定義 (`src/types/analysis.ts`)

```typescript
export interface AnalysisResult {
  nobs: number;                          // 観測数
  params: Record<string, number>;        // 係数
  std_errors: Record<string, number>;    // 標準誤差
  tstats: Record<string, number>;        // t統計量
  pvalues: Record<string, number>;       // p値
  rsquared_within: number;               // R² Within
  rsquared_between: number;              // R² Between
  rsquared_overall: number;              // R² Overall
  dropped_vars: string[];                // 除外された変数
}
```

### 型安全なAPI呼び出し

TypeScriptの型定義により、コンパイル時にAPI仕様の不一致を検出できます。

## 🎯 UI/UXの特徴

### レスポンシブデザイン
- モバイルファーストアプローチ
- タブレット・デスクトップ対応
- Tailwindのブレークポイント活用

### アクセシビリティ
- セマンティックHTML
- ARIA属性の適切な使用
- キーボードナビゲーション対応

### ユーザーエクスペリエンス
- ローディング状態の表示
- エラーメッセージの明確な表示
- 分析結果へのスムーズなスクロール
- 視覚的に分かりやすい結果表示

## 🐛 デバッグ

### React Developer Tools
```bash
# ブラウザ拡張機能をインストール
# Chrome: React Developer Tools
```

### Viteのデバッグモード
```bash
npm run dev -- --debug
```

### TypeScriptエラーの詳細表示
```bash
npm run typecheck -- --pretty
```

## 📊 パフォーマンス最適化

### Viteの最適化機能
- Tree shaking: 未使用コードの削除
- Code splitting: 動的インポートによる分割
- Minification: コードの最小化
- ESBuild: 高速なトランスパイル

### React最適化
- useMemo / useCallback の適切な使用
- コンポーネントの適切な分割
- 不要な再レンダリングの防止

## 🔄 開発フロー

### 1. 機能追加の流れ
```bash
# 1. 新しいブランチを作成
git checkout -b feature/new-feature

# 2. コードを編集
# 3. 型チェックとリンティング
npm run typecheck
npm run lint

# 4. ビルドテスト
npm run build

# 5. コミット
git add .
git commit -m "Add new feature"
```

### 2. コードスタイル
- 関数コンポーネント優先
- TypeScriptの型定義を徹底
- Propsインターフェースの明示
- カスタムフックによるロジック分離

## 🚀 デプロイ

### Nginxでのデプロイ（Docker使用）

```bash
# 1. ビルド
npm run build

# 2. Docker Composeで起動
docker-compose up frontend
```

`docker-compose.yml` の設定:
```yaml
services:
  frontend:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./frontend/dist:/usr/share/nginx/html
```

### 静的ホスティングサービス
以下のサービスに簡単にデプロイ可能:
- Vercel
- Netlify
- GitHub Pages
- Cloudflare Pages

## 🎯 今後の拡張案

- [ ] ユニットテストの追加（Vitest / React Testing Library）
- [ ] E2Eテストの追加（Playwright / Cypress）
- [ ] 国際化（i18n）対応
- [ ] ダークモード対応
- [ ] 分析結果のエクスポート機能（CSV, PDF）
- [ ] 複数ファイルの比較機能
- [ ] データビジュアライゼーション（チャート）の追加
- [ ] PWA対応

## 📚 参考資料

- [React公式ドキュメント](https://react.dev/)
- [TypeScript公式ドキュメント](https://www.typescriptlang.org/)
- [Vite公式ドキュメント](https://vitejs.dev/)
- [Tailwind CSS公式ドキュメント](https://tailwindcss.com/)
- [ESLint公式ドキュメント](https://eslint.org/)
