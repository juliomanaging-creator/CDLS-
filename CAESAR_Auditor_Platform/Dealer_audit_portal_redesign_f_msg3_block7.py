sub_data = [[
    Paragraph(f"{num}.{sub_num}", ...),
    Paragraph(f"<b>{heading}</b>", ...),
]]
sub_t = Table(sub_data, colWidths=[0.45*inch, 6.05*inch])
sub_t.setStyle(...)
sub_items.append(sub_t)