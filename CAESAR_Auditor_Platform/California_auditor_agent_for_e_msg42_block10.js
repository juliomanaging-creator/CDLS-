// Creates PDFs on dealer's computer
function generateDMVPackage(salesData) {
  const doc = new PDFDocument();
  doc.pipe(fs.createWriteStream('./reports/DMV_Package.pdf'));
  // ... generate complete audit package
}