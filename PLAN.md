# SuperCrawl Implementation Plan

## Project Overview
SuperCrawl is a multi-tenant, AI-powered SEO crawler and website auditor. It leverages Google Gemini for intelligent analysis and RAG capabilities, Supabase for backend/database, and a modern React/Shadcn frontend.

**Goal:** Build a premium, subscription-based SaaS that outperforms competitors like Screaming Frog by integrating deep AI analysis.

## Phase 1: Foundation & Infrastructure
**Objective:** Set up the core environment, database, and basic application structure.

### 1.1 Project Setup
- Initialize Git repository structure.
- Set up Python Flask backend environment (Virtualenv, Dependencies).
- Set up React/Vite frontend environment.
- Configure `settings_manager.py` for environment variables.

### 1.2 Supabase Configuration (Project: xgaqpazeyztyailjpsir)
- **Database Schema:**
    - `users` (Profile, Subscription Tier, Usage Stats)
    - `projects` (Domains to crawl)
    - `crawls` (Crawl sessions, Status, Config)
    - `pages` (Crawled URLs, Metadata, SEO Metrics)
    - `links` (Internal/External link graph)
    - `issues` (Detected SEO issues)
    - `vectors` (pgvector store for RAG)
- **Auth:** Configure Supabase Auth (Email/Password, Google OAuth).
- **Storage:** Buckets for export files (CSV/JSON/XML).

### 1.3 Google Cloud & AI Setup
- Configure Google Gemini API access.
- Set up Google PageSpeed Insights API key.
- Initialize Google Cloud Project for any required compute resources.

## Phase 2: Core Crawler Engine
**Objective:** Build the robust crawling logic capable of handling JS and static sites.

### 2.1 Crawler Architecture (`src/crawler.py`)
- **Engine:** Hybrid approach using `aiohttp` for speed and `Playwright` for JavaScript rendering.
- **Queue System:** Redis + Celery for managing crawl jobs and concurrency.
- **Politeness:** Implement `robots.txt` parsing, delays, and user-agent rotation.

### 2.2 Multi-tenancy & Persistence
- **Session Isolation:** Ensure crawl data is strictly scoped to `user_id` and `project_id`.
- **State Management:** Use Redis to track active crawls and progress.
- **LocalStorage Sync:** Frontend to sync crawler settings to local storage for persistence.

### 2.3 Data Extraction
- **SEO Metadata:** Title, Description, H1-H6, Canonical, Meta Robots.
- **Link Analysis:** Extract all `href`s, classify as Internal/External, check status codes (404, 301, etc.).
- **Content Extraction:** Clean HTML to text for AI processing.

## Phase 3: Data Processing & AI Integration
**Objective:** Turn raw crawl data into actionable insights using AI.

### 3.1 Vector Database & RAG
- **Embedding:** Chunk page content and generate embeddings using Gemini.
- **Storage:** Store embeddings in Supabase `vectors` table.
- **Retrieval:** Implement similarity search for "Chat with Site" feature.

### 3.2 AI Analysis Pipeline
- **Page Analysis:** Send page content to Gemini to generate:
    - Summary
    - Sentiment
    - Keyword extraction
    - Content quality score
- **Issue Detection:** Rule-based + AI-based detection (e.g., "Content sounds generic", "Missing alt text context").

### 3.3 PageSpeed Integration
- Integration with Google PageSpeed Insights API.
- Store Core Web Vitals (LCP, FID, CLS) for each page.

## Phase 4: Frontend & User Experience
**Objective:** Build a stunning, premium UI using Shadcn components.

### 4.1 Design System
- **Framework:** React + Tailwind CSS + Shadcn UI.
- **Theme:** Dark/Light mode support, custom CSS injection capabilities.
- **Layout:** Sidebar navigation, Dashboard overview, Detailed data tables.

### 4.2 Core Views
- **Dashboard:** Live crawl progress, aggregate stats (Pages crawled, Issues found, Health score).
- **Explorer:** Data grid view of all pages with filtering/sorting.
- **Chat Interface:** Chatbot UI to query the crawled site data (RAG).
- **Settings:** Crawler configuration (Depth, Speed, User Agent).

### 4.3 Real-time Updates
- Implement WebSockets (or Supabase Realtime) to stream crawl progress to the UI.

## Phase 5: Billing & Monetization
**Objective:** Implement subscription model and payment processing.

### 5.1 Stripe Integration
- **Products:**
    - Starter (Free, 3 crawls/week)
    - Professional ($40/mo, 100 crawls/mo)
    - Ultra ($150/mo, 300 crawls/mo)
- **Checkout:** Stripe Checkout for subscriptions.
- **Portal:** Customer portal for managing subscriptions.

### 5.2 Usage Enforcement
- Middleware to check crawl limits before starting a job.
- Cron job to reset weekly/monthly limits.

## Phase 6: Advanced Features & API
**Objective:** Extend functionality for developers and power users.

### 6.1 API & MCP
- **REST API:** Expose endpoints for starting crawls and retrieving data.
- **MCP Server:** Build a Model Context Protocol server to allow AI agents (like Claude/Gemini) to use SuperCrawl tools directly.

### 6.2 Export System
- Generators for CSV, JSON, and XML sitemaps.
- Direct download or email delivery.

## Phase 7: Deployment & SEO
**Objective:** Launch the application and ensure it ranks well.

### 7.1 Deployment
- **Backend:** Deploy Flask + Celery to Google Cloud Run or similar container service.
- **Frontend:** Deploy to Vercel or Netlify.
- **Database:** Managed Supabase instance.

### 7.2 Platform SEO
- Implement SSR (Server Side Rendering) or Prerendering for the marketing pages.
- Generate dynamic sitemap for `supercrawl.ai`.
- Optimize meta tags and structured data for the landing page.
