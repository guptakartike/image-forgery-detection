import { useState, useRef } from 'react';

/**
 * ImageUpload Component
 * Handles image file upload via drag-and-drop or file input
 * Validates file type and size
 * Displays image preview
 */
export default function ImageUpload({ onImageSelect, isLoading }) {
  const [preview, setPreview] = useState(null);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);
  const [fileName, setFileName] = useState(null);
  const [dragOver, setDragOver] = useState(false);

  // Allowed file types
  const ALLOWED_TYPES = ['image/jpeg', 'image/png'];
  const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB

  /**
   * Validate file before processing
   * @param {File} file - File to validate
   * @returns {boolean} - True if valid
   */
  const validateFile = (file) => {
    setError(null);

    // Check file type
    if (!ALLOWED_TYPES.includes(file.type)) {
      setError('Please upload a JPG or PNG file.');
      return false;
    }

    // Check file size
    if (file.size > MAX_FILE_SIZE) {
      setError('File size must be less than 5MB.');
      return false;
    }

    return true;
  };

  /**
   * Process selected file
   * @param {File} file - File to process
   */
  const processFile = (file) => {
    if (!validateFile(file)) return;

    setFileName(file.name);

    // Create preview
    const reader = new FileReader();
    reader.onload = (e) => {
      setPreview(e.target.result);
    };
    reader.readAsDataURL(file);

    // Call parent callback
    onImageSelect(file);
  };

  /**
   * Handle file input change
   */
  const handleFileInput = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      processFile(file);
    }
  };

  /**
   * Handle drag and drop
   */
  const handleDragOver = (e) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);

    const file = e.dataTransfer.files?.[0];
    if (file) {
      processFile(file);
    }
  };

  /**
   * Trigger file input when upload area is clicked
   */
  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  /**
   * Clear uploaded image and reset form
   */
  const handleClear = () => {
    setPreview(null);
    setError(null);
    setFileName(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto">
      {!preview ? (
        <div
          className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-all duration-300 ${
            dragOver
              ? 'border-trust-700 bg-trust-100 shadow-lg shadow-trust-500/15'
              : 'border-trust-600 bg-trust-50 hover:bg-trust-100 hover:shadow-lg hover:shadow-trust-500/10'
          }`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={handleUploadClick}
          role="button"
          tabIndex={0}
          aria-label="Upload image by dragging or clicking"
          onKeyDown={(e) => {
            if (e.key === 'Enter' || e.key === ' ') {
              handleUploadClick();
            }
          }}
        >
          <div className="text-4xl mb-4">📁</div>
          <h3 className="text-lg font-bold text-slate-900 mb-2">Drag and drop your image here</h3>
          <p className="text-trust-600 mb-3 font-medium">or click to browse</p>
          <p className="text-sm text-trust-600 opacity-70">Supported: JPG, PNG (Max 5MB)</p>
        </div>
      ) : (
        <div className="rounded-lg overflow-hidden border-2 border-trust-600 shadow-lg shadow-trust-500/10 animation-slide-in">
          <img src={preview} alt="Preview" className="w-full h-auto" />
          <div className="p-6 bg-white">
            <p className="text-slate-900 font-medium mb-4">📄 {fileName}</p>
            <button
              className="w-full px-4 py-2 bg-alert-500 hover:bg-alert-600 text-white font-semibold rounded-lg transition-all duration-200 disabled:bg-gray-300 disabled:cursor-not-allowed"
              onClick={handleClear}
              disabled={isLoading}
              aria-label="Remove image"
            >
              Remove Image
            </button>
          </div>
        </div>
      )}

      {error && (
        <div className="mt-4 p-4 bg-alert-100 border border-alert-300 text-alert-700 rounded-lg text-sm font-medium">
          {error}
        </div>
      )}

      {/* Hidden file input */}
      <input
        ref={fileInputRef}
        type="file"
        accept=".jpg,.jpeg,.png"
        onChange={handleFileInput}
        style={{ display: 'none' }}
        aria-hidden="true"
      />
    </div>
  );
}
