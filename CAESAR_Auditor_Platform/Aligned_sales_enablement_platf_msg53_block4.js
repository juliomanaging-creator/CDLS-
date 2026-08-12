const { jsPDF } = window.jspdf;
const doc = new jsPDF();

// Add logo
doc.addImage(logoBase64, 'PNG', 10, 10, 40, 15);

// Add title
doc.setFontSize(20);
doc.text('EV Fleet ROI Analysis', 105, 35, { align: 'center' });

// Add dealer info
doc.setFontSize(12);
doc.text(`Prepared for: ${dealerName.value}`, 20, 50);
doc.text(`Date: ${new Date().toLocaleDateString()}`, 20, 57);

// Add results table
doc.autoTable({
  startY: 70,
  head: [['Metric', 'Diesel Fleet', 'EV Fleet', 'Savings']],
  body: [
    ['Annual Fuel Cost', `$${dieselCost.value}`, `$${evCost.value}`, `$${savings.value}`],
    ['Maintenance Cost', `$${dieselMaint.value}`, `$${evMaint.value}`, `$${maintSavings.value}`],
    ['Carbon Credits', '$0', `$${carbonRevenue.value}`, `$${carbonRevenue.value}`],
    ['Total Annual', `$${dieselTotal.value}`, `$${evTotal.value}`, `$${totalSavings.value}`]
  ]
});

// Add charts
const chartImage = chartComponent.getImage();
doc.addImage(chartImage, 'PNG', 20, 120, 170, 80);

// Save
doc.save(`CDLS_ROI_Analysis_${dealerName.value}.pdf`);