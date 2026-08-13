# CAESAR Auditor Platform & ZEV Logistics Ecosystem

An enterprise-grade, multi-agent platform designed for zero-emission vehicle (ZEV) fleet logistics, bidirectional Vehicle-to-Grid (V2G) energy storage management, automated regulatory compliance auditing, and state tax exception tracking.

---

## 🗺️ Repository Structure & Core Subsystems---

## 🧜‍♂️ System Architecture (Mermaid)

`mermaid
flowchart TD
  subgraph CAESAR_Auditor_Platform
    direction TB
    V2G[V2G Syndication]
    CDLS[CDLS Agents Core]
    Sales[Sales Enablement]
    Shared[Shared Data Layer\n(SQL + JSON)]
    Bus[Integration Bus\n(APIs, JS)]
    UI[UI / Frontend\n(JS)]
    Utils[Agent Utils\n(Python)]
    Orch[Orchestration\n(JS/Python)]
    Reports[Reporting & Exports\n(TXT/JSON)]
  end

  V2G -->|writes/reads| Shared
  V2G -->|publishes events| Bus
  CDLS -->|reads/writes| Shared
  CDLS -->|subscribes| Bus
  CDLS -->|uses| Utils
  CDLS -->|coordinated by| Orch
  Sales -->|reads/writes| Shared
  Sales -->|integrates via| Bus
  Bus --> UI
  Shared --> Reports
  Reports --> UI
  Orch --> CDLS
  Orch --> Bus
  Utils --> Shared
⚡ Quick Start & Deployment Pipeline
To launch full ecosystem synchronization and live page builds:

PowerShell
powershell.exe -ExecutionPolicy Bypass -File "Developer_and_Code_Assets\Launch-Ecosystem.ps1"
🌐 Live Web Portal
Access the live dashboard at:

https://juliomanaging-creator.github.io/CDLS-/
