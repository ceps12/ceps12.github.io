import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "ceps12 | Frontend Developer",
  description:
    "Frontend developer crafting modern web applications with React, TypeScript, and Next.js. Building clean, user-friendly interfaces.",
  keywords: [
    "ceps12",
    "frontend developer",
    "React",
    "TypeScript",
    "Next.js",
    "web developer",
  ],
  authors: [{ name: "ceps12" }],
  icons: {
    icon: "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>⚡</text></svg>",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={`${inter.variable} antialiased bg-background text-foreground`}
      >
        {children}
      </body>
    </html>
  );
}
