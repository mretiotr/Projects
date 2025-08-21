
const express = require('express');
const router = express.Router();
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const pool = require('../config/db');

const SECRET_KEY = 'sekreti_yt_super_i_fshehtë'; // e ruajmë këtu për JWT

// ✅ REGJISTRIM
router.post('/signup', async (req, res) => {
  const { name, email, password } = req.body;
  try {
    const hashedPassword = await bcrypt.hash(password, 10);

    // Default role = 'user'
    const [rows] = await pool.promise().query(
      'INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)',
      [name, email, hashedPassword, 'user']
    );

    res.status(201).json({ message: 'User registered successfully' });
  } catch (err) {
    console.error(err);
    if (err.code === 'ER_DUP_ENTRY') {
      res.status(400).json({ error: 'Email already exists' });
    } else {
      res.status(500).json({ error: 'Server error' });
    }
  }
});

// ✅ LOGIN
router.post('/signin', async (req, res) => {
  const { email, password } = req.body;
  try {
    const [rows] = await pool.promise().query(
      'SELECT * FROM users WHERE email = ?',
      [email]
    );

    if (rows.length === 0) {
      return res.status(401).json({ error: 'Invalid email or password' });
    }

    const user = rows[0];
    const match = await bcrypt.compare(password, user.password);

    if (!match) {
      return res.status(401).json({ error: 'Invalid email or password' });
    }

    // ✅ Krijo JWT token
    const token = jwt.sign(
      { id: user.id, role: user.role },
      SECRET_KEY,
      { expiresIn: '1h' }
    );

    res.json({
      message: 'Login successful',
      token,
      user: { id: user.id, name: user.name, email: user.email, role: user.role }
    });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Server error' });
  }
});

module.exports = router;
