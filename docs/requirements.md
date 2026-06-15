# Project Requirements: Prop Firm Confidential

## 1. Introduction

This document captures the functional and non-functional requirements for the Prop Firm Confidential platform. The initial focus is a data-driven prop firm comparison and evaluation tool for futures traders, with room to expand into a broader research and automation pipeline.

## 2. Functional Requirements

### 2.1. Core Comparison
- List prop firms and their evaluation/funded accounts.
- Display key account attributes to support comparison.
- Allow users to filter and sort accounts.

### 2.2. Data Model
- **Firm**: `firm_information` block with `firm_name`, `firm_logo_url`, `firm_url`, `location`.
- **Account**: one record per account tier, not one per firm. Each account is an `account_details` block with `account_name`, `account_size`, `price`, `sale_price`, `profit_split`, `profit_target`, `daily_drawdown`, `max_drawdown`, `drawdown_type`, and `activation_fee`.
- **Rules**: `rules_and_parameters` with `min_trading_days`, `max_trading_days`, `allowed_instruments`, and `scaling_plan`.
- Multiple accounts may exist per firm; the dataset should store all observed account tiers for each firm.

### 2.3. Data Requirements
- Account pricing and activation fees must include all listed tiers from official firm pages.
- Activation fees must be validated from official sources, not inferred from cached or third-party data.
- Recurring-vs-one-time fee structure should be captured (`price` semantics documented per firm: monthly subscription or one-time evaluation fee).

### 2.4. User Interface
- A responsive table/card listing of accounts.
- Filter controls for account size, price, drawdown type, and firm.
- Sorting by price, account size, profit target, and drawdown.
- Search by firm or account name.

### 2.5. Future Enhancements
- User accounts and saved preferences.
- Side-by-side compare view.
- Proprietary scoring models built on top of the underlying data.

## 3. Non-Functional Requirements

### 3.1. Performance
- Page load target: under 3 seconds.
- API response target: under 500ms.

### 3.2. Reliability and Accuracy
- Dataset must be reviewed and updated regularly.
- Prices and rules should be sourced from official pages or recognized references whenever possible.

### 3.3. Technology
- Frontend: Next.js.
- Backend: FastAPI.
- Data store: JSON-backed during MVP; database migration path preserved for future phases.
- Deployment: frontend on Netlify; backend on Railway/Heroku or equivalent.

### 3.4. Usability
- Responsive design across devices.
- Clean, modern interface suited to trader workflows.

### 3.5. Domain and Branding
- Current working domain: `tempus.dpdns.org`
- Future production domain: not yet finalized; preference is an SEO-friendly, brandable domain for public launch.
