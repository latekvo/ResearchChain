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
  let heightClass = "h-60";
  if (isSummarizing) {
    heightClass = "h-32";
  } else if (completion) {
    heightClass = "h-2/3";
  }
  return (
    <>
      <main className="h-screen flex justify-center items-center flex-col">
        <div
          className={`w-3/5 px-6 relative py-8 shadow-xl rounded-xl border border-opacity-10 border-gray-400 bg-black bg-opacity-15 z-10 flex flex-col justify-between ${heightClass} transition-all duration-500 ease-in-out overflow-y-auto`}
          data-testid="blackbox"
        >
          {isSummarizing || completion ? (
            <RenderCompletion
              executing={isSummarizing}
              handleClose={handleCloseCompletionModal}
              completion_result={completion?.payload}
            />
          ) : (
            <PromptInput />
          )}
        </div>
      </main>
    </>
  );
}
