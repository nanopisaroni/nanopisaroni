import { launch } from 'puppeteer';
const browser = await launch({ 
  headless: true,
  args: ['--no-sandbox', '--disable-setuid-sandbox'],
  executablePath: '/home/nanobot/.cache/puppeteer/chrome/linux-147.0.7727.57/chrome-linux64/chrome'
});
const page = await browser.newPage();
await page.setViewport({ width: 800, height: 700 });
await page.goto('http://localhost:9876/index.html', { waitUntil: 'networkidle0' });
await page.screenshot({ path: '/tmp/sitio-preview.png', fullPage: true });
console.log('Screenshot saved');
await browser.close();
