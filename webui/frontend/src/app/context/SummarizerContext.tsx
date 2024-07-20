"use client";

import { createContext, useState, ReactNode } from "react";

interface SummarizerContextProps {
  isSummarizing: boolean;
  completion?: { uuid: string; status: string; payload: string } | null;
  sendUuid: (uuid: string) => void;
  handleCloseCompletionModal: () => void;
}

interface SummarizerContextProviderProps {
  children?: ReactNode;
}

export const SummarizerContext = createContext<SummarizerContextProps | null>(
  null
);

const SummarizerContextProvider = ({
  children,
}: SummarizerContextProviderProps) => {
  const [isSummarizing, setIsSummarizing] = useState<boolean>(false);
  const [completion, setCompletion] = useState<{
    uuid: string;
    status: string;
    payload: string;
  } | null>();

  const socket = new WebSocket("ws://localhost:8000/ws");

  const sendUuid = (uuid: string) => {
    if (socket && socket.readyState === WebSocket.OPEN && uuid) {
      setIsSummarizing(true);
      socket.send(JSON.stringify({ uuid: uuid }));
    }
  };

  socket.onmessage = (event) => {
    try {
      const completion = JSON.parse(event.data);
      if (completion.uuid && completion.status === "summary completed") {
        setCompletion(completion);
        setIsSummarizing(false);
      }
    } catch (error) {
      console.error("Error parsing message:", error);
    }
  };
  console.log(isSummarizing, completion);

  const handleCloseCompletionModal = () => {
    setCompletion(null);
  };

  const value = {
    isSummarizing,
    completion,
    sendUuid,
    handleCloseCompletionModal,
  };

  return (
    <SummarizerContext.Provider value={value}>
      {children}
    </SummarizerContext.Provider>
  );
};

export default SummarizerContextProvider;
