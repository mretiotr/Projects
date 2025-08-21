const express = require('express');
const router = express.Router();
const pool = require('../config/db');

router.post('/order', (req, res) => {
  const { name, email, items, total_price } = req.body;

  const values = items.map(item => [
    name,
    email,
    item.name,
    item.quantity,
    item.price,
    item.image,
    total_price
  ]);

  const sql = `INSERT INTO orders 
    (name, email, item_name, quantity, price, image_url, total_price) 
    VALUES ?`;

  pool.query(sql, [values], (err, result) => {
    if (err) {
      console.error('❌ Gabim gjatë ruajtjes së porosisë:', err);
      return res.status(500).json({ message: 'Gabim gjatë ruajtjes së porosisë' });
    }
    res.status(201).json({ message: '✅ Porosia u ruajt me sukses!' });
  });
});

module.exports = router;
