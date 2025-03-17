const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const sizes = [32, 64, 128, 256, 512];
const inputFile = path.join(__dirname, '../src/assets/logo.svg');
const outputDir = path.join(__dirname, '../src/assets');

// Ensure output directory exists
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

// Generate PNG versions in different sizes
sizes.forEach(size => {
  sharp(inputFile)
    .resize(size, size)
    .png()
    .toFile(path.join(outputDir, `logo-${size}.png`))
    .then(() => console.log(`Generated ${size}x${size} PNG`))
    .catch(err => console.error(`Error generating ${size}x${size} PNG:`, err));
}); 