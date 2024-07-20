import { Spinner, Button } from "@nextui-org/react";
import type { RenderCompletionProps } from "@/app/types/RenderCompletionProps";

const RenderCompletion = ({
  executing,
  completion_result,
  handleClose,
}: RenderCompletionProps) => {
  return (
    <div className="w-3/5 flex-col relative">
      <div className="w-full px-6 py-8 shadow-xl rounded-xl border border-opacity-10 border-gray-400 bg-black bg-opacity-15 z-10 flex flex-col justify-between relative">
        {executing ? (
          <div className="h-full w-full flex items-center justify-center">
            <Spinner label="Loading..." color="secondary" size="lg" />
          </div>
        ) : (
          <>
            <p className="text-lg">{completion_result}</p>
            <div className="w-full flex justify-end items-center">
              <Button color="danger" variant="bordered" onClick={handleClose}>
                Close
              </Button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default RenderCompletion;
