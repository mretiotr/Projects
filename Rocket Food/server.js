const express = require('express');
const cors = require('cors');
const path = require('path');
const pool = require('./config/db');

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Serve static frontend files (HTML, CSS, JS) nga folderi public
app.use(express.static(path.join(__dirname, 'public')));

// Routes
const authRoutes = require('./routes/auth');
app.use('/api', authRoutes);

const contactRoutes = require('./routes/contact');
app.use('/api', contactRoutes);

const orderRoutes = require('./routes/orders'); //
app.use('/api', orderRoutes);

// Test route për kontroll
app.get('/', (req, res) => {
  res.send('🚀 Rocket Food backend is running!');
});

// Run server
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`✅ Server is running on http://localhost:${PORT}`);
});
