import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "SepeCheck",
  description:
    "SepeCheck is a web application that allows you to check available SEPE offices by postal code.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${inter.className} bg-gradient-to-br from-gray-950 to-indigo-950`}
      >
        {children}
      </body>
    </html>
  );
}
