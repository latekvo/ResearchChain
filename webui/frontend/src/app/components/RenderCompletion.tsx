import { Spinner, Button } from "@nextui-org/react";
import type { RenderCompletionProps } from "@/app/types/RenderCompletionProps";
import { IoMdClose } from "react-icons/io";

const RenderCompletion = ({
  executing,
  completion_result,
  handleClose,
}: RenderCompletionProps) => {
  return (
    <>
      {executing ? (
        <div className="flex items-center justify-center">
          <Spinner label="Loading..." color="secondary" size="lg" />
        </div>
      ) : (
        <div>
          <p className="pb-4 text-primary text-2xl">Result</p>
          <IoMdClose
            className="rounded-2xl absolute top-2 right-2 hover:bg-gray-800 p-1 cursor-pointer text-3xl"
            onClick={handleClose}
          ></IoMdClose>
          <div className="overflow-auto ">
            <p className="text-lg">{completion_result}</p>
          </div>
        </div>
      )}
    </>
  );
};

export default RenderCompletion;
