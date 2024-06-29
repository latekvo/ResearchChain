"use client";

import { createContext, useState, useEffect, ReactNode } from "react";

interface SummarizerContext {
  isSummarizing: boolean;
  completion: string;
  sendUuid: (uuid: string | undefined) => void;
}

interface SummarizerContextProviderProps {
  children?: ReactNode;
}

export const SummarizerContext = createContext<SummarizerContext | null>(null);

const SummarizerContextProvider = ({
  children,
}: SummarizerContextProviderProps) => {
  const [isSummarizing, setIsSummarizing] = useState<boolean>(false);
  const [completion, setCompletion] = useState<string>("");

  const socket = new WebSocket("ws://localhost:8000/ws");

  const sendUuid = (uuid?: string) => {
    if (socket && socket.readyState === WebSocket.OPEN) {
      setIsSummarizing(true);
      socket.send(JSON.stringify({ uuid: uuid }));
    }
  };

  const value = {
    isSummarizing,
    completion,
    sendUuid,
  };

  return (
    <SummarizerContext.Provider value={value}>
      {children}
    </SummarizerContext.Provider>
  );
};

export default SummarizerContextProvider;
