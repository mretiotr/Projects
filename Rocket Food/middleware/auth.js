const jwt = require('jsonwebtoken');
const SECRET_KEY = 'sekreti_yt_super_i_fshehtë';

function verifyAdmin(req, res, next) {
  const authHeader = req.headers.authorization;
  if (!authHeader) {
    return res.status(401).json({ error: 'Access denied, no token provided' });
  }

  const token = authHeader.split(' ')[1]; // format: "Bearer TOKEN"
  try {
    const decoded = jwt.verify(token, SECRET_KEY);
    if (decoded.role !== 'admin') {
      return res.status(403).json({ error: 'Access forbidden: admin only' });
    }

    req.user = decoded;
    next();
  } catch (err) {
    return res.status(400).json({ error: 'Invalid token' });
  }
}

module.exports = verifyAdmin;
