const { chromium } = require('playwright');
const { PDFDocument } = require('pdf-lib');
const fs = require('fs');
const path = require('path');

(async () => {
  const VIEWPORT  = { width: 1440, height: 810 };
  const HTML_FILE = path.resolve(__dirname, 'slides-JPMCBIAI.html');
  const OUT_PDF   = path.resolve(__dirname, 'AIBuilderLevel1.pdf');

  console.log('Launching Chromium…');
  const browser  = await chromium.launch({ headless: true });

  // deviceScaleFactor: 3 → captures at 4320×2430 px (3× retina)
  // PDF page dimensions stay at 1440×810 pt — text and edges stay sharp
  const context  = await browser.newContext({
    viewport: VIEWPORT,
    deviceScaleFactor: 3,
  });
  const page = await context.newPage();
  await page.goto(`file://${HTML_FILE}`, { waitUntil: 'networkidle' });

  // Wait for Google Fonts + transitions to settle
  await page.waitForTimeout(1500);

  // Count slides
  const slideCount = await page.locator('.slide').count();
  console.log(`Found ${slideCount} slides.`);

  const jpegBuffers = [];

  for (let i = 0; i < slideCount; i++) {
    console.log(`  Capturing slide ${i + 1} / ${slideCount}…`);

    // Activate the target slide, deactivate all others
    await page.evaluate((idx) => {
      document.querySelectorAll('.slide').forEach((s, j) => {
        s.classList.toggle('active', j === idx);
        // Bypass the CSS opacity transition so the screenshot is instant
        s.style.transition = 'none';
        s.style.opacity    = j === idx ? '1' : '0';
        s.style.pointerEvents = j === idx ? 'all' : 'none';
      });
      // Update progress bar
      const total = document.querySelectorAll('.slide').length;
      const bar   = document.getElementById('prog');
      if (bar) bar.style.width = ((idx + 1) / total * 100) + '%';
    }, i);

    // Short settle after DOM change
    await page.waitForTimeout(120);

    const slide  = page.locator('.slide').nth(i);
    const buffer = await slide.screenshot({ type: 'jpeg', quality: 100 });
    jpegBuffers.push(buffer);
  }

  await browser.close();
  console.log('Browser closed. Assembling PDF…');

  // Build PDF — one page per slide at 1440×810 pts
  const pdfDoc = await PDFDocument.create();

  for (let i = 0; i < jpegBuffers.length; i++) {
    const jpgImage = await pdfDoc.embedJpg(jpegBuffers[i]);
    const page     = pdfDoc.addPage([VIEWPORT.width, VIEWPORT.height]);
    page.drawImage(jpgImage, {
      x: 0, y: 0,
      width:  VIEWPORT.width,
      height: VIEWPORT.height,
    });
  }

  const pdfBytes = await pdfDoc.save();
  fs.writeFileSync(OUT_PDF, pdfBytes);

  const sizeMB = (pdfBytes.length / 1024 / 1024).toFixed(2);
  console.log(`\n✅ PDF saved: ${OUT_PDF}`);
  console.log(`   ${slideCount} pages · ${sizeMB} MB`);
})();
