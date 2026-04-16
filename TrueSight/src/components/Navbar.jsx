/**
 * Navbar Component
 * Display project title and navigation
 */
export default function Navbar() {
  return (
    <nav className="sticky top-0 z-100 bg-white border-b-2 border-trust-600 backdrop-blur-sm bg-opacity-95">
      <div className="max-w-7xl mx-auto px-8 py-4 flex justify-between items-center">
        <div className="flex items-center gap-3">
          <img src="/logo.svg" alt="TrueSight Logo" className="w-10 h-10" />
          <h1 className="text-xl font-bold bg-gradient-to-r from-slate-900 to-trust-600 bg-clip-text text-transparent tracking-wide">
            TrueSight
          </h1>
        </div>
        <p className="text-sm text-trust-600 font-medium hidden sm:block">
          Verify image authenticity with confidence
        </p>
      </div>
    </nav>
  );
}
