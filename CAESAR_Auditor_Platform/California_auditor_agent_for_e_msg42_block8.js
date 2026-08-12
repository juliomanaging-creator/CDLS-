// Watches folder for new files
watcher.on('add', path => {
  processNewSalesFile(path);
});