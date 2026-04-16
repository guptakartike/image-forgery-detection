/**
 * Footer Component
 * Display credits and additional information
 */
export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-white border-t-2 border-trust-600 py-8 px-5 mt-16">
      <div className="max-w-7xl mx-auto px-8 flex flex-col sm:flex-row justify-between items-center gap-5 flex-wrap">
        <div className="flex-1 min-w-full sm:min-w-auto">
          <p className="text-trust-600 font-medium mb-2">
            &copy; {currentYear} TrueSight. All rights reserved.
          </p>
          <p className="text-gray-600 text-sm leading-relaxed">
            <strong className="text-slate-900">Disclaimer:</strong> This is a demonstration project for educational purposes only.
            Results are simulated and not based on real image analysis.
          </p>
        </div>
        <div className="text-right">
          <p className="text-gray-600 text-sm">Built with React + Vite + Tailwind CSS</p>
        </div>
      </div>
    </footer>
  );
}
