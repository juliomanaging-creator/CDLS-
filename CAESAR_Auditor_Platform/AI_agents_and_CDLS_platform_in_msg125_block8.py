# Agents talk to each other automatically

document_drafting_agent.message(financial_modeling_agent,
    "I need carbon allocation % for term sheet"
)

financial_modeling_agent.responds(
    "Carbon allocation: 20% (1.26M MT CO2, NPV $136.4M)"
)

document_drafting_agent.generates(
    "Term sheet with carbon section included"
)