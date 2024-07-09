import PromptInput from "./components/PromptInput";
import RenderCompletion from "./components/RenderCompletion";

export default function Page() {
  return (
    <>
      <main className="h-screen flex justify-center items-center flex-col">
        <PromptInput />
        <RenderCompletion
          executing={false}
          completion_result=""
        />
      </main>
    </>
  );
}
