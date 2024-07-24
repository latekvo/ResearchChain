import { Spinner, Button } from "@nextui-org/react";
import type { RenderCompletionProps } from "@/app/types/RenderCompletionProps";

const RenderCompletion = ({
  executing,
  completion_result,
  handleClose,
}: RenderCompletionProps) => {
  return (
    <>
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
    </>
  );
};

export default RenderCompletion;
