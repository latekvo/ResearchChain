import PromptyInput from "./components/PromptInput";
import BackgroundSvg from "./components/Background";
import Header from "./components/Header";

export default function Page() {
  return (
    <div className="h-screen w-screen">
      <BackgroundSvg />
      <div className=" flex ">
        <Header></Header>
      </div>
      <section className="h-4/5 flex justify-center items-center">
        <PromptyInput />
      </section>
    </div>
  );
}
