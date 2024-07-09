"use client";

import { createContext, useState, useEffect, ReactNode } from "react";

interface SummarizerContext {
  isSummarizing: boolean;
  completion: { uuid: string; status: string; payload: string }[];
  sendUuid: (uuid: string) => void;
}

interface SummarizerContextProviderProps {
  children?: ReactNode;
}

export const SummarizerContext = createContext<SummarizerContext | null>(null);

const SummarizerContextProvider = ({
  children,
}: SummarizerContextProviderProps) => {
  const [isSummarizing, setIsSummarizing] = useState<boolean>(false);
  const [completion, setCompletion] = useState<
    { uuid: string; status: string; payload: string }[]
  >([]);

  const socket = new WebSocket("ws://localhost:8000/ws");

  const sendUuid = (uuid: string) => {
    if (socket && socket.readyState === WebSocket.OPEN && uuid) {
      setIsSummarizing(false);
      socket.send(JSON.stringify({ uuid: uuid }));
    }
  };

  socket.onmessage = (event) => {
    try {
      const completion = JSON.parse(event.data);
      if (completion.uuid && completion.status === "summary completed") {
        setCompletion((prevCompletion) => [...prevCompletion, completion]);
      } else {
        console.error("Received message has an invalid structure:", completion);
      }
    } catch (error) {
      console.error("Error parsing message:", error);
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
