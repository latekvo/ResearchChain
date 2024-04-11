import PromptyInput from "./components/PromptInput";
import BackgroundSvg from "./components/Background";

export default function Page() {
  return (
      <section className="w-screen min-h-screen flex justify-center items-center bg-circle-purple bg-cover bg-center">
        <BackgroundSvg></BackgroundSvg>
        <PromptyInput />
      </section>
  );
}
