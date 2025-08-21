const verifyAdmin = require('../middleware/auth');
const express = require('express');
const router = express.Router();
const pool = require('../config/db');
const sendContactEmail = require('../utils/mailer'); // Importo funksionin e email-it

// ✅ POST - Ruaj një mesazh në databazë dhe dërgo email
router.post('/contact', (req, res) => {
  const { name, email, message } = req.body;

  // Ruajtja në databazë
  const sql = 'INSERT INTO contact_messages (name, email, message) VALUES (?, ?, ?)';
  pool.query(sql, [name, email, message], (err, result) => {
    if (err) {
      console.error('❌ Gabim gjatë ruajtjes së mesazhit:', err);
      return res.status(500).json({ message: 'Gabim gjatë ruajtjes së mesazhit' });
    }

    // Dërgimi i email-it pas ruajtjes
    sendContactEmail(name, email, message)
      .then(() => {
        res.status(200).json({ message: 'Mesazhi u ruajt dhe emaili u dërgua me sukses!' });
      })
      .catch((emailErr) => {
        console.error('❌ Gabim gjatë dërgimit të email-it:', emailErr);
        res.status(500).json({ message: 'Mesazhi u ruajt, por emaili nuk u dërgua.' });
      });
  });
});

// ✅ GET - Merr të gjitha mesazhet
router.get('/contact', verifyAdmin, (req, res) => {
  const sql = 'SELECT * FROM contact_messages ORDER BY created_at DESC';
  pool.query(sql, (err, results) => {
    if (err) {
      console.error('❌ Gabim gjatë marrjes së mesazheve:', err);
      return res.status(500).json({ message: 'Gabim gjatë marrjes së mesazheve' });
    }
    res.status(200).json(results);
  });
});

// ✅ DELETE - Fshi një mesazh sipas ID-së
router.delete('/contact/:id', (req, res) => {
  const id = req.params.id;
  const sql = 'DELETE FROM contact_messages WHERE id = ?';
  pool.query(sql, [id], (err, result) => {
    if (err) {
      console.error('❌ Gabim gjatë fshirjes së mesazhit:', err);
      return res.status(500).json({ message: 'Gabim gjatë fshirjes së mesazhit' });
    }

    if (result.affectedRows === 0) {
      return res.status(404).json({ message: 'Mesazhi nuk u gjet për t’u fshirë' });
    }

    res.status(200).json({ message: '✅ Mesazhi u fshi me sukses' });
  });
});

module.exports = router;
