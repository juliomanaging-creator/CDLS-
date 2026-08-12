# CalPERS-specific with carbon allocation
result = agent.execute('generate_term_sheet', {
    'series': 'B',
    'investment_amount': 50000000,
    'investor_name': 'CalPERS',
    'carbon_allocation': True,
    'carbon_percentage': 20
})