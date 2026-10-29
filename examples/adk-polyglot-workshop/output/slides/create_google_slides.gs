/**
 * Google Apps Script to build Google Slides directly in Google Drive.
 * 
 * Instructions:
 * 1. Open https://script.google.com/
 * 2. Create a New Project, paste this code, and click 'Run' -> 'createWorkshopSlides'.
 * 3. A new Google Slides presentation will be created in your Google Drive!
 */
function createWorkshopSlides() {
  const title = "adk-polyglot-workshop";
  const topic = "Multi-Language Agent Systems with Google ADK (Python, Go, Java, Kotlin, TypeScript)";
  const deck = SlidesApp.create(title + " - Presentation");
  
  // Slide 1: Title
  const slide1 = deck.getSlides()[0];
  slide1.getBackground().setSolidFill("#0f172a");
  const titleShape = slide1.insertTextBox(title, 50, 150, 620, 100);
  titleShape.getText().getTextStyle().setFontSize(28).setForegroundColor("#38bdf8").setBold(true);
  const subShape = slide1.insertTextBox(topic + "\nBuild with AI / DevFest Workshop", 50, 260, 620, 60);
  subShape.getText().getTextStyle().setFontSize(16).setForegroundColor("#818cf8");

  // Slide 2: Agenda
  const slide2 = deck.appendSlide(SlidesApp.PredefinedLayout.BLANK);
  slide2.getBackground().setSolidFill("#0f172a");
  const agTitle = slide2.insertTextBox("Workshop Agenda", 50, 40, 620, 50);
  agTitle.getText().getTextStyle().setFontSize(24).setForegroundColor("#38bdf8").setBold(true);
  const agBody = slide2.insertTextBox("• [00 - 15m] Architecture & Prerequisites Setup\n• [15 - 45m] Lab 01 & Lab 02 Hands-on Implementation\n• [45 - 55m] Lab 03 End-to-End Pipeline & Evaluation\n• [55 - 60m] Q&A, Troubleshooting & Wrap-up", 50, 110, 620, 250);
  agBody.getText().getTextStyle().setFontSize(16).setForegroundColor("#f8fafc");

  Logger.log("✅ Google Slides created successfully: " + deck.getUrl());
}
