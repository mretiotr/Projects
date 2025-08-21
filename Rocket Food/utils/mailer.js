const nodemailer = require('nodemailer');

// Transportuesi – konfigurimi i email-it
const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: 'andishkoza8@gmail.com',          // ← vendos emailin tënd
    pass: 'oedldvlhvyfhfjwy'     // ← përdor një "App Password"
  }
});

// Funksioni për të dërguar email
function sendContactEmail(name, email, message) {
  const mailOptions = {
    from: `"${name}" <${email}>`,
    to: 'andishkoza8@gmail.com', // ← vendos ku do ta marrësh emailin
    subject: 'Mesazh i ri nga Rocket Food',
    text: `Emër: ${name}\nEmail: ${email}\n\nMesazh:\n${message}`
  };

  return transporter.sendMail(mailOptions);
}

module.exports = sendContactEmail;
