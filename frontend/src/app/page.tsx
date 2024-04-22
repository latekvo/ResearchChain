import PromptyInput from "./components/PromptInput";
import BackgroundSvg from "./components/Background";
import Header from "./components/Header";

export default function Page() {
  return (
    <div className="h-screen w-screen ">
       <head>
        <style>{`
          body {
            background: rgb(9,10,11);
            background: linear-gradient(70deg, rgba(9,10,11,1) 0%, rgba(24,36,62,0.45284051120448177) 29%, rgba(7,9,14,0.5704875700280112) 54%, rgba(28,4,46,0.5844931722689075) 83%, rgba(16,7,23,0.7665660014005602) 98%);
        `}</style>

      </head>
      <div className=" flex ">
        <Header></Header>
      </div>
      <section className="h-4/5 flex justify-center items-center">
        <PromptyInput />
      </section>
    </div>
  );
}
