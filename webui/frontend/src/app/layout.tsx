import React from "react";
import { Metadata } from "next";
import { Providers } from "./providers";
import Header from "./components/Header";
import "./globals.css";
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body>
        <Providers>
          <Header />
          {children}
        </Providers>
      </body>
    </html>
  );
}

export const metadata: Metadata = {
  title: "Research Chain",
};
