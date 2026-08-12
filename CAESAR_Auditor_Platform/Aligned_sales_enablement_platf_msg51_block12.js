// Track email opens
Email includes: <img src="track.cdls.com/open/{dealerId}" />

// Track link clicks  
All links go through: redirect.cdls.com/click/{linkId}

// Lead scoring
if (emailOpened && linksClicked > 2 && calculatorRuns > 3) {
  leadScore = "Hot";
  notifyTeam("High-intent dealer: " + dealerName);
}