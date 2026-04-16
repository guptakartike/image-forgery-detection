const express = require('express');
const multer = require('multer');
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');
const path = require('path');

const router = express.Router();

const buildPredictUrl = (port) => `http://127.0.0.1:${port}/predict`;

const DEFAULT_MODEL_PORTS = Array.from({ length: 11 }, (_, index) => 5000 + index);

const resolveCandidateUrls = () => {
  const envUrl = process.env.AI_MODEL_URL;
  if (envUrl) {
    return [envUrl];
  }

  return DEFAULT_MODEL_PORTS.map((port) => buildPredictUrl(port));
};

const getHealthInfo = async (predictUrl) => {
  try {
    if (!predictUrl.includes('/predict')) {
      return { healthy: false, modern: false };
    }

    const healthUrl = predictUrl.replace('/predict', '/health');
    const healthResponse = await axios.get(healthUrl, { timeout: 1500 });
    const data = healthResponse.data || {};

    return {
      healthy: healthResponse.status === 200,
      modern: Object.prototype.hasOwnProperty.call(data, 'modelLoaded'),
    };
  } catch (error) {
    return { healthy: false, modern: false };
  }
};

const findReachableModelUrl = async () => {
  const candidates = resolveCandidateUrls();

  // If URL is explicitly configured, trust that and only validate reachability.
  if (process.env.AI_MODEL_URL) {
    const info = await getHealthInfo(candidates[0]);
    return info.healthy ? candidates[0] : null;
  }

  for (const candidate of candidates) {
    // eslint-disable-next-line no-await-in-loop
    const info = await getHealthInfo(candidate);
    if (info.healthy && info.modern) {
      return candidate;
    }
  }

  for (const candidate of candidates) {
    // eslint-disable-next-line no-await-in-loop
    const info = await getHealthInfo(candidate);
    if (info.healthy) {
      return candidate;
    }
  }

  return null;
};

// Store uploads temporarily
const upload = multer({
  dest: path.join(__dirname, '../uploads/'),
  limits: { fileSize: 5 * 1024 * 1024 }, // 5MB max
  fileFilter: (req, file, cb) => {
    const allowed = ['image/jpeg', 'image/png', 'image/webp'];
    if (allowed.includes(file.mimetype)) {
      cb(null, true);
    } else {
      cb(new Error('Only JPG, PNG, and WEBP files are allowed.'));
    }
  },
});

// POST /api/detect
router.post('/detect', upload.single('image'), async (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: 'No image file uploaded.' });
  }

  const filePath = req.file.path;

  try {
    const modelUrl = await findReachableModelUrl();
    if (!modelUrl) {
      throw new Error('No reachable AI model server found on expected ports (5000-5010).');
    }

    // Forward image to Python AI server
    const form = new FormData();
    form.append('image', fs.createReadStream(filePath));

    const response = await axios.post(modelUrl, form, {
      headers: form.getHeaders(),
      timeout: 30000,
    });

    res.json(response.data); // { real: 72.4, ai: 27.6 }
  } catch (err) {
    const upstreamError = err.response?.data?.error;
    console.error('AI model request failed:', upstreamError || err.message);
    res.status(502).json({
      error: upstreamError || 'AI model server is unavailable. Please try again later.',
    });
  } finally {
    // Clean up temp file
    fs.unlink(filePath, () => {});
  }
});

module.exports = router;
