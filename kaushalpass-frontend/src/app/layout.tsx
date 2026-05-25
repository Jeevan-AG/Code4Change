import type { Metadata } from "next";
import { Outfit } from "next/font/google";
import "./globals.css";

const outfit = Outfit({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "KaushalLink - Premium AI Opportunity Engine",
  description: "Personalized government schemes, training, and jobs.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={`${outfit.className} bg-[#050505] text-neutral-200 min-h-screen antialiased selection:bg-purple-500/30`}>
        {children}
      </body>
    </html>
  );
}
