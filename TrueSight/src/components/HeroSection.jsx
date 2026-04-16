/**
 * HeroSection Component
 * Displays introduction and explanation of image forgery detection
 */
export default function HeroSection() {
  return (
    <section className="bg-white border-b-2 border-trust-600 py-8 px-5 sm:py-12">
      <div className="max-w-3xl mx-auto">
        <h2 className="text-4xl font-bold text-center bg-gradient-to-r from-slate-900 to-trust-600 bg-clip-text text-transparent mb-4">
          Verify Image Authenticity
        </h2>
        <p className="text-center text-gray-600 mb-8 max-w-2xl mx-auto leading-relaxed">
          Upload an image to TrueSight and verify its authenticity. Our advanced analysis
          examines lighting patterns, pixel consistency, and metadata to assess trust and integrity.
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
          <div className="p-5 border-2 border-gray-200 rounded-lg text-center transition-all duration-300 hover:border-trust-600 hover:bg-trust-50 hover:shadow-lg hover:shadow-trust-500/10">
            <span className="block text-3xl mb-3">📸</span>
            <h3 className="font-bold text-slate-900 mb-2 tracking-wide">Image Analysis</h3>
            <p className="text-gray-600 text-sm leading-relaxed">Comprehensive examination of image integrity and consistency</p>
          </div>

          <div className="p-5 border-2 border-gray-200 rounded-lg text-center transition-all duration-300 hover:border-trust-600 hover:bg-trust-50 hover:shadow-lg hover:shadow-trust-500/10">
            <span className="block text-3xl mb-3">✓</span>
            <h3 className="font-bold text-slate-900 mb-2 tracking-wide">Authenticity Check</h3>
            <p className="text-gray-600 text-sm leading-relaxed">Identifies signs of manipulation and forgery with precision</p>
          </div>

          <div className="p-5 border-2 border-gray-200 rounded-lg text-center transition-all duration-300 hover:border-trust-600 hover:bg-trust-50 hover:shadow-lg hover:shadow-trust-500/10">
            <span className="block text-3xl mb-3">📊</span>
            <h3 className="font-bold text-slate-900 mb-2 tracking-wide">Trust Score</h3>
            <p className="text-gray-600 text-sm leading-relaxed">Quantified reliability measure for authentication results</p>
          </div>
        </div>
      </div>
    </section>
  );
}
