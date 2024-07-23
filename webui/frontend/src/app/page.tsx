"use client";
import { useContext } from "react";
import PromptInput from "./components/PromptInput";
import RenderCompletion from "./components/RenderCompletion";
import { SummarizerContext } from "./context/SummarizerContext";

export default function Page() {
  const context = useContext(SummarizerContext);
  const isSummarizing = context?.isSummarizing ?? false;
  const completion = context?.completion ?? null;
  const handleCloseCompletionModal = context!.handleCloseCompletionModal;
  return (
    <>
      <main className="min-h-screen flex justify-center items-center flex-col">
        {isSummarizing || completion ? (
          <RenderCompletion
            executing={isSummarizing}
            handleClose={handleCloseCompletionModal}
            completion_result={completion?.payload}
          />
        ) : (
          <PromptInput />
        )}
      </main>
    </>
  );
}
