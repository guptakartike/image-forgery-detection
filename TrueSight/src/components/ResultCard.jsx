/**
 * ResultCard Component
 * Displays the results of image forgery detection
 */
export default function ResultCard({ result, isLoading }) {
  if (!result && !isLoading) {
    return null;
  }

  return (
    <div className="bg-white rounded-lg overflow-hidden shadow-lg shadow-black/10 animation-slide-in mt-8 border-2 border-gray-200">
      {isLoading ? (
        <div className="flex flex-col items-center justify-center py-16 px-8 text-center">
          <div className="w-12 h-12 border-2 border-gray-300 border-t-trust-600 rounded-full animate-spin mb-4"></div>
          <p className="text-slate-900 font-bold text-lg mb-1">Analyzing image...</p>
          <p className="text-trust-600 font-medium text-sm">This may take a few seconds</p>
        </div>
      ) : (
        <>
          <div className={`px-8 py-6 flex items-center border-b-2 ${
            result.status === 'Authentic'
              ? 'bg-gradient-to-r from-trust-50 to-trust-100 border-trust-600'
              : 'bg-gradient-to-r from-alert-50 to-alert-100 border-alert-500'
          }`}>
            <div className="flex items-center gap-4 w-full">
              <div className={`flex items-center justify-center w-11 h-11 rounded-full bg-white font-bold text-2xl ${
                result.status === 'Authentic' ? 'text-trust-600' : 'text-alert-500'
              }`}>
                {result.status === 'Authentic' ? '✓' : '⚠'}
              </div>
              <span className={`text-2xl font-bold tracking-wide ${
                result.status === 'Authentic' ? 'text-trust-600' : 'text-alert-500'
              }`}>
                {result.status}
              </span>
            </div>
          </div>

          <div className="px-8 py-8">
            <div className="mb-8">
              <div className="flex justify-between items-center mb-3">
                <h4 className="text-slate-900 font-bold text-sm tracking-wide">Confidence Score</h4>
                <span className="text-2xl font-bold text-slate-900">{result.confidence}%</span>
              </div>
              <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all duration-600 ${
                    result.status === 'Authentic'
                      ? 'bg-gradient-to-r from-trust-600 to-trust-700'
                      : 'bg-gradient-to-r from-alert-500 to-alert-600'
                  }`}
                  style={{ width: `${result.confidence}%` }}
                />
              </div>
            </div>

            <div className="p-4 bg-gray-50 rounded-lg border-l-4 border-gray-300 mb-6">
              <h4 className="text-slate-900 font-bold text-sm mb-2 tracking-wide">Analysis Details</h4>
              <p className="text-gray-600 text-sm leading-relaxed">{result.explanation}</p>
            </div>

            <div className="pt-4 border-t border-gray-200 text-center">
              <small className="text-gray-400 text-xs">
                Analyzed on {new Date(result.timestamp).toLocaleString()}
              </small>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
