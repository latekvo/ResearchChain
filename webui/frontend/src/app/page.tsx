import PromptInput from "./components/PromptInput";
import RenderCompletion from "./components/RenderCompletion";

export default function Page() {
  return (
    <>
      <main className="h-screen flex justify-center items-center flex-col">
        <PromptInput />
        <RenderCompletion
          executing={false}
          completion_result="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce lobortis justo lacus, id luctus leo laoreet id. Aenean nec lacus lobortis, pellentesque metus at, lacinia leo. Praesent quis viverra risus. Pellentesque tortor leo, tristique vitae quam a, fringilla eleifend tellus. Nullam pellentesque, nisl ut laoreet suscipit, orci est tempor neque, sit amet lobortis odio augue nec lectus. Phasellus feugiat sed ligula id pellentesque. Quisque bibendum eros a congue semper. Mauris eu dui pellentesque, pellentesque erat ac, bibendum eros. Aliquam suscipit, nulla non facilisis varius, ligula neque sollicitudin elit, nec lobortis purus magna at diam. Nullam accumsan luctus est, sit amet auctor nisl eleifend et. Cras accumsan erat sit amet tempus tristique.

"
        />
      </main>
    </>
  );
}
