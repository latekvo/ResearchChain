"use client";
import { NextUIProvider } from "@nextui-org/react";
import { QueryClient, QueryClientProvider } from "react-query";
import SummarizerContextProvider from "@/app/context/SummarizerContext";

const queryClient = new QueryClient();
export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <NextUIProvider>
      <QueryClientProvider client={queryClient}>
        <SummarizerContextProvider>{children}</SummarizerContextProvider>
      </QueryClientProvider>
    </NextUIProvider>
  );
}
