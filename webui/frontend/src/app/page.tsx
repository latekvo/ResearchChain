import PromptyInput from "./components/PromptInput";
import Header from "./components/Header";

export default function Page() {
  return (
    <div className="h-screen w-screen">
      <div className="flex">
        <Header></Header>
      </div>
      <div className="h-4/5 flex justify-center items-center">
        <PromptyInput />
      </div>
    </div>
  );
}
