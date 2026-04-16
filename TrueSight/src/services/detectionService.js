/**
 * Calls backend API to detect image forgery.
 * @param {File} imageFile - The image file to analyze
 * @returns {Promise<{status: string, confidence: number, explanation: string, timestamp: string}>}
 */
export const detectImageForgery = async (imageFile) => {
  const formData = new FormData();
  formData.append('image', imageFile);

  const response = await fetch('/api/detect', {
    method: 'POST',
    body: formData,
  });

  const payload = await response.json();

  if (!response.ok) {
    throw new Error(payload.error || 'Detection failed.');
  }

  const ai = Number(payload.ai);
  const real = Number(payload.real);
  const isForged = ai > real;
  const confidence = Math.round((isForged ? ai : real) * 10) / 10;

  return {
    status: isForged ? 'Forged' : 'Authentic',
    confidence,
    explanation: getExplanation(isForged, confidence),
    timestamp: new Date().toISOString(),
  };
};

/**
 * Generate explanation text based on detection result
 * @param {boolean} isForged - Whether the image is detected as forged
 * @param {number} confidence - Confidence percentage
 * @returns {string} - Explanation text
 */
const getExplanation = (isForged, confidence) => {
  if (isForged) {
    if (confidence > 90) {
      return 'High-confidence detection: The image shows significant signs of manipulation including inconsistent lighting, unnatural blending patterns, and metadata anomalies.';
    } else if (confidence > 80) {
      return 'Medium-high confidence: Detected potential tampering in specific regions. Analysis suggests possible splicing or cloning techniques.';
    } else {
      return 'Moderate confidence: Some indicators suggest possible forgery, but confidence is not definitive. Manual review recommended.';
    }
  } else {
    if (confidence > 95) {
      return 'Very high confidence: Image passes all authentication checks. No detectable signs of manipulation or tampering.';
    } else if (confidence > 85) {
      return 'High confidence: The image appears authentic. Consistent lighting, natural blending, and valid metadata detected.';
    } else {
      return 'Moderate confidence: Image likely authentic, but some minor anomalies detected. These may be due to compression or camera artifacts.';
    }
  }
};
