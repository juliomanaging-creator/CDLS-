// CalPERS Institutional Investor Template
const calPERSTemplate = {
  name: "Institutional Investor Due Diligence",
  items: [
    {
      title: "Initial Pitch Presentation",
      type: "milestone",
      owner: "internal",
      duration_days: 0
    },
    {
      title: "NDA Execution",
      type: "task",
      owner: "shared",
      duration_days: 3,
      dependencies: []
    },
    {
      title: "Detailed Financial Model Review",
      type: "task",
      owner: "investor",
      duration_days: 14,
      dependencies: ["NDA Execution"]
    },
    {
      title: "Investment Committee Presentation",
      type: "milestone",
      owner: "investor",
      duration_days: 7,
      dependencies: ["Detailed Financial Model Review"]
    },
    {
      title: "Legal Due Diligence",
      type: "task",
      owner: "shared",
      duration_days: 21,
      dependencies: ["Investment Committee Presentation"]
    },
    {
      title: "Final Investment Committee Vote",
      type: "decision_point",
      owner: "investor",
      duration_days: 14,
      dependencies: ["Legal Due Diligence"]
    },
    {
      title: "Term Sheet Negotiation",
      type: "task",
      owner: "shared",
      duration_days: 10,
      dependencies: ["Final Investment Committee Vote"]
    },
    {
      title: "Definitive Agreement Execution",
      type: "milestone",
      owner: "shared",
      duration_days: 7,
      dependencies: ["Term Sheet Negotiation"]
    },
    {
      title: "Funding Close",
      type: "milestone",
      owner: "shared",
      duration_days: 0,
      dependencies: ["Definitive Agreement Execution"]
    }
  ]
};