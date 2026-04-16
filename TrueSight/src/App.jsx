import { useState } from 'react';
import './index.css';
import Navbar from './components/Navbar';
import HeroSection from './components/HeroSection';
import ImageUpload from './components/ImageUpload';
import ResultCard from './components/ResultCard';
import Footer from './components/Footer';
import { detectImageForgery } from './services/detectionService';

/**
 * Main App Component
 * Orchestrates the image forgery detection workflow
 */
function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  /**
   * Handle image selection from upload component
   * @param {File} imageFile - The selected image file
   */
  const handleImageSelect = (imageFile) => {
    setSelectedImage(imageFile);
    setResult(null); // Clear previous results
  };

  /**
   * Trigger the forgery detection analysis
   */
  const handleDetect = async () => {
    if (!selectedImage) {
      alert('Please select an image first');
      return;
    }

    setIsLoading(true);
    try {
      const detectionResult = await detectImageForgery(selectedImage);
      setResult(detectionResult);
    } catch (error) {
      console.error('Detection error:', error);
      alert('An error occurred during analysis. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col min-h-screen w-full bg-white">
      <Navbar />
      <HeroSection />

      <main className="flex-1 py-12 px-5 sm:py-16">
        <div className="max-w-3xl mx-auto">
          <section>
            <div className="flex flex-col items-center gap-6">
              <ImageUpload onImageSelect={handleImageSelect} isLoading={isLoading} />

              {selectedImage && (
                <button
                  className="px-8 py-3 bg-gradient-to-r from-trust-600 to-trust-700 text-white font-semibold rounded-lg transition-all duration-300 hover:shadow-lg hover:shadow-trust-500/30 active:scale-95 disabled:bg-slate-300 disabled:cursor-not-allowed disabled:opacity-100 disabled:shadow-none"
                  onClick={handleDetect}
                  disabled={isLoading}
                  aria-label="Start authentication verification"
                >
                  {isLoading ? 'Verifying...' : 'Verify Authenticity'}
                </button>
              )}
            </div>

            <ResultCard result={result} isLoading={isLoading} />
          </section>
        </div>
      </main>

      <Footer />
    </div>
  );
}

export default App;
