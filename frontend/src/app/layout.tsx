import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "RailPulse AI - Dynamic Forecast of Expected Time of Arrival (ETA) | Ministry of Railways (SIH26028)",
  description: "Dynamic ETA forecasting, Explainable AI (XAI) delay attribution, and dispatcher precedence simulator fusing real-time track telemetry with meteorological data.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="h-full">
      <body className="min-h-full flex flex-col bg-slate-50 text-slate-900 antialiased selection:bg-blue-100 selection:text-blue-900">
        {children}
      </body>
    </html>
  );
}
